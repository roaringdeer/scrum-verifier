<template>
    <div class="p-d-flex p-jc-center p-ai-center p-flex-column">
        <!-- <BlockUI :blocked="loading" :fullScreen="true"></BlockUI> -->
        <Card style="width: 400px">
            <template #title>
                Log in 
            </template>
            <template #content>
            <div class="p-mb-2 p-jc-center p-ai-center">
                <div class="p-inputgroup" style="width: 368px; margin-bottom: 10px">
                    <span class="p-inputgroup-addon">
                        <i class="pi pi-user"></i>
                    </span>
                    <InputText placeholder="E-Mail" v-model="username" />
                </div>
                <div class="p-inputgroup p-as-center" style="width: 368px">
                    <span class="p-inputgroup-addon">
                        <i class="pi pi-lock"></i>
                    </span>
                    <InputText placeholder="Password" type="password" v-model="password"/>
                </div>
            </div>
            <Button icon="pi pi-info-circle" label='Log In' @click="loginButtonPressed"/>
            </template>
        </Card>
        <Card style="width: 400px; margin-top: 20px">
            <template #content>
                New to us? <a href="/register">Sign Up!</a>
            </template>
        </Card>
    </div>    
</template>

<script>
import LocalStorageDataService from '../services/LocalStorageDataService'
import AuthService from '../services/AuthService'

export default {
    data () {
        return{
            username: "",
            password: ""
        }
    },
    setup () {
        const accessToken = LocalStorageDataService.getAccessToken();
        return {
            accessToken
        }
    },
    methods: {
        async loginButtonPressed () {
            try {
                if(await AuthService.loginUser(this.username, this.password)){
                    this.$router.push('/');
                    window.location.reload();
                }
                else{
                    this.username = "";
                    this.password = "";
                }
            }
            catch (err) {
                alert(`Error <Login.vue>: ${err}`);
            }
            
        }
    }
}

</script>

<style>

</style>