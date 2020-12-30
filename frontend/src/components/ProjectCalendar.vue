<template>
    <div>
        {{events}}
        <FullCalendar ref="projectFullCalendar" :events="events" :options="calendarOptions" />

        <Dialog header="Create new event" :contentStyle="{overflow: 'visible'}" :modal="true" v-model:visible="createEventDialog">
            <Divider>
                Title
            </Divider>
            <InputText v-model="title" style="float: left; width: 80%;"/>
            <Divider>
                Description
            </Divider>
            <Textarea v-model="description" rows="5" cols="30" :autoResize="true" style="float: left; width: 80%;"/>
            <Divider>
                Type
            </Divider>
            <Dropdown
                v-model="eventType"
                :options="eventTypeOptions"
                optionLabel="value"
                placeholder="Select Type"
                style="float: left; width: 80%;"
            />
            <Divider>
                Start & End Dates
            </Divider>
            <Calendar v-model="selectedDateStart" :inline="false" :showTime="true"/> - 
            <Calendar v-model="selectedDateEnd" :inline="false" :showTime="true"/>
            
            <Divider>
                All day
            </Divider>
            <InputSwitch v-model="allDay"/>
            <template #footer>
                <Button label="Cancel" icon="pi pi-times" class="p-button-text" @click="closeCreateEventDialog"/>
                <Button label="Create" icon="pi pi-check" class="p-button-text" @click="createNewEvent" />
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
            title: "",
            description: "",
            eventType: "other",
            eventTypeOptions: [
                {value:"Other", key: 'other'},
                {value:"Daily", key: 'daily'},
                {value:"Retro", key: 'retro'},
                {value:"Planning", key: 'planning'},
            ],
            selectedDateStart: new Date(),
            selectedDateEnd: new Date(),
            allDay: false,
            createEventDialog: false,
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
                editable: true,
                height: "50vh",
                dateClick: (e) => {
                    console.log(e)
                },
                eventDrop: async (e) => {
                    await this.editEvent(e.event)
                    console.log(e.event.title)
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
        const { selectedProject } = useProjects()
        const {backlog, todo, ongoing, done} = useTasks()
        const {events, createEvent, editEvent} = useEvents()
        return{
            selectedProject,
            backlog,
            todo,
            ongoing,
            done,
            events,
            createEvent,
            editEvent
        }
    },
    mounted(){
        // window.resize()
        // $(window).resize()
        
        // for (var v in this.$refs.projectFullCalendar.initialize){
        //     console.log(v)
        // }
        // console.log(this.$refs.projectFullCalendar)
        // this.$refs.projectFullCalendar.getApi().render()
    },
    methods: {
        toggle(event){
            this.$refs.menu.toggle(event)
        },
        async createNewEvent(){
            var newEvent = {
                title: this.title,
                description: this.description,
                project_id: this.selectedProject.id,
                start_date: this.selectedDateStart,
                end_date: this.selectedDateEnd,
                all_day: this.allDay
            }
            await this.createEvent(newEvent)
            console.log(this.events)
            this.closeCreateEventDialog()
        },
        closeCreateEventDialog(){
            this.createEventDialog = false
        }
    }
}
</script>

<style>

</style>