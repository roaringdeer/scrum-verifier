<template>
    <Card class="member-card tasks-border" style="width: 20rem;" >
        <template #header>
            <div class="avatar">
                <Avatar
                    v-if="member?.profile.image"
                    :image="'http://localhost:8000/api/files/' + member?.profile.image"
                    size="xlarge" shape="circle"
                    style="cursor: pointer;"
                    @click="gotoMember"
                />
                <Avatar
                    v-else
                    :label="member.profile.username[0].toUpperCase()"
                    size="xlarge"
                    shape="circle"
                    style="cursor: pointer;"
                    @click="gotoMember"
                />
            </div>
        </template>
        <template #title>
            <div v-if="member?.profile.fullname" style="cursor: pointer;" @click="gotoMember">
                {{member?.profile.fullname}}
            </div>
            <div v-else style="cursor: pointer;" @click="gotoMember">
                {{member?.profile.username}}
            </div>
        </template>
        <template #subtitle>
            <div v-if="member?.profile.fullname">
                {{member?.profile.username}}
            </div>
        </template>
        <template #content>
            {{member?.profile.bio}}
        </template>
        <template #footer>
        </template>
    </Card>
</template>

<script>
export default {
    props: ['member'],
    data(){
        return{
            
        }
    },
    setup(){

    },
    methods: {
        gotoMember(){
            this.$router.push(`/user/${this.member.profile.username}`)
        }

    }
}
</script>

<style>
.member-card .p-card-header{
    height: 120px;
}
.avatar{
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>