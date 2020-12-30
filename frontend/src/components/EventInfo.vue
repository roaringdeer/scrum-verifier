<template>
    <div>
        <Tag :rounded="true" @click="openDialog">
            {{eventName}}
        </Tag>
        <Dialog v-model:visible="isOpen">
            <div v-if="eventType=='other'">
                This is a meeting not clearly defined in Scrum. However, it doesn't mean it isn't important!
            </div>
            <div v-else-if="eventType=='daily'">
                This is a Daily meeting. Discuss what you have accomplished so far and what you plan to do today.
            </div>
            <div v-else-if="eventType=='retro'">
                During this meeting you should be prepared to talk about your experience during this Sprint. Talk about any grievances you have towards your colleges and try to talk them through. If you came up with any improvements your team could benefit, it is the best time to present them!
            </div>
            <div v-else-if="eventType=='review'">
                Prepare for this one! This is a meeting with your client, so be ready to talk about what have been accomplished during the Sprint. Collect feedback about your work and talk about your products future.
            </div>
            <div v-else-if="eventType=='planning'">
                The beggining of the Sprint. Talk about what can be achived during this Sprint. Set the Sprint Goal and select Sprint Backlog items. Remember to not exceed your maximum capacity for work, so you can finish everything before the Sprint ends!
            </div>
            <div v-else>
                Unknown event type. If you see this message, something went wrong. Please contact us!
            </div>
        </Dialog>
    </div>

</template>

<script>
export default {
    props:['eventType'],
    data(){
        return{
            isOpen: false
        }
    },
    computed: {
        eventName: function (){
            switch (this.eventType){
                case 'other':
                    return 'Other'
                case 'daily':
                    return 'Daily'
                case 'retro':
                    return 'Sprint Retrospective'
                case 'review':
                    return 'Sprint Review'
                case 'planning':
                    return 'Sprint Planning'
                default:
                    return 'Unknown'
            }
        }
    },
    methods: {
        openDialog() {
            this.isOpen = true
        },
        closeDialog() {
            this.isOpen = false
        }
    }
    
}
</script>

<style scoped>

</style>