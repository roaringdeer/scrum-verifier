<template>
  <Card class="card-border" style="width: 20rem;">
    <template #header>
        {{team}}
    </template>
    <template #title>
        {{project.name}}
    </template>
    <template #subtitle>
        <div>
            <ProgressBar :value="progress"/>
        </div>
    </template>
    <template #content>
        <div v-if="project.description">
            {{project.description.substring(0, 100)+'...'}}
        </div>
    </template>
    <template #footer>
        <Button label="Open" icon="pi pi-info-circle" @click="$emit('goto')"></Button>
    </template>
  </Card>
</template>

<script>
export default {
  props: ['project', 'team', 'progress'],
  emits: ['edit', 'goto'],
  data(){
    return{

    }
  }
};
</script>

<style>
.card-border {
  border: 2px solid var(--primary-color);
  border-radius: 5px;
}
</style>
