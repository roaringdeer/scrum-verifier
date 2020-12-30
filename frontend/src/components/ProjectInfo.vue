<template>
    <div>
        <div class="p-grid">
            <div class="p-col" >
                <div style="float: left; font-weight: bold; font-size: 2em; text-overflow: clip;">
                    {{selectedProject.name}}
                </div>
                <ScrollPanel style="height: 10vh">
                    <p style="text-align: justify; white-space: pre-wrap;">
                    {{selectedProject.description}}
                    </p>
                </ScrollPanel>
            </div>
            <div class="p-col-2" v-tooltip="tooltip">
                <Knob v-model="progress" style="width: 100%" :readonly="true" valueTemplate="{value}%"/>
            </div>
        </div>

        <FullCalendar ref="fullCalendar" :key="calendarKey" :events="events" :options="calendarOptions"/>

        <Dialog header="Create new event" :contentStyle="{overflow: 'visible'}" :modal="true" v-model:visible="createEventDialog" :closable="false">
            <Divider>
                Title
            </Divider>
            <InputText v-model="selectedEvent.title" style="float: left; width: 80%;"/>
            <Divider>
                Description
            </Divider>
            <Textarea v-model="selectedEvent.description" rows="5" cols="30" :autoResize="true" style="float: left; width: 80%;" />
            <Divider>
                Type
            </Divider>
            <div v-for="eventType of eventTypes" :key="eventType.key" class="p-field-radiobutton">
                <RadioButton :id="eventType.key" name="role" :value="eventType.key" v-model="selectedEvent.eventType" />
                <label :for="eventType.key">{{eventType.value}}</label>
            </div>
            <Divider>
                Start & End Dates
            </Divider>
            <div v-if="!selectedEvent.allDay">
                <Calendar v-model="selectedEvent.selectedDateStart" :inline="false" :showTime="true"/> - 
                <Calendar v-model="selectedEvent.selectedDateEnd" :inline="false" :showTime="true"/>
            </div>
            <div v-else>
                <Calendar v-model="selectedEvent.selectedDateStart" :inline="false" :showTime="false"/> - 
                <Calendar v-model="selectedEvent.selectedDateEnd" :inline="false" :showTime="false"/>
            </div>
            <Divider>
                All day
            </Divider>
            <InputSwitch v-model="selectedEvent.allDay"/>
            <template #footer>
                <Button label="Cancel" icon="pi pi-times" class="p-button-text" @click="closeCreateEventDialog"/>
                <Button label="Create" icon="pi pi-check" class="p-button-text" @click="createNewEvent" />
            </template>
        </Dialog>

        <Dialog header="Event" :contentStyle="{overflow: 'visible'}" :modal="true" v-model:visible="eventDialog" :closable="false">
            <Divider>
                Title
            </Divider>
                {{selectedEvent.title}}
            <Divider>
                Description
            </Divider>
                <div v-if="selectedEvent.description">
                    {{selectedEvent.description}}
                </div>
                <div v-else style="font-style: italic;">
                    None
                </div>
            <Divider>
                Event type
            </Divider>
                <EventInfo :eventType="selectedEvent.eventType"/>

            <Divider>
                Start & End Dates
            </Divider>
                <div class="p-grid">
                    <div class="p-col-fixed" style="width: 4rem">
                        Start:
                    </div>
                    <div class="p-col">
                        {{getEventStartDateString(selectedEvent)}}
                    </div>
                </div>
                <div class="p-grid">
                    <div class="p-col-fixed" style="width: 4rem">
                        End:
                    </div>

                    <div class="p-col">
                        {{getEventEndDateString(selectedEvent)}}
                    </div>
                </div>
            <template #footer>
                <Button label="Cancel" icon="pi pi-times" class="p-button-text" @click="closeEventDialog"/>
                <Button label="Edit" icon="pi pi-pencil" class="p-button-text" @click="openEditEventDialog" />
            </template>
        </Dialog>

        <Dialog header="Edit event" :contentStyle="{overflow: 'visible'}" :modal="true" v-model:visible="editEventDialog" :closable="false">
            <Divider>
                Title
            </Divider>
            <InputText v-model="selectedEvent.title" style="float: left; width: 80%;"/>
            <Divider>
                Description
            </Divider>
            <Textarea v-model="selectedEvent.description" rows="5" cols="30" :autoResize="true" style="float: left; width: 80%;" />
            <Divider>
                Type
            </Divider>
            <div v-for="eventType of eventTypes" :key="eventType.key" class="p-field-radiobutton">
                <RadioButton :id="eventType.key" name="role" :value="eventType.key" v-model="selectedEvent.eventType" />
                <label :for="eventType.key">{{eventType.value}}</label>
            </div>
            <Divider>
                Start & End Dates
            </Divider>
                <Calendar v-model="selectedEvent.selectedDateStart" :inline="false" :showTime="true"/> - 
                <Calendar v-model="selectedEvent.selectedDateEnd" :inline="false" :showTime="true"/>
            <Divider>
                All day
            </Divider>
            <InputSwitch v-model="selectedEvent.allDay"/>
            <template #footer>
                <Button label="Delete" icon="pi pi-trash" class="p-button-text" @click="openDeleteEventDialog" style="float: left;"/>
                <Button label="Cancel" icon="pi pi-times" class="p-button-text" @click="closeEditEventDialog"/>
                <Button label="Save" icon="pi pi-check" class="p-button-text" @click="editSelectedEvent" />
            </template>
        </Dialog>

        <Dialog header="Confirmation" v-model:visible="deleteEventDialog" :style="{width: '350px'}" :modal="true">
        <div class="confirmation-content">
            <i class="pi pi-exclamation-triangle p-mr-3" style="font-size: 2rem" />
            <span>Are you sure you want to proceed?</span>
        </div>
        <template #footer>
            <Button label="No" icon="pi pi-times" @click="closeDeleteEventDialog" class="p-button-text" autofocus/>
            <Button label="Yes" icon="pi pi-check" @click="deleteSelectedEvent" class="p-button-text"/>
        </template>
        </Dialog>

    </div>
</template>

<script>
import useProjects from '../store/projects'
import useTasks from '../store/tasks'
import useEvents from '../store/events'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction'
export default {
    data(){
        return{
            calendarKey: 0,
            selectedEvent:{
                id: null,
                title: "",
                description: "",
                eventType: "other",
                selectedDateStart: new Date(),
                selectedDateEnd: new Date(),
                allDay: false
            },
            eventTypes: [
                {value:"Other", key: 'other'},
                {value:"Daily", key: 'daily'},
                {value:"Sprint Retrospective", key: 'retro'},
                {value:"Sprint Review", key: 'review'},
                {value:"Sprint Planning", key: 'planning'},
            ],
            eventDialog: false,
            clickedEvent: null,
            createEventDialog: false,
            editEventDialog: false,
            deleteEventDialog: false,
            calendarOptions: {
                plugins:[dayGridPlugin, timeGridPlugin, interactionPlugin],
                initialDate: new Date(),
                nowIndicator: true,
                headerToolbar: {
                    left: 'prev,next,myCustomButton',
                    center: 'title',
                    right: 'dayGridMonth,timeGridWeek,timeGridDay'
                },
                forceEventDuration: true,
                dayMaxEventRows: 2,
                editable: true,
                height: "55vh",
                dateClick: (e) => {
                    console.log(e)
                },
                eventDrop: async (e) => {
                    await this.handleEventDrop(e.event)
                    
                    console.log(e.event.title)
                },
                eventClick: (e) => {
                    this.handleEventClick(e.event)
                },
                customButtons: {
                    myCustomButton: {
                        text: "Add new event",
                        click: () => this.createEventDialog = true
                    },
                }
            },
        }
    },
    async setup(){
        const { selectedProject, getProjectProgress } = useProjects()
        const {backlog, todo, ongoing, done} = useTasks()
        const {events, createEvent, editEvent, deleteEvent} = useEvents()
        return{
            selectedProject,
            getProjectProgress,
            backlog,
            todo,
            ongoing,
            done,
            events,
            createEvent,
            editEvent,
            deleteEvent
        }
    },
    computed:{
        progress: function (){
            try{
                return this.getProjectProgress(this.selectedProject.id)
            }
            catch(error){
                console.log(error)
                return 0
            }
        },
        tooltip: function (){
            return `Backlog:\t${this.selectedProject.stats.backlog_count}
                    To do:\t${this.selectedProject.stats.todo_count}
                    Ongoing:\t${this.selectedProject.stats.ongoing_count}
                    Done:\t${this.selectedProject.stats.done_count}`
        },
        eventTypeDisplayed: function (){
            switch (this.selectedEvent.eventType){
                case 'other':
                    return 'Other'
                case 'daily':
                    return 'Daily'
                case 'retro':
                    return 'Sprint Retrospective'
                    case 'review':
                    return 'Sprint Review'
                case 'planning':
                    return 'Sprint Planning'
                default:
                    return 'Unknown'
                
            }
        }
    },
    methods: {
        async createNewEvent(){
            console.log(this.selectedEvent)
            await this.createEvent(this.selectedEvent, this.selectedProject.id)
            this.closeCreateEventDialog()
        },
        closeCreateEventDialog(){
            this.refreshEvents()
            this.createEventDialog = false
        },
        async handleEventDrop(event){
            this.selectedEvent.id = event.id
            this.selectedEvent.title = event.title
            this.selectedEvent.selectedDateStart = event.start
            this.selectedEvent.selectedDateEnd = event.end
            this.selectedEvent.allDay = event.allDay
            this.selectedEvent.description = event.extendedProps.description
            this.selectedEvent.eventType = event.extendedProps.eventType
            this.selectedEvent.projectId = event.extendedProps.projectId
            await this.editEvent(this.selectedEvent)
        },
        handleEventClick (event){
            this.selectedEvent.id = event.id
            this.selectedEvent.title = event.title
            this.selectedEvent.selectedDateStart = event.start
            this.selectedEvent.selectedDateEnd = event.end
            this.selectedEvent.allDay = event.allDay
            this.selectedEvent.description = event.extendedProps.description
            this.selectedEvent.eventType = event.extendedProps.eventType
            this.selectedEvent.projectId = event.extendedProps.projectId
            this.openEventDialog()
        },
        openEventDialog(){
            this.eventDialog = true;
        },
        closeEventDialog(){
            this.eventDialog = false;
            this.clearSelectedEvent()
        },
        openEditEventDialog(){
            this.editEventDialog = true;
        },
        closeEditEventDialog(){
            this.editEventDialog = false;
        },
        async editSelectedEvent(){
            await this.editEvent(this.selectedEvent)
            this.refreshEvents()
            this.closeEditEventDialog()
        },
        openDeleteEventDialog(){
            this.deleteEventDialog = true
        },
        closeDeleteEventDialog(){
            this.deleteEventDialog = false
        },
        async deleteSelectedEvent(){
            await this.deleteEvent(this.selectedEvent)
            this.refreshEvents()
            this.closeDeleteEventDialog()
            this.closeEditEventDialog()
            this.closeEventDialog()
        },
        refreshEvents(){
            var eventSources = this.$refs.fullCalendar.calendar.getEventSources()
            for (var i in eventSources){
                var evres = eventSources[i]
                evres.refetch()
            }
            this.$refs.fullCalendar.calendar.render()
            console.log(this.events)
        },
        clearSelectedEvent(){
            this.selectedEvent.id = null
            this.selectedEvent.title = ""
            this.selectedEvent.description = ""
            this.selectedEvent.eventType = "other"
            this.selectedEvent.selectedDateStart = new Date()
            this.selectedEvent.selectedDateEnd = new Date()
            this.selectedEvent.allDay = false
        },
        getEventStartDateString(event){
            return this.getEventDate(event.selectedDateStart)
        },
        getEventEndDateString(event){
            return this.getEventDate(event.selectedDateEnd)
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