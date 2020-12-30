<template>
    <div>
        <div class="content">
            <div v-if="error"> {{ error }} </div>
            <Suspense v-else>
                <template #default>
                    <ProjectCardsList />
                </template>
                <template #fallback>
                    <ProgressSpinner/>
                </template>
            </Suspense>
        </div>
        
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
    }
}

</script>

<style>

.sidebar {
    position: fixed;
    left: 0;
    top: 70px;
    height: calc(100% - 70px);
    overflow: auto;
    width: 200px;
    padding: 1rem;
}
.floater-right{
	position:fixed;
	bottom:40px;
	right:40px;
}
.floater-left{
	position:fixed;
	bottom:40px;
	left:40px;
}
</style>