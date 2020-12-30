<template>
    <div class="content">
        <div>
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
                None
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
                None
            </div>
            <Divider align="left" type="dashed">
                <b>Bio</b>
            </Divider>
            <div v-if="profile.bio">
                {{profile.bio}}
            </div>
            <div v-else style="font-style: italic;">
                None
            </div>
        </div>
    </div>
</template>

<script>
import ProfileDataService from '../services/ProfileDataService'
import {useRoute} from 'vue-router'

export default {
    async setup(){
        const route = useRoute()
        const profile = (await ProfileDataService.getProfile(route.params.username))?.data
        console.log(profile)
        return{
            profile
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