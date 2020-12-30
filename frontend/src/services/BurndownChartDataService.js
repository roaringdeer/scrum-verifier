import {httpAuth} from "../http-common";

class EventDataService{
    async getAllUserEvents(){
        return await httpAuth.get('/events/')
    }

    async getAllProjectEvents(projectId){
        return await httpAuth.get(`/projects/${projectId}/events`)
    }

    async createNewEvent(newEvent){
        return await httpAuth.post('/events/', newEvent)
    }

    async getEvent(eventId){
        return await httpAuth.get(`/events/${eventId}`)
    }

    async updateEvent(eventId, eventUpdate){
        return await httpAuth.put(`/events/${eventId}`, eventUpdate)
    }

    async deleteEvent(eventId){
        return await httpAuth.delete(`/events/${eventId}`)
    }
}

export default new EventDataService();