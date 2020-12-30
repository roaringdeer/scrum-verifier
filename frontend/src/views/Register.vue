<template>
    <div class="p-d-flex p-jc-center p-ai-center p-flex-column">
        <BlockUI :blocked="loading" :fullScreen="true"></BlockUI>
        <Card style="width: 400px">
            <template #title>
                Sign Up
            </template>
            <template #content>
            <div class="p-mb-2 p-jc-center p-ai-center">
                <div class="p-inputgroup" style="width: 368px; margin-bottom: 10px">
                    <span class="p-inputgroup-addon">
                        <i class="pi pi-envelope"></i>
                    </span>
                    <InputText placeholder="E-Mail" v-model="email" />
                </div>
                <div class="p-inputgroup" style="width: 368px; margin-bottom: 10px">
                    <span class="p-inputgroup-addon">
                        <i class="pi pi-user"></i>
                    </span>
                    <InputText placeholder="Username" v-model="username" />
                </div>
                <div class="p-inputgroup p-as-center" style="width: 368px">
                    <span class="p-inputgroup-addon">
                        <i class="pi pi-lock"></i>
                    </span>
                    <InputText placeholder="Password" type="password" v-model="password"/>
                </div>
            </div>
                <Button icon="pi pi-info-circle" label='Register' @click="registerButtonPressed">
                </Button>
            </template>
        </Card>
        <Card style="width: 400px; margin-top: 20px">
            <template #content>
                Already registered? <a href="/login">Log in here!</a>
            </template>
        </Card>
    </div>    
</template>

<script>
import AuthService from '../services/AuthService'
export default {
    data () {
        return{
            email: "",
            username: "",
            password: "",
        }
    },
    setup () {

    },
    methods: {
        registerButtonPressed () {
            AuthService.registerUser(this.email, this.username, this.password)
            this.$router.push('/login');
        }
    }
}

</script>

<style>

</style>