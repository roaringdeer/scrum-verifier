import {httpAuth} from "../http-common";

class ProjectDataService{
    async getAllUserProjects(){
        return await httpAuth.get('/projects/')
    }

    async createNewProject(newProject){
        return await httpAuth.post('/projects/', newProject)
    }

    async getProject(projectId){
        return await httpAuth.get(`/projects/${projectId}`)
    }

    async updateProject(projectId, projectUpdate){
        return await httpAuth.put(`/projects/${projectId}`, projectUpdate)
    }

    async deleteProject(projectId){
        return await httpAuth.delete(`/projects/${projectId}`)
    }

    async getBurndownChartData(projectId){
        return await httpAuth.get(`/projects/${projectId}/chart`)
    }
}

export default new ProjectDataService();