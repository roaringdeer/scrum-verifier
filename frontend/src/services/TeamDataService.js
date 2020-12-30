import {httpAuth} from "../http-common";

class TeamDataService{
    async getAllUserTeams(){
        return await httpAuth.get('/teams/')
    }

    async createNewTeam(newTeam){
        return await httpAuth.post('/teams/', newTeam)
    }

    async getTeam(teamId){
        return await httpAuth.get(`/teams/${teamId}`)
    }

    async getTeamProjects(teamId){
        return await httpAuth.get(`/teams/${teamId}/projects`)
    }

    async updateTeam(teamId, teamUpdate){
        return await httpAuth.put(`/teams/${teamId}`, teamUpdate)
    }

    async deleteTeam(teamId){
        return await httpAuth.delete(`/teams/${teamId}`)
    }
}

export default new TeamDataService();