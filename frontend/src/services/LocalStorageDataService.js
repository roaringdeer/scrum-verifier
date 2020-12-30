
const ACCESS_TOKEN_KEY = 'authToken'
const USER_KEY = 'user'

class LocalStorageDataService{

    setUser(user){
        localStorage.setItem(USER_KEY, JSON.stringify(user));
    }

    getUser(){
        return JSON.parse(localStorage.getItem(USER_KEY));
    }

    clearUser(){
        localStorage.removeItem(USER_KEY);
    }

    getAccessToken(){
        return localStorage.getItem(ACCESS_TOKEN_KEY);
    }

    setAccessToken(accessToken){
        localStorage.setItem(ACCESS_TOKEN_KEY, accessToken)
    }

    clearAccessToken(){
        localStorage.removeItem(ACCESS_TOKEN_KEY)
    }
}

export default new LocalStorageDataService();