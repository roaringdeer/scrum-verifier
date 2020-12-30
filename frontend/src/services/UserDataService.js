import {httpAuth} from '../http-common'

class UserDataService{
    async updateCurrentUser(userToUpdate){
        return await httpAuth.put('/users/me', userToUpdate)
    }
}

export default new UserDataService();