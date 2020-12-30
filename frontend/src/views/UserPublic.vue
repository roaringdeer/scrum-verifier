<template>
    <div>
        <div v-if="error"> {{ error }} </div>
        <Suspense v-else>
            <template #default>
                <UserProfilePublic/>
            </template>
            <template #fallback>
                <ProgressSpinner/>
            </template>
        </Suspense>
    </div>
</template>

<script>
import { onErrorCaptured, ref } from 'vue'

export default {
    data(){
        return{

        };
    },
    setup(){
        const error = ref(null)
        onErrorCaptured(e => {
            error.value = e
            return true
        })
        
        return{error}
    },
}
</script>

<style>

</style>