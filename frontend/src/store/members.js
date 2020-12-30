import {reactive, toRefs} from 'vue';

const state = reactive({
  members: null
})

export default function useMembers() {

  const setMembers = async (value) => {
    state.members = value;
  }

  const clearMembers = async () => {
    state.members = null;
  }

  return {
    ...toRefs(state),
    setMembers,
    clearMembers
  }
}