<template>
    <div>
        <div style="padding: 20px">
        Hi, {{userProfile.fullname || userProfile.username}}
        </div>
        <div class="p-grid">
            <div class="p-col">
                My assigned tasks:
                <div v-if="myTasks.filter(t => t.status == 'to_do' || t.status == 'ongoing').length">
                    <ScrollPanel>
                        <div
                            v-for="task in myTasks.filter(t => t.status == 'to_do' || t.status == 'ongoing')"
                            :key="task.id"
                            @click="assignedTaskClicked(task)"
                            style="cursor: pointer;"
                        >
                            <Divider />
                            <div class="p-grid">
                                <div class="p-col">
                                    {{task.name}}
                                </div>
                                <div class="p-col-fixed" style="width: 130px">
                                    <Tag v-if="task.status == 'ongoing'" value="Ongoing" severity="success"/>
                                    <Tag v-else-if="task.status =='to_do'" value="In sprint backlog" severity="warning"/>
                                </div>
                            </div>
                        </div>
                    </ScrollPanel>
                </div>
                <div v-else style="font-style: italic; padding-top: 10px;">
                    You don't have any assigned tasks to worry about!
                </div>
                
            </div>
            <div class="p-col-1">
                <Divider layout="vertical" />
            </div>
            <div class="p-col">
                <FullCalendar :events="events" :options="calendarOptions"/>
            </div>
        </div>

        <Dialog v-model:visible="displayTask" style="width: 500px" header="Task">
            <Divider>
                Name
            </Divider>
                {{clickedTask.name}}
            <Divider>
                Description
            </Divider>
                <div v-if="clickedTask.description">
                    {{clickedTask.description}}
                </div>
                <div v-else style="font-style: italic;">
                    No description set for this task. Remeber that every team member should know what DoD is for each task.
                </div>

        </Dialog>
        <Dialog header="Event" :contentStyle="{overflow: 'visible'}" :modal="true" v-model:visible="displayEvent">
            <Divider>
                Title
            </Divider>
                {{clickedEvent.title}}
            <Divider>
                Description
            </Divider>
                <div v-if="clickedEvent.extendedProps.description">
                    {{clickedEvent.extendedProps.description}}
                </div>
                <div v-else style="font-style: italic;">
                    None
                </div>
            <Divider>
                Event type
            </Divider>
                <EventInfo :eventType="clickedEvent.extendedProps.eventType"/>
            <Divider>
                Start & End Dates
            </Divider>
                <div class="p-grid">
                    <div class="p-col-fixed" style="width: 4.5rem">
                        Start:
                    </div>
                    <div class="p-col">
                        {{getEventStartDateString(clickedEvent)}}
                    </div>
                </div>
                <div class="p-grid">
                    <div class="p-col-fixed" style="width: 4.5rem">
                        End:
                    </div>

                    <div class="p-col">
                        {{getEventEndDateString(clickedEvent)}}
                    </div>
                </div>
        </Dialog>
    </div>
</template>

<script>
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid';
import listPlugin from '@fullcalendar/list';
import interactionPlugin from '@fullcalendar/interaction'
import LocalStorageDataService from '../services/LocalStorageDataService'
import TaskDataService from '../services/TaskDataService'
// import EventDataService from '../services/EventDataService'
import useEvents from '../store/events'

export default {
    data(){
        return{
            expandedRows: [],
            clickedTask: null,
            displayTask: false,
            clickedEvent: null,
            displayEvent: false,
            userProfile: {
                filters: {},
                username: null,
                fullname: null,
                bio: null,
                phoneNumber: null,
                email: null,
                image: null
            },
            calendarOptions: {
                plugins:[dayGridPlugin, timeGridPlugin, interactionPlugin, listPlugin],
                initialDate: new Date(),
                nowIndicator: true,
                headerToolbar: {
                    left: 'prev,next',
                    center: 'title',
                    right: 'dayGridMonth,listWeek'
                },
                forceEventDuration: true,
                dayMaxEventRows: 2,
                editable: true,
                height: "55vh",
                // dateClick: (e) => {
                //     console.log(e)
                // },
                eventDrop: async (e) => {
                    await this.editEvent(e.event)
                },
                eventClick: (e) => {
                    console.log(e.event)
                    this.eventClicked(e.event)
                }
            }
        }
    },
    async setup(){
        const myTasks = (await TaskDataService.getAllUserTasks())?.data
        const {events, getCurrentUserEvents} = useEvents()
        getCurrentUserEvents()
        return{
            myTasks,
            events
        }
    },
    created(){
        const user = LocalStorageDataService.getUser()
        
        this.userProfile.username = user.profile.username
        this.userProfile.fullname = user.profile.fullname
        this.userProfile.bio = user.profile.bio
        this.userProfile.phoneNumber = user.profile.phone_number
        this.userProfile.email = user.profile.email
        this.userProfile.image = user.profile.image
    },
    methods: {
        getToDoStatusText(task){
            var texts = [
                `${task.name} is waiting in sprint backlog for You!`,
                `Have you heard? ${task.name} is waiting!`
            ]
            return texts[Math.floor(Math.random() * texts.length)];
        },
        getOngoingStatusText(task){
            var texts = [
                `Are you properly working on ${task.name}?`,
                `You need to work on ${task.name} right now!`,
                'aaa',
                'bbb'
            ]

            return texts[Math.floor(Math.random() * texts.length)];
        },
        getTaskText(task){
            switch(task.status){
                case 'todo':
                    return this.getToDoStatusText(task)
                case 'ongoing':
                    return this.getOngoingStatusText(task)
            }
        },
        assignedTaskClicked(task){
            this.clickedTask = task
            this.displayTask = true
        },
        eventClicked(event){
            this.clickedEvent = event
            this.displayEvent = true
        },
        getEventStartDateString(event){
            return this.getEventDate(event.start)
        },
        getEventEndDateString(event){
            return this.getEventDate(event.end)
        },
        getEventDate(dateString){
            var date = new Date(dateString)
            var weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
            var weekday = weekdays[date.getDay()]
            var day = date.getDate()
            var months = ['January', 'Febuary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            var month = months[date.getMonth()]
            var hours = date.getHours()
            var minutes = date.getMinutes()
            if (minutes == 0){
                minutes = '00'
            }
            return `${weekday}, ${day} of ${month} at ${hours}:${minutes}`
        },
    }
}
</script>

<style>

</style>