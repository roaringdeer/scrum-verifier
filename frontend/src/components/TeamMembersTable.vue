<template>
    <div class="card">
        <DataTable :value="members" :paginator="true" class="p-datatable-customers" :rows="10"
        dataKey="id" :rowHover="true" :filters="filters" :loading="loading"
        paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown" :rowsPerPageOptions="[10,25,50]"
        currentPageReportTemplate="Showing {first} to {last} of {totalRecords} entries">
            <template #header>
                <div class="table-header">
                    Members
                    <span>
                        <Button class="p-mr-2" label="Add new Member" @click="openAddMemberDialog"/>
                        <span class="p-input-icon-left">
                            <i class="pi pi-search" />
                            <InputText v-model="filters['global']" placeholder="Search" />
                        </span>
                    </span>
                </div>
            </template>
            <template #empty>
                No members found.
            </template>
            <template #loading>
                Loading members...
            </template>
            <Column :sortable="true" field="profile.username" header="Username"></Column>
            <Column :sortable="true" field="profile.full_name" header="Name"></Column>
            <Column :sortable="true" field="profile.email" header="E-Mail"></Column>
            <Column :sortable="true" field="role" header="Role">
                <template #body="slotProps">
                    <RoleTag :role="slotProps.data.role"/>
                    <!-- <Tag :rounded="true" severity="success" v-if="slotProps.data.role=='dev'">Developer</Tag>
                    <Tag :rounded="true" severity="warning" v-else-if="slotProps.data.role=='sm'">Scrum Master</Tag>
                    <Tag :rounded="true" severity="danger" v-else-if="slotProps.data.role=='po'">Product Owner</Tag>
                    <Tag :rounded="true" severity="info" v-else>None</Tag> -->
                </template>
            </Column>
            <Column headerStyle="width: 10rem; text-align: center" bodyStyle="text-align: center; overflow: visible">
                <template #body="slotProps">
                    <span class="p-buttonset">
                        <Button type="button" icon="pi pi-trash" class="p-button-danger" @click="openDeleteMemberDialog(slotProps.data)"></Button>
                        <Button type="button" icon="pi pi-pencil" class="p-button-warning" @click="openEditMemberDialog(slotProps.data)" ></Button>
                        <Button type="button" icon="pi pi-angle-right" class="p-button-success" @click="gotoMember(slotProps.data)"></Button>
                    </span>
                </template>
            </Column>
        </DataTable>

        <Dialog header="Add member" :modal="true" v-model:visible="addMemberDialog">
            <div class="p-inputgroup" style="margin-bottom: 10px">
                <span class="p-inputgroup-addon">Username</span>
                <InputText v-model="username" />
            </div>
            <h5>Member Role</h5>
            <div v-for="role of roles" :key="role.key" class="p-field-radiobutton">
                <RadioButton :id="role.key" name="category" :value="role.key" v-model="selectedRole" />
                <label :for="role.key">{{role.name}}</label>
            </div>
            <template #footer>
                <Button label="Cancel" icon="pi pi-times" @click="closeAddMemberDialog" class="p-button-text"/>
                <Button label="Add" icon="pi pi-check" @click="addMember" class="p-button-text" autofocus />
            </template>
        </Dialog>

        <Dialog header="Edit member" :modal="true" v-model:visible="editMemberDialog" style="width: 400px">
            <h4>{{member.profile.username}}</h4>
            <Divider>
                Member role
            </Divider>
            <div v-for="role of roles" :key="role.key" class="p-field-radiobutton">
                <RadioButton :id="role.key" name="role" :value="role.key" v-model="selectedRole" />
                <label :for="role.key">{{role.name}}</label>
            </div>
            <template #footer>
                <Button label="Cancel" icon="pi pi-times" class="p-button-text" @click="closeEditMemberDialog"/>
                <Button label="Save" icon="pi pi-check" class="p-button-text" @click="editMember" />
            </template>
        </Dialog>

        <Dialog header="Delete member" v-model:visible="deleteMemberDialog" :style="{width: '350px'}" :modal="true">
            <div class="delete-confirmation-content">
                <i class="pi pi-exclamation-triangle p-mr-3" style="font-size: 2rem" />
                <span>Are you sure you want to delete {{member.name}}?</span>
            </div>
            <template #footer>
                <Button label="No" icon="pi pi-times" @click="closeDeleteMemberDialog" class="p-button-text"/>
                <Button label="Yes" icon="pi pi-check" @click="deleteMember" class="p-button-text" autofocus />
            </template>
        </Dialog>
    </div>    
</template>

<script>
import MemberDataService from '../services/MemberDataService'
import ProfileDataService from '../services/ProfileDataService'
import useMembers from '../store/members'
import useTeams from '../store/teams'
import RoleTag from './RoleTag.vue'

export default {
  components: { RoleTag },
    data(){
        return{
            filters: {},
            addMemberDialog: false,
            editMemberDialog: false,
            deleteMemberDialog: false,
            member: null,
            role: 'none',
            username: null,
            selectedRole: 'none',
            roles: [
                {name: 'Developer', key: 'dev'},
                {name: 'Scrum Master', key: 'sm'},
                {name: 'Product Owner', key: 'po'},
                {name: 'None', key: 'none'},
            ]
        }
    },
    setup(){
        const {members} = useMembers()
        const {selectedTeam} = useTeams()
        return {
            members,
            selectedTeam
        }
    },
    methods:{
        async openAddMemberDialog(){
            this.addMemberDialog = true;
        },
        async openEditMemberDialog(member){
            this.member = {...member}
            this.editMemberDialog = true;
            this.selectedRole = member.role;
        },
        async openDeleteMemberDialog(member){
            this.member = {...member}
            this.deleteMemberDialog = true;
        },
        async gotoMember(member){
            alert(member.profile.username)
        },
        async addMember(){
            try{
                const searchedUser = (await ProfileDataService.getProfile(this.username))?.data
                var newMember = {
                    user_id: searchedUser.id,
                    team_id: this.selectedTeam.id
                }
                const createdMember = (await MemberDataService.createNewMember(
                    this.selectedTeam.id,
                    {
                        new_member: newMember
                    }
                ))?.data
                this.members.push(createdMember);
                await this.closeAddMemberDialog()
            }
            catch(error){
                if (error.response) {
                    alert('Error ' + error.response.status +': ' +error.response.data.detail);
                } else if (error.request) {
                    alert(error.request);
                } else {
                    alert(error.message);
                }
            }
        },
        async editMember(){
            try{
                const updatedMember = (await MemberDataService.updateMember(
                    this.selectedTeam.id,
                    this.member.profile.username,
                    {
                        member_update:{
                            role: this.selectedRole
                        }
                    }
                ))?.data
                this.members[this.findIndexById(this.member.user_id)] = updatedMember;
                this.member = {}
            }
            catch(error){
                if (error.response) {
                    alert('Error ' + error.response.status +': ' +error.response.data.detail);
                } else if (error.request) {
                    alert(error.request);
                } else {
                    alert(error.message);
                }
            }
            await this.closeEditMemberDialog()
        },
        async deleteMember(){
            try{
                await MemberDataService.deleteMember(
                    this.selectedTeam.id,
                    this.member.profile.username
                )
                this.members = this.members.filter(val => val.user_id !== this.member.user_id);
                this.member = {}
            }
            catch(error){
                if (error.response) {
                    alert('Error ' + error.response.status +': ' +error.response.data.detail);
                } else if (error.request) {
                    alert(error.request);
                } else {
                    alert(error.message);
                }
            }
            await this.closeDeleteMemberDialog()
        },
        async closeAddMemberDialog(){
            this.username = null;
            this.selectedRole = 'none';
            this.addMemberDialog = false;
        },
        async closeEditMemberDialog(){
            this.selectedRole = 'none'
            this.editMemberDialog = false;
        },
        async closeDeleteMemberDialog(){
            this.deleteMemberDialog = false;
        },
        findIndexById(id) {
            let index = -1;
            for (let i = 0; i < this.members.length; i++) {
                if (this.members[i].user_id === id) {
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
.table-header {
    display: flex;
    justify-content: space-between;
}
</style>