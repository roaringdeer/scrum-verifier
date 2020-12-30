import {reactive, toRefs} from 'vue';
import EventDataService from '../services/EventDataService'

const state = reactive({
    events: []
})

function parseEvent(dbEvent){
    return{
        id: dbEvent.id,
        title: dbEvent.title,
        start: dbEvent.start_date,
        end: dbEvent.end_date,
        allDay: dbEvent.all_day,
        description: dbEvent.description,
        eventType: dbEvent.event_type,
        projectId: dbEvent.project_id
    }
}

export default function useEvents() {

    const getEvents = async (projectId) => {
        const gotEvents = (await EventDataService.getAllProjectEvents(projectId))?.data
        state.events = gotEvents.map(e => parseEvent(e))
    }

    const getCurrentUserEvents = async () => {
        const gotEvents = (await EventDataService.getAllUserEvents())?.data
        state.events = gotEvents.map(e => parseEvent(e))
    }

    const createEvent = async (eventToCreate, projectId) => {
        console.log(eventToCreate)
        if (eventToCreate.allDay){
            const today = new Date()
            const tomorrow = new Date(today)
            tomorrow.setDate(tomorrow.getDate() + 2)
            tomorrow.setHours(0,0,0,0)
            eventToCreate.selectedDateEnd = tomorrow
        }
        console.log(eventToCreate)
        const createdTask = (await EventDataService.createNewEvent({
            new_event: {
                title: eventToCreate.title,
                description: eventToCreate.description,
                start_date: eventToCreate.selectedDateStart,
                end_date: ((eventToCreate.selectedDateEnd==null) ? eventToCreate.selectedDateStart : eventToCreate.selectedDateEnd),
                all_day: eventToCreate.allDay,
                event_type: eventToCreate.eventType,
                project_id: projectId
            }
        }))?.data
        state.events.push(parseEvent(createdTask))
    }

    const editEvent = async (eventToUpdate) => {
        console.log(eventToUpdate)
        const updatedEvent = (await EventDataService.updateEvent(
            eventToUpdate.id,
        {
            event_update: {
                title: eventToUpdate.title,
                description: eventToUpdate.description,
                start_date: eventToUpdate.selectedDateStart,
                end_date: ((eventToUpdate.selectedDateEnd==null) ? eventToUpdate.selectedDateStart : eventToUpdate.selectedDateEnd),
                all_day: eventToUpdate.allDay,
                event_type: eventToUpdate.eventType
            }
        }
        ))?.data
        console.log(parseEvent(updatedEvent))
        state.events[state.events.findIndex(el => el.id == updatedEvent.id)] = parseEvent(updatedEvent)
    }

    const deleteEvent = async (eventToDelete) => {
        // console.log(state.events)
        state.events = state.events.filter(val => val.id != eventToDelete.id);
        // console.log(state.events)
        await EventDataService.deleteEvent(eventToDelete.id)
    }

    const clearEvents = async () => {
        state.events = []
    }

    return {
        ...toRefs(state),
        getEvents,
        createEvent,
        editEvent,
        deleteEvent,
        clearEvents,
        getCurrentUserEvents
    }
}