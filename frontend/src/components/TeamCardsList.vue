<template>
    <div>
        <div class="p-grid p-jc-center" style="margin-bottom: 20px;">
            
            <span class="p-input-icon-left project-search">
                <i class="pi pi-search" />
                <InputText type="text" v-model="search" placeholder="Search" />
            </span>
            <Button class="p-ml-2" @click="visibleLeft = true">
                <i class="pi pi-filter" />
            </Button>
        </div>
        <div class="p-grid p-jc-center">
            <div v-for="team in filteredAndSearchedTeams()" :key="team.id">
                <div class="p-col-12 p-sm-12 p-md-6 p-lg-3 p-mx-2 p-jc-center">
                    <TeamCard
                        :team="team"
                        @edit="openEditTeamDialog(team)"
                        @goto="gotoTeam(team)"
                    />
                </div>
            </div>
        </div>
        <Sidebar v-model:visible="visibleLeft">
            Filters
            <Divider>
                Team activity
            </Divider>
            <div class="p-field-radiobutton">
                <RadioButton value="all" v-model="teamActivitySelection" />
                <label>All</label>
            </div>
            <div class="p-field-radiobutton">
                <RadioButton value="active" v-model="teamActivitySelection" />
                <label>Active</label>
            </div>
            <div class="p-field-radiobutton">
                <RadioButton value="archived" v-model="teamActivitySelection" />
                <label>Archived</label>
            </div>
        </Sidebar>
        
        <Dialog header="Create new team" :modal="true" v-model:visible="createTeamDialog">
            <Divider>
                Name
            </Divider>
                <InputText v-model="teamToCreate.name" style="float: left; width: 80%"/>
            <Divider>
                Description
            </Divider>
            <Textarea v-model="teamToCreate.description" rows="5" cols="30" :autoResize="true" style="float: left;  width: 80%"/>
            <template #footer>
                <Button label="Cancel" icon="pi pi-times" class="p-button-text" @click="closeCreateTeamDialog"/>
                <Button label="Create" icon="pi pi-check" class="p-button-text" @click="createTeam" />
            </template>
        </Dialog>

        <Dialog header="Edit team" :contentStyle="{overflow: 'visible'}" :modal="true" v-model:visible="editTeamDialog">
        <Divider>
            Name
        </Divider>
        <InputText v-model="selectedTeam.name" style="float: left; width: 80%;"/>
        <Divider>
            Description
        </Divider>
        <Textarea v-model="selectedTeam.description" rows="5" cols="30" :autoResize="true" style="float: left; width: 80%;"/>
        <template #footer>
            <Button label="Delete" icon="pi pi-trash" class="p-button-text" @click="openDeleteTeamDialog" style="float: left;"/>
            <Button label="Cancel" icon="pi pi-times" class="p-button-text" @click="closeEditTeamDialog"/>
            <Button label="Save" icon="pi pi-check" class="p-button-text" @click="editSelectedTeam" />
        </template>
        </Dialog>
        
        <Dialog header="Confirmation" v-model:visible="deleteTeamDialog" :style="{width: '350px'}" :modal="true">
        <div class="confirmation-content">
            <i class="pi pi-exclamation-triangle p-mr-3" style="font-size: 2rem" />
            <span>Are you sure you want to proceed?</span>
        </div>
        <template #footer>
            <Button label="No" icon="pi pi-times" @click="closeDeleteTeamDialog" class="p-button-text" autofocus/>
            <Button label="Yes" icon="pi pi-check" @click="deleteSelectedTeam" class="p-button-text"/>
        </template>
        </Dialog>

        <Button
            class="create-floater-right p-button-rounded"
            icon="pi pi-plus"
            @click="openCreateTeamDialog"
            :rounded="true"
        />
    </div>
    
</template>

<script>
import useTeams from '../store/teams'
import useTasks from '../store/tasks'
import useEvents from '../store/events'
import useMembers from '../store/members'
import useProjects from '../store/projects'
import TeamDataService from '../services/TeamDataService'
import MemberDataService from '../services/MemberDataService'

export default {
    data(){
        return{
            visibleLeft: false,
            search: '',
            teamActivitySelection: 'all',
            editTeamDialog: false,
            selectedTeam: {
                name: null,
                description: null
            },
            createTeamDialog: false,
            teamToCreate: {
                name: null,
                description: null
            },
            deleteTeamDialog: false
        }
    },
    async setup(){
        const {setProjects} = useProjects()
        const {teams, setTeams, setSelectedTeam, pushTeam, editTeam, deleteTeam} = useTeams()
        const {getTasks, clearTasks} = useTasks()
        const {setMembers} = useMembers()
        const {getEvents} = useEvents()
        // await setProjects((await ProjectDataService.getAllUserProjects())?.data)
        await setTeams((await TeamDataService.getAllUserTeams())?.data)
        return {
            teams,
            pushTeam,
            editTeam,
            deleteTeam,
            setSelectedTeam,
            getTasks,
            clearTasks,
            setMembers,
            getEvents,
            setProjects
        }
    },
    methods:{
        async gotoTeam(team){
            console.log((await TeamDataService.getTeamProjects(team.id))?.data)
            await this.setProjects((await TeamDataService.getTeamProjects(team.id))?.data)
            await this.setMembers((await MemberDataService.getAllTeamMembers(team.id))?.data)
            await this.setSelectedTeam(team)
            this.$router.push('/teams/view')
        },
        async goBack(){
            this.viewProject = false
            await this.setSelectedProject(null)
            await this.clearTasks()
            await this.setMembers(null)
        },
        filteredAndSearchedTeams(){
            var searched = [];
            if (this.search == ''){
                searched = this.teams
            }
            else{
                searched = this.searchTeams(this.teams, this.search);
            }
            return searched
            // var filtered = [];
            // filtered = this.filterTeamsIsArchived(searched, this.teamActivitySelection)
            // return filtered
        },
        searchTeams(arr, query) {
            return arr.filter(function(el) {
                return el.name.toLowerCase().indexOf(query.toLowerCase())> -1 || el.description?.toLowerCase().indexOf(query.toLowerCase())>-1
            })
        },
        // filterTeamsIsArchived(arr, query){
        //     return arr.filter(function(el) {
        //         return query!='active' && el.is_archived || query!='archived' && !el.is_archived
        //     })
        // },
        openCreateTeamDialog(){
            this.createTeamDialog = true
        },
        async createTeam(){
            var createdTeam = (await TeamDataService.createNewTeam({
                new_team: {
                    name: this.teamToCreate.name,
                    description: this.teamToCreate.description
                }
            }))?.data

            await this.pushTeam(createdTeam)
            this.closeCreateTeamDialog()
        },
        closeCreateTeamDialog(){
            this.createTeamDialog = false
        },
        openEditTeamDialog(team){
            this.selectedTeam = {...team}
            this.editTeamDialog = true
        },
        async editSelectedTeam(){
            await TeamDataService.updateTeam(
                this.selectedTeam.id,
                {
                    team_update: this.selectedTeam
                }
            )
            await this.editTeam(this.selectedTeam)
            this.closeEditTeamDialog()
        },
        closeEditTeamDialog(){
            this.selectedTeam = null
            this.editTeamDialog = false
        },
        openDeleteTeamDialog(){
            this.deleteTeamDialog = true
        },
        async deleteSelectedTeam(){
            await TeamDataService.deleteTeam(this.selectedTeam.id)
            await this.deleteTeam(this.selectedTeam)
            this.closeEditTeamDialog()
            this.closeDeleteTeamDialog()
        },
        closeDeleteTeamDialog(){
            this.selectedTeam = null
            this.deleteTeamDialog = false
        }
    }
}
</script>

<style>
.project-search{
    margin-top: 10px;
}
.shown-dropdown{
    width: 120px;
    margin-left: 10px;
    margin-top: 10px;
}
.back-button{
    float: left;
    overflow: auto;
    width: auto;
}
.content-body{
    padding-top: 50px;
    /* height: 80vh; */
    margin-bottom: 5vh;
}
</style>