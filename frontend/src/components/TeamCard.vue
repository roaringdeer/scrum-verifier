<template>
    <Card class="card-border" style="width: 20rem; ">
        <template #header>
            <button
            class="p-panel-header-icon p-link p-mr-2"
            style="float: right; margin-top: 5px;"
            @click="$emit('edit')"
            >
                <span class="pi pi-pencil"></span>
            </button>
        </template>
        <template #title>
            {{team?.name}}
        </template>
        <template #subtitle>
        </template>
        <template #content>
            <div v-if="team.description">
                {{shortenedDescription}}
            </div>
        </template>
        <template #footer>
            <Button label="Open" icon="pi pi-info-circle" @click="$emit('goto')"></Button>
        </template>
    </Card>
</template>

<script>
export default {
  props: ['team'],
  emits: ['edit', 'goto'],
  data(){
    return{
      isBlocked: false,
    }
  }, 
  computed: {
    shortenedDescription: function (){
      if (this.team.description.length < 100){
        return this.team.description
      }
      else {
        return this.team.description.substring(0, 100)+'...'
      }
    }
  }
};
</script>

<style>
.blocked{
  background-color: rgb(233, 236, 240)
}
.card-border {
  border: 2px solid rgba(67, 140, 224, 0.459);
  border-radius: 5px;
}
</style>
