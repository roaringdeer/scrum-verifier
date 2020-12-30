import {httpAuth} from "../http-common";

class TaskDataService{
    async getAllUserTasks(){
        return await httpAuth.get('/tasks/')
    }

    async getAllProjectTasks(projectId){
        return await httpAuth.get(`/projects/${projectId}/tasks`)
    }

    async getToDoProjectTasks(projectId){
        return await httpAuth.get(`/projects/${projectId}/tasks/todo`)
    }

    async getOngoingProjectTasks(projectId){
        return await httpAuth.get(`/projects/${projectId}/tasks/ongoing`)
    }

    async getDoneProjectTasks(projectId){
        return await httpAuth.get(`/projects/${projectId}/tasks/done`)
    }

    async createNewTask(newTask){
        return await httpAuth.post('/tasks/', newTask)
    }

    async getTask(taskId){
        return await httpAuth.get(`/tasks/${taskId}`)
    }

    async updateTask(taskId, taskUpdate){
        return await httpAuth.put(`/tasks/${taskId}`, taskUpdate)
    }

    async deleteTask(taskId){
        return await httpAuth.delete(`/tasks/${taskId}`)
    }
}

export default new TaskDataService();