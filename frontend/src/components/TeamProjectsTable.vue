<template>
    <div class="card">
        <DataTable
            :value="projects"
            :paginator="true"
            :rows="10"
            dataKey="id"
            :rowHover="true"
            :filters="filters"
            :loading="loading"
            paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
            :rowsPerPageOptions="[10,25,50]"
            currentPageReportTemplate="Showing {first} to {last} of {totalRecords} entries">
            <template #header>
                <div class="table-header">
                    Projects
                    <span>
                        <Button class="p-mr-2" label="Create new project" @click="openCreateProjectDialog"/>
                        <span class="p-input-icon-left">
                            <i class="pi pi-search" />
                            <InputText v-model="filters['global']" placeholder="Search" />
                        </span>
                    </span>
                </div>
            </template>
            <template #empty>
                No projects found.
            </template>
            <template #loading>
                Loading projects
            </template>
            <Column :sortable="true" field="name" header="Name"></Column>
            <Column :sortable="true" field="description" header="Description"></Column>
            <Column :sortable="true" field="is_archived" header="Archived"></Column>
            <Column :sortable="true" field="is_archived" header="Progress">
                <template #body="slotProps">
                    <ProgressBar :value="getProjectProgress(slotProps.data.id)"/>
                </template>
            </Column>

            <Column headerStyle="width: 10rem; text-align: center" bodyStyle="text-align: center; overflow: visible">
                <template #body="slotProps">
                    <span class="p-buttonset">
                        <Button type="button" icon="pi pi-trash" class="p-button-danger" @click="openDeleteProjectDialog(slotProps.data)" ></Button>
                        <Button type="button" icon="pi pi-pencil" class="p-button-warning" @click="openEditProjectDialog(slotProps.data)" ></Button>
                        <Button type="button" icon="pi pi-angle-right" class="p-button-success" @click="gotoProject(slotProps.data)" ></Button>
                    </span>
                </template>
            </Column>
        </DataTable>

        <Dialog header="Create new project" :modal="true" v-model:visible="createProjectDialog">
            <Divider>
                Project name
            </Divider>
            <InputText v-model="projectName"  style="float: left;  width: 80%"/>
            <Divider>
                Project description
            </Divider>
            <Textarea v-model="projectDesc" rows="5" cols="30" :autoResize="true" style="float: left;  width: 80%"/>
            <template #footer>
                <Button label="Cancel" icon="pi pi-times" class="p-button-text" @click="closeCreateProjectDialog"/>
                <Button label="Save" icon="pi pi-check" class="p-button-text" @click="createProject" />
            </template>
        </Dialog>

        <Dialog header="Edit project" :modal="true" v-model:visible="editProjectDialog">
            <Divider>
                Project name
            </Divider>
            <InputText v-model="project.name"  style="float: left;  width: 80%"/>
            <Divider>
                Project description
            </Divider>
            <Textarea v-model="project.description" rows="5" cols="30" :autoResize="true" style="float: left;  width: 80%"/>
            <template #footer>
                <Button label="Cancel" icon="pi pi-times" class="p-button-text" @click="closeEditProjectDialog"/>
                <Button label="Save" icon="pi pi-check" class="p-button-text" @click="editProject" />
            </template>
        </Dialog>
        
        <Dialog header="Delete project" v-model:visible="deleteProjectDialog" :style="{width: '350px'}" :modal="true">
            <div class="delete-confirmation-content">
                <i class="pi pi-exclamation-triangle p-mr-3" style="font-size: 2rem" />
                <span>Are you sure you want to delete {{project.name}}?</span>
            </div>
            <template #footer>
                <Button label="No" icon="pi pi-times" @click="closeDeleteProjectDialog" class="p-button-text"/>
                <Button label="Yes" icon="pi pi-check" @click="deleteProject" class="p-button-text" autofocus />
            </template>
        </Dialog>
    </div>
</template>

<script>
import ProjectDataService from '../services/ProjectDataService'
// import TeamDataService from '../services/TeamDataService'
import useMembers from '../store/members'
import useProjects from '../store/projects'
import useTeams from '../store/teams'
export default {
    data(){
        return{
            filters: {},
            createProjectDialog: false,
            project: null,
            projectName: null,
            projectDesc: null,
            editProjectDialog: false,
            deleteProjectDialog: false
        }
    },
    async setup(){
        const {projects, getProjectProgress} = useProjects()
        const {members} = useMembers()
        const {selectedTeam} = useTeams()
        return{
            projects,
            getProjectProgress,
            members,
            selectedTeam
        }
    },
    methods:{
        async openCreateProjectDialog(){
            this.createProjectDialog = true;
        },
        async openEditProjectDialog(project){
            this.project = {...project}
            this.editProjectDialog = true;
        },
        async openDeleteProjectDialog(project){
            this.project = {...project}
            this.deleteProjectDialog = true;
        },
        async gotoProject(project){
            alert(project.name)
        },
        async createProject(){
            var new_project = {
                name: this.projectName,
                description: this.projectDesc,
                team_id: this.selectedTeam.id,
                sprint_interval: 2
            }
            const createdProject = (await ProjectDataService.createNewProject({
                new_project: new_project
            }))?.data
            this.projects.push(createdProject)
            await this.closeCreateProjectDialog()
        },
        async editProject(){
            await ProjectDataService.updateProject(
                this.project.id,
                {
                    project_update:{
                        ...this.project
                    }
                }
            )
            this.projects[this.findIndexById(this.project.id)] = this.project;
            this.project = {}
            await this.closeEditProjectDialog()
        },
        async deleteProject(){
            this.projects = this.projects.filter(val => val.id !== this.project.id);
            await ProjectDataService.deleteProject(this.project.id)
            this.project = {}
            await this.closeDeleteProjectDialog()
        },
        async closeCreateProjectDialog(){
            this.createProjectDialog = false;
        },
        async closeEditProjectDialog(){
            this.editProjectDialog = false;
        },
        async closeDeleteProjectDialog(){
            this.deleteProjectDialog = false;
        },
        findIndexById(id) {
            let index = -1;
            for (let i = 0; i < this.projects.length; i++) {
                if (this.projects[i].id === id) {
                    index = i;
                    break;
                }
            }
            return index;
        },
    }
}
</script>

<style>
.delete-confirmation-content {
    display: flex;
    align-items: center;
    justify-content: center;
}
</style>