<template>
    <div>
    <div class="p-grid">
            <Button
                label="Back to teams"
                @click="$router.push('/teams')"
                style="float: right;"
            />
        </div>
        <div>
            <TabView>
                <TabPanel header="Info">
                    <div v-if="error"> {{ error }} </div>
                    <Suspense v-else>
                        <template #default>
                            <TeamInfo/>
                        </template>
                        <template #fallback>
                            <ProgressSpinner/>
                        </template>
                    </Suspense>
                </TabPanel>
                <TabPanel header="Projects">
                    <div v-if="error"> {{ error }} </div>
                    <Suspense v-else>
                        <template #default>
                            <TeamProjectsTable/>
                        </template>
                        <template #fallback>
                            <ProgressSpinner/>
                        </template>
                    </Suspense>
                </TabPanel>
                <TabPanel header="Members">
                    <div v-if="error"> {{ error }} </div>
                    <Suspense v-else>
                        <template #default>
                            <TeamMembersTable/>
                        </template>
                        <template #fallback>
                            <ProgressSpinner/>
                        </template>
                    </Suspense>
                </TabPanel>
            </TabView>
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
    },
    
}
</script>

<style>

</style>