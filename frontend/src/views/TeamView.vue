<template>
    <div class="content">
        <div v-if="error"> 
            <SomethingWentWrong @back="backToTeams" />
        </div>
        <Suspense v-else>
            <template #default>
                <TeamTabs />
            </template>
            <template #fallback>
                <ProgressSpinner/>
            </template>
        </Suspense>
    </div>
</template>

<script>
import useTeams from '../store/teams'
import { onErrorCaptured, ref } from 'vue'

export default {
    data(){
        return{
            visibleLeft: false,
        }
    },
    setup(){
        const {selectedTeam} = useTeams()
        const error = ref(null)
        onErrorCaptured(e => {
            error.value = e
            // console.log(error)
            return true
        })
        
        return{
            error,
            selectedTeam
        }
    },
    methods: {
        openSidebar(){
            this.visibleLeft = true
        },
        backToTeams(){
            this.$router.push('/teams')
        }
    }
}
</script>

<style>

</style>