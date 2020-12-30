import {httpAuth} from "../http-common";

class MemberDataService{
    async getAllTeamMembers(teamId){
        return await httpAuth.get(`/teams/${teamId}/members`)
    }

    async createNewMember(teamId, newMember){
        return await httpAuth.post(`/teams/${teamId}/members`, newMember)
    }

    async getMemberForUser(teamId, username){
        return await httpAuth.get(`/teams/${teamId}/members/${username}`)
    }

    async updateMember(teamId, username, memberUpdate){
        return await httpAuth.put(`/teams/${teamId}/members/${username}`, memberUpdate)
    }

    async deleteMember(teamId, username){
        return await httpAuth.delete(`/teams/${teamId}/members/${username}`)
    }
}

export default new MemberDataService();