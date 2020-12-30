import decode from 'jwt-decode'
import axios from 'axios';
import LocalStorageDataService from './LocalStorageDataService'


class AuthService{
    async registerUser(email, username, password){
        LocalStorageDataService.clearAccessToken()
        try{
            const res = await axios({
                method: `POST`,
                url: `http://localhost:8000/api/users/`,
                data: { new_user: { username, email, password } },
                headers: {
                    "Content-Type": "application/json",
                },
            })
            console.log('a', res)
            
        }
        catch(error){
            console.log('(a')
            console.log(`${error}`)
        }
    }

    async loginUser(username, password){
        LocalStorageDataService.clearAccessToken()
        const formData = new FormData()
        formData.set("username", username)
        formData.set("password", password)
        // set the request headers
        const headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        // make the actual HTTP request to our API
        try{
            const res = await axios({
                method: `POST`,
                url: `http://localhost:8000/api/users/login/token/`,
                data: formData,
                headers,
            })
            console.log(res)
            LocalStorageDataService.setAccessToken(res?.data?.access_token)
            await this.currentUser()
            return true
        }
        catch(err){
            console.log(`${err}`)
        }
    }

    async logoutUser(){
        LocalStorageDataService.clearAccessToken()
        LocalStorageDataService.clearUser()
    }
    
    async currentUser(){
        const headers = {
            "Content-Type": "application/json",
            Authorization: `Bearer ${LocalStorageDataService.getAccessToken()}`
        }
        try {
            const res = await axios({
                method: `GET`,
                url: `http://localhost:8000/api/users/me/`,
                headers
            })
            console.log(res)
            LocalStorageDataService.setUser(res?.data)
        }
        catch(err){
            alert(err)
        }
    }

    getTokenExpirationDate(encodedToken) {
        let token = decode(encodedToken)
        if (!token.exp) {
            return null
        }
      
        let date = new Date(0)
        date.setUTCSeconds(token.exp)
      
        return date
    }

    isLoggedIn() {
        let authToken = LocalStorageDataService.getAccessToken()
        return !!authToken && !this.isTokenExpired(authToken)
    }

    isTokenExpired(token) {
        let expirationDate = this.getTokenExpirationDate(token)
        return expirationDate < new Date()
    }
}

export default new AuthService();