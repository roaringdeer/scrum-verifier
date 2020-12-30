import {reactive, toRefs} from 'vue';
import ProjectDataService from '../services/ProjectDataService'

const state = reactive({
  projects: null,
  selectedProject: null
})

export default function useProjects() {

  const setProjects = async (value) => {
    state.projects = value;
  }

  const setProjectProgress = async (projectId, backlog, todo, ongoing, done) => {
    var project = state.projects?.filter(p => p.id == projectId)[0]
    project.stats.backlog_count = backlog.length
    project.stats.backlog_points = backlog.map(t => t.cost).reduce((prev, curr) => prev + curr, 0);
    project.stats.todo_count = todo.length
    project.stats.todo_points = todo.map(t => t.cost).reduce((prev, curr) => prev + curr, 0);
    project.stats.ongoing_count = ongoing.length
    project.stats.ongoing_points = ongoing.map(t => t.cost).reduce((prev, curr) => prev + curr, 0);
    project.stats.done_count = done.length
    project.stats.done_points = done.map(t => t.cost).reduce((prev, curr) => prev + curr, 0);
    project.stats.chart_data = (await ProjectDataService.getBurndownChartData(project.id))?.data
  }

  const getProjectProgress = (projectId) => {
    var project = state.projects?.filter(p => p.id == projectId)[0]
    if (project.stats.done_points + project.stats.todo_points  + project.stats.ongoing_points + project.stats.backlog_points == 0){
      return 0.0
    }
    console.log(project.stats.done_points / (project.stats.done_points + project.stats.todo_points  + project.stats.ongoing_points + project.stats.backlog_points))
    return Math.round(project.stats.done_points / (project.stats.done_points + project.stats.todo_points  + project.stats.ongoing_points + project.stats.backlog_points) * 100 * 100)/100
  }

  const setSelectedProject = async (value) => {
    state.selectedProject = value
  }

  const clearProjects = async () => {
    state.projects = null;
  }

  return {
    ...toRefs(state),
    setProjects,
    clearProjects,
    setSelectedProject,
    setProjectProgress,
    getProjectProgress
  }
}