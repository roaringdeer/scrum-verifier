<template>
    <div>
        <div class="content">
            <div v-if="error"> {{ error }} </div>
            <Suspense v-else>
                <template #default>
                    <TeamCardsList />
                </template>
                <template #fallback>
                    <ProgressSpinner/>
                </template>
            </Suspense>
        </div>
        <!-- <Button class="floater-right p-button-rounded" icon="pi pi-info-circle" :rounded="true"></Button> -->
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

.sidebar {
    position: fixed;
    left: 0;
    top: 70px;
    height: calc(100% - 70px);
    overflow: auto;
    width: 200px;
    padding: 1rem;
    -webkit-transition: -webkit-transform .4s cubic-bezier(.05,.74,.2,.99);
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
.create-floater-right{
    position:fixed;
	bottom:80px;
	right:40px;
}
</style>