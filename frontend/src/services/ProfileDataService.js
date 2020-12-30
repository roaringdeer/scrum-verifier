import {httpAuth} from "../http-common";

class ProfileDataService{
    async getProfile(username){
        return await httpAuth.get(`/profiles/${username}`)
    }

    async updateProfile(profileUpdate){
        return await httpAuth.put('/profiles/me', profileUpdate)
    }
}

export default new ProfileDataService();