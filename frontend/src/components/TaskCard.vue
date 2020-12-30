<template>
  <Card v-bind:class="{blocked: isBlocked}" class="card-border">
    <template #header>
      <i 
        v-if="task.blocked"
        class="p-tag p-tag-icon p-tag-warning pi pi-exclamation-triangle"
        style="float: left; margin-left: 5px; margin-top: 5px;"
        v-tooltip="'Warning: finish other tasks that this task depends on!'"
      />
      <button
        class="p-panel-header-icon p-link p-mr-2"
        style="float: right; margin-top: 5px;"
        @click="$emit('edit')"
      >
        <span class="pi pi-pencil"></span>
      </button>
    </template>
    <template #title>
      {{task.name}}
    </template>
    <template #subtitle>
      Cost: {{task.cost}}
    </template>
    <template #content>
      {{task.description}}
    </template>
  </Card>
</template>

<script>
export default {
  props: ['task'],
  emits: ['edit'],
  data(){
    return{
      isBlocked: false,
    }
  }
};
</script>

<style>

</style>
