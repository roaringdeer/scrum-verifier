<template>
    <div>
        <div class="p-grid">
            <div class="p-col" style="display: flex; justify-content: flex-start">
                <Button
                    label="Back to projects"
                    @click="$router.push('/projects')"
                />
            </div>
            <div class="p-col">
                Your team role is:
                <RoleTag :role="userRole"/>
            </div>
        </div>
        <div>
            <TabView >
                <TabPanel header="Info">
                    <div v-if="error"> {{ error }} </div>
                    <Suspense v-else>
                        <template #default>
                            <ProjectInfo/>
                        </template>
                        <template #fallback>
                            <ProgressSpinner/>
                        </template>
                    </Suspense>
                </TabPanel>
                <TabPanel header="Tasks">
                    <div v-if="error"> {{ error }} </div>
                    <Suspense v-else>
                        <template #default>
                            <Tasks />
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
                            <ProjectMembers />
                        </template>
                        <template #fallback>
                            <ProgressSpinner />
                        </template>
                    </Suspense>
                </TabPanel>
                <TabPanel header="Stats">
                    <div v-if="error"> {{ error }} </div>
                    <Suspense v-else>
                        <template #default>
                            <ProjectStats />
                        </template>
                        <template #fallback>
                            <ProgressSpinner />
                        </template>
                    </Suspense>
                </TabPanel>
            </TabView>
        </div>
    </div>
</template>

<script>
import useMembers from '../store/members'
import LocalStorageDataService from '../services/LocalStorageDataService'
import { onErrorCaptured, ref } from 'vue'
export default {
    data(){
        return{
            roleHelper: false
        }
    },
    setup(){
        const { members } = useMembers()
        const error = ref(null)
        const user = LocalStorageDataService.getUser()
        onErrorCaptured(e => {
            error.value = e
            return true
        })

        return{
            error,
            members,
            user
        }
    },
    computed: {
        userRole: function (){
            return this.members.filter(m => m.user_id == this.user.id)[0].role
        }
    },
    methods:{
        openRoleHelper(){
            this.roleHelper=true
        }
    }
}
</script>

<style>
.back-button{
    
}
</style>