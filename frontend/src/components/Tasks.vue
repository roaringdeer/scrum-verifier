<template>
  <div>
    <div class="p-grid" style="margin-bottom: 10px;">
      <div class="p-col">
        <Button label="Add task" style="float: left;" @click="openCreateTaskDialog"/>
      </div>
    </div>
    <div class="p-grid">
      <div class="p-col tasks-border" style="height: 65vh; overflow: auto; margin: 5px">
          <div v-tooltip="backlogTooltip">
            Backlog
          </div>
          <Divider />
          <draggable 
            class="list-group"
            :list="backlog"
            group="people"
            @change="onBacklogChange"
            itemKey="id"
            :delay="200"
            :delay-on-touch-only="true"
            id="todo"
          >
            <template #item="{element}">
                <div style="padding-bottom: 10px;">
                  <TaskCard :task="element" @edit="openEditTaskDialog(element)"/>
                </div>
            </template>
          </draggable>
      </div>
      <div class="p-col tasks-border" style="height: 65vh; overflow: auto; margin: 5px">
        <div v-tooltip="todoTooltip">
          Sprint Backlog
        </div>
        <Divider />
        <draggable 
          class="list-group"
          :list="todo"
          group="people"
          @change="onToDoChange"
          itemKey="id"
          :delay="200"
          :delay-on-touch-only="true"
          id="todo"
        >
          <template #item="{element}">
              <div style="padding-bottom: 10px;">
                <TaskCard :task="element" @edit="openEditTaskDialog(element)"/>
              </div>
          </template>
        </draggable>
      </div>
      <div class="p-col tasks-border" style="height: 65vh; overflow: auto; margin: 5px">
        <div v-tooltip="ongoingTooltip">
        Ongoing
        </div>
        <Divider />
        <draggable  
          class="list-group"
          :list="ongoing"
          group="people"
          @change="onOngoingChange"
          itemKey="id"
          :delay="200"
          :delay-on-touch-only="true"
          id="ongoing"
        >
          <template #item="{element}">
              <div style="padding-bottom: 10px;">
                <TaskCard :task="element" @edit="openEditTaskDialog(element)"/>
              </div>
          </template>
        </draggable>
      </div>
      <div class="p-col tasks-border" style="height: 65vh; overflow: auto; margin: 5px">
        <div v-tooltip="doneTooltip">
        Done
        </div>
        <Divider />
        <draggable 
          class="list-group"
          :list="done"
          group="people"
          @change="onDoneChange"
          itemKey="id"
          :delay="200"
          :delay-on-touch-only="true"
          id="done"
        >
          <template #item="{element}">
              <div style="padding-bottom: 10px;" :key="element.id">
                <TaskCard :task="element" @edit="openEditTaskDialog(element)"/>
              </div>
          </template>
        </draggable>
      </div>
    </div>
    <Dialog header="Create new task" :contentStyle="{overflow: 'visible'}" :modal="true" v-model:visible="createTaskDialog">
      {{assignedUser}}
      <Divider>
        Name
      </Divider>
      <InputText v-model="taskName" style="float: left; width: 80%;"/>
      <Divider>
        Description
      </Divider>
      <Textarea v-model="taskDesc" rows="5" cols="30" :autoResize="true" style="float: left; width: 80%;"/>
      <Divider>
        Cost
      </Divider>
      <InputNumber v-model="cost" showButtons buttonLayout="horizontal" :step="1"
        decrementButtonClass="p-button-danger" incrementButtonClass="p-button-success"
        incrementButtonIcon="pi pi-plus" decrementButtonIcon="pi pi-minus" style="float: left; width: 80%;"/>
      <Divider>
        Assigned User
      </Divider>
      <Dropdown
        v-model="assignedUser"
        :options="members"
        optionLabel="profile.username"
        placeholder="Select Member"
        style="float: left; width: 80%;"/>
      <Divider>
        Dependent on
      </Divider>
      <MultiSelect
        v-model="dependentOn"
        :options="tasks"
        optionLabel="name"
        placeholder="Select Tasks"
        style="float: left; width: 80%;"/>
      <template #footer>
        <Button label="Cancel" icon="pi pi-times" class="p-button-text" @click="closeCreateTaskDialog"/>
        <Button label="Create" icon="pi pi-check" class="p-button-text" @click="createToDoTask" />
      </template>
    </Dialog>

    <Dialog header="Edit task" :contentStyle="{overflow: 'visible'}" :modal="true" v-model:visible="editTaskDialog">
      <Divider>
        Name
      </Divider>
      <InputText v-model="task.name" style="float: left; width: 80%;"/>
      <Divider>
        Description
      </Divider>
        <Textarea v-model="task.description" rows="5" cols="30" :autoResize="true" style="float: left; width: 80%;"/>
      <Divider>
        Cost
      </Divider>
      <InputNumber v-model="task.cost" showButtons buttonLayout="horizontal" :step="1"
        decrementButtonClass="p-button-danger" incrementButtonClass="p-button-success"
        incrementButtonIcon="pi pi-plus" decrementButtonIcon="pi pi-minus" style="float: left; width: 80%;"/>
      <Divider>
        Assigned User
      </Divider>
      <Dropdown
        v-model="task.user_id"
        :options="members.map(m => m.profile)"
        :showClear="true"
        optionLabel="username"
        placeholder="Select Member"
        style="float: left; width: 80%;"
      />
      <Divider>
        Dependent on
      </Divider>
      <MultiSelect
        v-model="taskDependentOn"
        :options="tasks"
        optionLabel="name"
        placeholder="Select Tasks"
        style="float: left; width: 80%;"
      />
      <template #footer>
        <Button label="Delete" icon="pi pi-trash" class="p-button-text" @click="openDeleteTaskDialog" style="float: left;"/>
        <Button label="Cancel" icon="pi pi-times" class="p-button-text" @click="closeEditTaskDialog"/>
        <Button label="Save" icon="pi pi-check" class="p-button-text" @click="editSelectedTask" />
      </template>
    </Dialog>
    
    <Dialog header="Confirmation" v-model:visible="deleteTaskDialog" :style="{width: '350px'}" :modal="true">
      <div class="confirmation-content">
          <i class="pi pi-exclamation-triangle p-mr-3" style="font-size: 2rem" />
          <span>Are you sure you want to proceed?</span>
      </div>
      <template #footer>
          <Button label="No" icon="pi pi-times" @click="closeDeleteTaskDialog" class="p-button-text" autofocus/>
          <Button label="Yes" icon="pi pi-check" @click="deleteSelectedTask" class="p-button-text"/>
      </template>
    </Dialog>
  </div>
</template>

<script>
import draggable from 'vuedraggable'
import useTasks from '../store/tasks'
import useMembers from '../store/members'
import useProjects from '../store/projects'
import {httpAuth} from '../http-common'
// import AuthService from '../services/AuthService'

export default {
  components: {
    draggable
  },
  data(){
    return{
      connection: null,
      task: null,
      createTaskDialog: false,
      editTaskDialog: false,
      deleteTaskDialog: false,
      taskName: null,
      taskDesc: null,
      cost: 0,
      assignedUser: null,
      dependentOn: [],
      taskDependentOn: [],
      search: ""
    }
  },
  async setup(){
    const { selectedProject } = useProjects()
    const { tasks, backlog, todo, ongoing, done, createTask, editTask, deleteTask, setTasks} = useTasks()
    const { members } = useMembers()
    var ticket = (await httpAuth.get(`/projects/ws/ticket`))?.data.ticket
    
    return{
      tasks,
      backlog,
      todo,
      ongoing,
      done,
      createTask,
      editTask,
      deleteTask,
      members,
      selectedProject,
      setTasks,
      ticket
    }
  },
  created(){
    this.connection = new WebSocket(`ws://localhost:8000/api/projects/${this.selectedProject.id}/ws?ticket=${this.ticket}`)
    this.connection.addEventListener('message', (event) => {
      var json = JSON.parse(event.data)
      this.setTasks(json)
    })
    this.connection.onopen = function (event){
      console.log(event)
    }
    this.connection.onerror = function (event){
      console.log(event)
    }
  },
  computed: {
    backlogTooltip: function (){
      return `Tasks count: ${this.selectedProject.stats.backlog_count}\nTasks points: ${this.selectedProject.stats.backlog_points}`
    },
    todoTooltip: function (){
      return `Tasks count: ${this.selectedProject.stats.todo_count}\nTasks points: ${this.selectedProject.stats.todo_points}`
    },
    ongoingTooltip: function (){
      return `Tasks count: ${this.selectedProject.stats.ongoing_count}\nTasks points: ${this.selectedProject.stats.ongoing_points}`
    },
    doneTooltip: function (){
      return `Tasks count: ${this.selectedProject.stats.done_count}\nTasks points: ${this.selectedProject.stats.done_points}`
    },
  },
  methods: {
    async sendWebSocketJSON(json) {
      this.connection.send(
        JSON.stringify(
          json
        )
      )
    },
    async onBacklogChange({added}){
      if (added) {
        added.element.status = 'backlog'
        var message = {
          action: 'update',
          payload: {
            id: added.element.id,
            status:'backlog',
            project_id: added.element.project_id,
            date_done: null
          }
        }
        await this.sendWebSocketJSON(message)
      }
    },
    async onToDoChange({ added }) {
      if (added) {
        var message = {
        action: 'update',
        payload: {
          id: added.element.id,
            status:'to_do',
            project_id: added.element.project_id,
            date_done: null
          }
        }
        added.element.status = 'to_do'
        await this.sendWebSocketJSON(message)
      }
    },
    async onOngoingChange({ added }) {
      if (added) {
        var message = {
          action: 'update',
          payload: {
            id: added.element.id,
            status:'ongoing',
            project_id: added.element.project_id,
            date_done: null
          }
        }
        added.element.status = 'ongoing'
        await this.sendWebSocketJSON(message)
      }
    },
    async onDoneChange({ added }) {
      if (added) {
        var message = {
        action: 'update',
        payload: {
          id: added.element.id,
            status:'done',
            project_id: added.element.project_id,
            date_done: new Date()
          }
        }
        added.element.status = 'done'
        await this.sendWebSocketJSON(message)
      }
    },
    async openCreateTaskDialog(){
      this.createTaskDialog = true;
    },
    async openEditTaskDialog(task){
      this.task = {...task}

      this.taskDependentOn = this.tasks.filter(t => this.task?.dependent_on.includes(t.id))
      this.editTaskDialog = true;
    },
    async openDeleteTaskDialog(){
      // this.task = {...task}
      this.deleteTaskDialog = true;
    },
    async gotoTask(task){
      alert(task.name)
    },
    async createToDoTask(){
      var message = {
        action: 'create',
        payload: {
          name: this.taskName,
          description: this.taskDesc,
          cost: this.cost,
          user_id: this.assignedUser?.user_id,
          dependent_on: this.dependentOn.map(t => t.id),
          status: 'backlog',
          project_id: this.selectedProject.id
        }
      }
      await this.sendWebSocketJSON(message)
      await this.closeCreateTaskDialog()
    },
    async editSelectedTask(){
      this.task.dependent_on = this.taskDependentOn.map(t => t.id)
      var message = {
        action: 'update',
        payload: this.task
      }
      if (typeof message.payload.task?.user_id == "object"){
        message.payload.task.user_id = message.payload.task.user_id.id
      }
      await this.sendWebSocketJSON(message)
      this.task = {}
      await this.closeEditTaskDialog()
    },
    async deleteSelectedTask(){
      var message = {
        action: 'delete',
        payload: this.task
      }
      await this.sendWebSocketJSON(message)
      this.task = {}
      await this.closeEditTaskDialog()
      await this.closeDeleteTaskDialog()
    },
    async closeCreateTaskDialog(){
      this.createTaskDialog = false;
    },
    async closeEditTaskDialog(){
      this.editTaskDialog = false;
      this.taskDependentOn = []
      this.task = {}
    },
    async closeDeleteTaskDialog(){
      this.deleteTaskDialog = false;
    },
    searchedTasks(tasksArray, query){
      return tasksArray.filter(function(el) {
        return el.name.toLowerCase().indexOf(query.toLowerCase())> -1 || el.description?.toLowerCase().indexOf(query.toLowerCase())>-1
      })
    }
  },
}
</script>

<style scoped>
.drop-zone {
  background-color: #eee;
  margin-bottom: 10px;
  padding: 10px;
}

.drag-el {
  background-color: #fff;
  margin-bottom: 10px;
  padding: 5px;
}
.list-group{
  height: 90%;
}
.custom .p-scrollpanel-bar {
    background-color: #1976d2;
    opacity: 1;
    transition: background-color .3s;
}
.overflow-dialog .p-dialog {
  overflow: visible;
}

.tasks-border {
  border: 2px solid var(--secondary-color);
  /* rgb(136, 136, 136); */
  border-radius: 5px;
}
</style>