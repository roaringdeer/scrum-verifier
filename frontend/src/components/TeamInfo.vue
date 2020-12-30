<template>
    <div>
        <h4>{{selectedTeam.name}}</h4>
        <h5>{{selectedTeam.description}}</h5>
    </div>
</template>

<script>
import useTeams from '../store/teams'
export default {
    async setup(){
        const {selectedTeam} = useTeams()
        return{
            selectedTeam
        }
    }
}
</script>

<style>

</style>