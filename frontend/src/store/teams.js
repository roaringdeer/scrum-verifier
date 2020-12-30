import {reactive, toRefs} from 'vue';

const state = reactive({
  teams: null,
  selectedTeam: null
})

export default function useTeams() {

  const setTeams = async (value) => {
    state.teams = value;
  }

  const pushTeam = async (value) => {
    state.teams.push(value);
  }

  const setSelectedTeam = async (value) => {
    state.selectedTeam = value
  }

  const editTeam = async (value) => {
    state.teams[state.teams.findIndex(el => el.id == value.id)] = value
  }

  const deleteTeam = async (value) => {
    state.teams = state.teams.filter(val => val.id !== value.id);
  }

  const clearTeams = async () => {
    state.teams = null;
    state.selectedTeam = null;
  }

  return {
    ...toRefs(state),
    setTeams,
    setSelectedTeam,
    pushTeam,
    clearTeams,
    deleteTeam,
    editTeam
  }
}