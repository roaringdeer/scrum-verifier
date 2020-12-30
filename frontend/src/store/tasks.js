import {reactive, toRefs} from 'vue';
import TaskDataService from '../services/TaskDataService'
import useProjects from '../store/projects'

const {setProjectProgress} = useProjects()

const state = reactive({
  tasks: null,
  backlog: null,
  todo: null,
  ongoing: null,
  done: null
})

export default function useTasks() {

  const getTasks = async (projectId) => {
    state.tasks = (await TaskDataService.getAllProjectTasks(projectId))?.data
    sortTasks()
    setProjectProgress(projectId, state.backlog, state.todo, state.ongoing, state.done)
  }

  const setTasks = async (tasks) => {
    state.tasks = tasks
    sortTasks()
    setProjectProgress(tasks[0]?.project_id, state.backlog, state.todo, state.ongoing, state.done)
  }

  const sortTasks = () => {
    state.backlog = state.tasks.filter(t => t.status == 'backlog')
    state.todo = state.tasks.filter(t => t.status == 'to_do')
    state.ongoing = state.tasks.filter(t => t.status == 'ongoing')
    state.done = state.tasks.filter(t => t.status == 'done')
  }

  const createTask = async (taskToCreate) => {
    const createdTask = (await TaskDataService.createNewTask({
      new_task: taskToCreate
    }))?.data
    state.tasks.push(createdTask)
    state.backlog.push(createdTask)
    await setProjectProgress(taskToCreate.project_id, state.backlog, state.todo, state.ongoing, state.done)
  }

  const editTask = async (taskToUpdate) => {
    delete taskToUpdate.blocked;
    // if (typeof taskToUpdate.user_id != 'integer'){
    //   taskToUpdate.user_id = taskToUpdate.user_id.id
    // }
    const updatedTask = (await TaskDataService.updateTask(
      taskToUpdate.id,
      {
        task_update:{
          ...taskToUpdate
        }
      }
    ))?.data
    state.tasks[state.tasks.findIndex(el => el.id == updatedTask.id)] = updatedTask
    await setProjectProgress(taskToUpdate.project_id, state.backlog, state.todo, state.ongoing, state.done)
  }

  const deleteTask = async (taskToDelete) => {
    state.tasks = state.tasks.filter(val => val.id !== taskToDelete.id);
    state.todo = state.todo.filter(val => val.id !== taskToDelete.id);
    state.ongoing = state.ongoing.filter(val => val.id !== taskToDelete.id);
    state.done = state.done.filter(val => val.id !== taskToDelete.id);
    await TaskDataService.deleteTask(taskToDelete.id)
    await setProjectProgress(taskToDelete.project_id, state.backlog, state.todo, state.ongoing, state.done)
  }

  const clearTasks = async () => {
    state.tasks = null;
    state.todo = null;
    state.ongoing = null;
    state.done = null;
  }

  return {
    ...toRefs(state),
    getTasks,
    clearTasks,
    createTask,
    editTask,
    deleteTask,
    setTasks
  }
}