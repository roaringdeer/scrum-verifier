<template>
    <div>
        <div class="content">
            <div v-if="error"> 
                <SomethingWentWrong @back="backToProjects" />
            </div>
            <Suspense v-else>
                <template #default>
                    <ProjectTabs />
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
            // console.log(error)
            return true
        })
        
        return{error}
    },
    methods: {
        backToProjects(){
            this.$router.push('/projects')
        }
    }
}
</script>

<style>
.project-search{
    margin-top: 10px;

}
.shown-dropdown{
    width: 120px;
    margin-left: 10px;
    margin-top: 10px;
}
.back-button{
    float: left;
    overflow: auto;
    width: auto;
}
.content-body{
    padding-top: 50px;
    /* height: 80vh; */
    margin-bottom: 5vh;
}
</style>