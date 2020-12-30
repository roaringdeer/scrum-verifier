<template>
    <div class="content">
        <Button :rounded="true" class="floater-left p-button-rounded" @click="openEditUserDialog" icon="pi pi-cog"></Button>
            <div :key="avatarKey">
                <Avatar
                    v-if="profile.image"
                    class="big-avatar"
                    shape="circle"
                    size="xlarge"
                    :image="'http://localhost:8000/api/files/' + profile.image"
                />
                <Avatar
                    v-else
                    :label="profile.username[0].toUpperCase()"
                    class="big-avatar"
                    size="xlarge"
                    shape="circle"
                    style="margin-bottom: 10px;"
                />
            </div>
            <FileUpload
                ref="fileUpload"
                mode="basic"
                accept="image/*"
                :customUpload="true"
                @uploader="avatarUploader"
                :auto="true"
                chooseLabel="Upload avatar"
            />
        <div>
            <Divider align="left" type="dashed">
                <b>Username</b>
            </Divider>
            {{profile.username}}
            <Divider align="left" type="dashed">
                <b>Full Name</b>
            </Divider>
            <div v-if="profile.full_name">
                {{profile.full_name}}
            </div>
            <div v-else style="font-style: italic;">
                What's your real name though?
            </div>
            <Divider align="left" type="dashed">
                <b>E-Mail</b>
            </Divider>
            {{profile.email}}
            <Divider align="left" type="dashed">
                <b>Phone Number</b>
            </Divider>
            <div v-if="profile.phone_number">
                {{profile.phone_number}}
            </div>
            <div v-else style="font-style: italic;">
                Add your phone number maybe?
            </div>
            <Divider align="left" type="dashed">
                <b>Bio</b>
            </Divider>
            <div v-if="profile.bio">
                {{profile.bio}}
            </div>
            <div v-else style="font-style: italic;">
                Let everyone know who you are!
            </div>
        </div>
        <Dialog :header="toUpdate?.username" v-model:visible="editUserDialog" style="width: 500px">
            <Divider align="left" type="dashed">
                Full Name
            </Divider>
                <InputText v-model="toUpdate.full_name" style="float: left; width: 80%;"/>
                <br/>
                <small v-if="!validFullName" class="p-invalid" style="float: left;">
                    Invalid full name.
                </small>

            <Divider align="left" type="dashed">
                E-Mail
            </Divider>
            <InputText v-model="toUpdate.email" style="float: left; width: 80%;"/>
            <br/>
            <small v-if="!validEmail" class="p-invalid" style="float: left;">
                E-Mail is invalid.
            </small>

            <Divider align="left" type="dashed">
                Phone Number
            </Divider>
                <InputText v-model="toUpdate.phone_number" style="float: left; width: 80%;"/>
                <br/>
                <small v-if="!validPhoneNumber" class="p-invalid" style="float: left;">
                    Phone number is invalid.
                </small>

            <Divider align="left" type="dashed">
                Bio
            </Divider>
                <Textarea v-model="toUpdate.bio" rows="5" cols="30" :autoResize="true" style="float: left; width: 80%;"/>
            <template #footer>
                <Button label="Cancel" icon="pi pi-times" class="p-button-text" @click="closeEditUserDialog"/>
                <Button label="Save" icon="pi pi-check" class="p-button-text" @click="editUser" />
            </template>
        </Dialog>
    </div>
</template>

<script>
import LocalStorageDataService from '../services/LocalStorageDataService'
import UserDataService from '../services/UserDataService'
import ProfileDataService from '../services/ProfileDataService'
import FileDataService from '../services/FileDataService'

export default {
    events: ['edit'],
    data(){
        return{
            editUserDialog: false,
            toUpdate: null,
            avatarKey: 0
        }
    },
    async setup(){
        const user = LocalStorageDataService.getUser()
        const profile = user.profile
        return {
            profile
        }
    },
    computed: {
        validUsername: function (){
            if (!this.toUpdate.username){
                return false
            }
            var re = /^[a-zA-Z0-9_-]+$/;
            return re.test(this.toUpdate?.username);
        },
        validEmail: function (){
            if (!this.toUpdate.email){
                return false
            }
            var re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
            return re.test(this.toUpdate?.email);
        },
        validFullName: function (){
            if (!this.toUpdate?.full_name){
                return true
            }
            var re = /^[a-zA-Z\s]+$/;
            return re.test(this.toUpdate?.full_name);
        },
        validPhoneNumber: function (){
            if (!this.toUpdate?.phone_number){
                return true
            }
            var re = /^\+?[0-9\s]+$/;
            return re.test(this.toUpdate?.phone_number);
        },
    },
    methods:{
        async avatarUploader(event){
            try{
                const file = event.files[0]
                const response = await FileDataService.uploadAvatar(file)
                this.$refs.fileUpload.clear()
                this.profile.image = response?.data.filename
                var user = LocalStorageDataService.getUser()
                user.profile.image = response?.data.filename
                LocalStorageDataService.setUser(user)
                this.avatarKey += 1
            }
            catch(error){
                alert(error.message)
            }
        },
        openEditUserDialog(){
            this.editUserDialog = true
            this.toUpdate = {...this.profile}
            console.log(this.toUpdate)
        },
        async editUser(){
            try{
                await ProfileDataService.updateProfile({
                    profile_update: {
                        ...this.toUpdate
                    }
                })
                const userRes = await UserDataService.updateCurrentUser({
                    user_update: {
                        email: this.toUpdate.email,
                        username: this.toUpdate.username
                }
                })
                const updatedUser = userRes?.data
                console.log(updatedUser)
                this.profile = updatedUser.profile
                this.toUpdate = null
                console.log(this.profile)
                LocalStorageDataService.setUser(updatedUser)
                this.closeEditUserDialog()
            }
            catch(error){
                if (error.response) {
                    alert(error.response.data.detail);
                } else if (error.request) {
                    alert(error.request);
                } else {
                    alert(error.message);
                }
            }
        },
        closeEditUserDialog(){
            this.toUpdate = null
            this.editUserDialog = false
        }
    }
}
</script>

<style>
.big-avatar.p-avatar-xl{
  width: 8rem;
  height: 8rem;
  font-size: 4rem;
}

.floater-left{
	position:fixed;
	bottom:40px;
	left:40px;
}
</style>