<template>
    <div class="p-grid p-jc-center">
        <div v-for="member in members" :key="member.id">
            <div class="p-col-12 p-sm-12 p-md-6 p-lg-3 p-mx-2 p-jc-center">
                <MemberCard :member="member" />
            </div>
        </div>
    </div>
</template>

<script>
import useMembers from '../store/members'
export default {
    async setup(){
        const { members } = useMembers()
        return{
            members
        }
    }
}
</script>

<style>

</style>