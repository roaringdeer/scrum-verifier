import {httpAuthFiles} from '../http-common'

class FileDataService{
    async uploadAvatar(file){
        let formData = new FormData()
        formData.append('file', file)
        return await httpAuthFiles.post('/files/avatar/', formData)
    }
}

export default new FileDataService();