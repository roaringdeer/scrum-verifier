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
            <div v-for="project in filteredAndSearchedProjects()" :key="project.id">
                <div class="p-col-12 p-sm-12 p-md-6 p-lg-3 p-mx-2 p-jc-center">
                    <ProjectCard
                        :project="project"
                        :team="Object.values(teams).filter(t => t.id == project.team_id)[0]?.name"
                        :progress="progress(project.id)"
                        @goto="gotoProject(project)"
                    />
                </div>
            </div>
        </div>

        <Sidebar v-model:visible="visibleLeft">
            Filters
            <Divider>
                Project activity
            </Divider>
            <div class="p-field-radiobutton">
                <RadioButton value="all" v-model="projectActivitySelection" />
                <label>All</label>
            </div>
            <div class="p-field-radiobutton">
                <RadioButton value="active" v-model="projectActivitySelection" />
                <label>Active</label>
            </div>
            <div class="p-field-radiobutton">
                <RadioButton value="archived" v-model="projectActivitySelection" />
                <label>Archived</label>
            </div>
            <Divider>
                Teams
            </Divider>
            <div v-for="team of teams" :key="team.id" class="p-field-checkbox">
                <Checkbox :id="team.key" name="team" :value="team" v-model="selectedTeams"/>
                <label :for="team.key">{{team.name}}</label>
            </div>
        </Sidebar>
    </div>
</template>

<script>
import useProjects from '../store/projects'
import useTeams from '../store/teams'
import useTasks from '../store/tasks'
import useEvents from '../store/events'
import useMembers from '../store/members'
import ProjectDataService from '../services/ProjectDataService'
import TeamDataService from '../services/TeamDataService'
import MemberDataService from '../services/MemberDataService'

export default {
    data(){
        return{
            visibleLeft: false,
            search: '',
            projectButtonOptions: [
                {label: 'Update'},
                {label: 'Delete'}
            ],
            projectActivitySelection: 'all',
            selectedTeams: this.teams,
            tasksEventSource: null
        }
    },
    async setup(){
        const {projects, setProjects, getProjectProgress, selectedProject, setSelectedProject} = useProjects()
        const {teams, setTeams} = useTeams()
        const {getTasks, clearTasks} = useTasks()
        const {setMembers} = useMembers()
        const {getEvents} = useEvents()
        await setProjects((await ProjectDataService.getAllUserProjects())?.data)
        await setTeams((await TeamDataService.getAllUserTeams())?.data)
        return {
            projects,
            teams,
            setSelectedProject,
            selectedProject,
            getTasks,
            clearTasks,
            setMembers,
            getProjectProgress,
            getEvents
        }
    },
    methods:{
        progress(projectId){
            return this.getProjectProgress(projectId)
        },
        async gotoProject(project){
            await this.setSelectedProject(project)
            await this.getTasks(project.id)
            await this.setMembers((await MemberDataService.getAllTeamMembers(project.team_id))?.data)
            await this.getEvents(project.id)
            this.$router.push('/projects/view')
        },
        async goBack(){
            await this.setSelectedProject(null)
            await this.clearTasks()
            await this.setMembers(null)
            
        },
        filteredAndSearchedProjects(){
            var searched = [];
            var filtered = [];
            if (this.search == ''){
                searched = this.projects
            }
            else{
                searched = this.searchProjects(this.projects, this.search);
            }
            filtered = this.fiterProjectsInTeam(
                this.filterProjectsIsArchived(searched, this.projectActivitySelection),
                this.selectedTeams
            )
            return filtered
        },
        searchProjects(arr, query) {
            return arr.filter(function(el) {
                return el.name.toLowerCase().indexOf(query.toLowerCase())> -1 || el.description?.toLowerCase().indexOf(query.toLowerCase())>-1
            })
        },
        filterProjectsIsArchived(arr, query){
            return arr.filter(function(el) {
                return query!='active' && el.is_archived || query!='archived' && !el.is_archived
            })
        },
        fiterProjectsInTeam(arr, query){
            return arr.filter(function(el) {
                for(var q of query){
                    if (el.team_id == q.id){
                        return true;
                    }
                }
                return false
            })
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