<template>
    <div>
        <div v-if="!!teams">
            <Listbox v-model="focusedTeam" :options="teams" optionLabel="name" @change="changeState"/>
            <!-- <Listbox v-model="selectedTeam" :options="teams" optionLabel="name"/> -->
        </div>
        <Button label="Create new team" style="margin-top: 15px" @click="openCreateTeamDialog"/>
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
import TeamDataSercive from '../services/TeamDataService'
import MemberDataService from '../services/MemberDataService'
import useTeams from '../store/teams'
import useProjects from '../store/projects'
import useMembers from '../store/members'

export default {
    data(){
        return{
            createTeamDialog: false,
            listboxKey: 0,
            newTeamName: null,
            newTeamDesc: null,
            focusedTeam: null
        }
    },
    async setup(){
        const {teams, setTeams, selectedTeam, setSelectedTeam, pushTeam} = useTeams();
        const {setProjects} = useProjects()
        const {setMembers} = useMembers()
        const teamsResponse = await TeamDataSercive.getAllUserTeams()
        await setTeams(teamsResponse?.data)
        return{
            teams,
            selectedTeam,
            setTeams,
            setSelectedTeam,
            pushTeam,
            setProjects,
            setMembers
        }
    },
    methods:{
        async changeState(){
            await this.setSelectedTeam(this.focusedTeam)
            if(this.focusedTeam){
                await this.setProjects(
                    (await TeamDataSercive.getTeamProjects(this.focusedTeam.id))?.data
                )
                await this.setMembers(
                    (await MemberDataService.getAllTeamMembers(this.focusedTeam.id))?.data
                )
            }
        },
        openCreateTeamDialog(){
            this.createTeamDialog = true;
        },
        async createTeam(){
            const newTeamResponse = await TeamDataSercive.createNewTeam({
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