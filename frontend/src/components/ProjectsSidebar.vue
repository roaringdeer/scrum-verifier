<template>
    <div> 
        <Dialog header="Create new team" :modal="true" v-model:visible="createTeamDialog">
            <div class="p-inputgroup" style="margin-bottom: 10px">
                <span class="p-inputgroup-addon">Team name</span>
                <InputText v-model="newTeamName"/>
            </div>
            <div class="p-inputgroup" style="margin-bottom: 10px">
                <span class="p-inputgroup-addon">Team name</span>
                <Textarea v-model="newTeamDesc" rows="5" cols="30" :autoResize="true"/>
            </div>
            <template #footer>
                <Button label="Cancel" icon="pi pi-times" class="p-button-text" @click="closeCreateTeamDialog"/>
                <Button label="Create" icon="pi pi-check" class="p-button-text" @click="createTeam" />
            </template>
        </Dialog>
    </div>
</template>

<script>
import TeamDataService from '../services/TeamDataService'
import ProjectDataService from '../services/ProjectDataService'
// import MemberDataService from '../services/MemberDataService'
// import useTeams from '../store/teams'
import useProjects from '../store/projects'
// import useMembers from '../store/members'

export default {
    data(){
        return{
            createTeamDialog: false,
            listboxKey: 0,
            newTeamName: null,
            newTeamDesc: null,
            focusedProject: null
        }
    },
    async setup(){
        const {projects, setProjects} = useProjects()
        // const {setMembers} = useMembers()
        // const teamsResponse = await TeamDataService.getAllUserTeams()
        const projectsResponse = await ProjectDataService.getAllUserProjects()
        await setProjects(projectsResponse?.data)
        return{
            setProjects,
            projects
        }
    },
    methods:{
        async changeState(){
            // await this.setSelectedTeam(this.focusedTeam)
            // if(this.focusedTeam){
            //     await this.setProjects(
            //         (await TeamDataService.getTeamProjects(this.focusedTeam.id))?.data
            //     )
            //     await this.setMembers(
            //         (await MemberDataService.getAllTeamMembers(this.focusedTeam.id))?.data
            //     )
            // }
        },
        openCreateTeamDialog(){
            this.createTeamDialog = true;
        },
        async createTeam(){
            const newTeamResponse = await TeamDataService.createNewTeam({
                new_team: {
                    name: this.newTeamName,
                    description: this.newTeamDesc
                }
            });
            this.closeCreateTeamDialog();
            this.pushTeam(newTeamResponse?.data)
            await this.setSelectedTeam(newTeamResponse?.data)
        },
        closeCreateTeamDialog(){
            this.createTeamDialog = false;
        }
    }
}
</script>

<style>

</style>