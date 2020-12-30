<template>
    <div class="p-text-center">
        <h2>Something went wrong</h2>
        <Button label="Take me back!" @click="$emit('back')"/>
    </div>
</template>

<script>
export default {
    emits: ['back'],
}
</script>

<style>

</style>