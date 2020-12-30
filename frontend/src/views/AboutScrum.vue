<template>
    <div class="content">
        <div class="p-grid p-jc-center">
            <div class="p-col-12 p-md-6 p-lg-10 p-mx-2 p-offset-3 as-panel">
                <Card>
                    <template #title>
                        {{aboutScrum.about.title}}
                    </template>
                    <template #content>
                        <div class="p-text-justify" v-html="aboutScrum.about.content" />
                    </template>
                </Card>
            </div>
        </div>
        <div class="p-grid p-jc-center">
            <div class="p-col-12 p-md-6 p-lg-3 p-mx-2 p-jc-center" style="width: 400px">
                <Card>
                    <template #header>
                    </template>
                    <template #title>
                        {{aboutScrum.artifacts.title}}
                    </template>
                    <template #subtitle>
                        {{aboutScrum.artifacts.subtitle}}
                    </template>
                    <template #content>
                        {{aboutScrum.artifacts.description}}
                    </template>
                    <template #footer>
                        <Button icon="pi pi-info-circle" label='Learn more'  @click="openArtifactsDialog">
                        </Button>
                    </template>
                </Card>
            </div>
            <div class="p-col-12 p-md-6 p-lg-3 p-mx-2 p-jc-center" style="width: 400px">
                <Card>
                    <template #header>
                    </template>
                    <template #title>
                        {{aboutScrum.team.title}}
                    </template>
                    <template #subtitle>
                        {{aboutScrum.team.subtitle}}
                    </template>
                    <template #content>
                        {{aboutScrum.team.description}}
                    </template>
                    <template #footer>
                        <Button icon="pi pi-info-circle" label='Learn more'  @click="openTeamDialog">
                        </Button>
                    </template>
                </Card>
            </div>
            <div class="p-col-12 p-md-6 p-lg-3 p-mx-2 p-jc-center" style="width: 400px">
                <Card>
                    <template #header>
                    </template>
                    <template #title>
                        {{aboutScrum.events.title}}
                    </template>
                    <template #subtitle>
                        {{aboutScrum.events.subtitle}}
                    </template>
                    <template #content>
                        {{aboutScrum.events.description}}
                    </template>
                    <template #footer>
                        <Button icon="pi pi-info-circle" label='Learn more'  @click="openEventsDialog">
                        </Button>
                    </template>
                </Card>
            </div>
            <div class="p-col-12 p-md-6 p-lg-3 p-mx-2 p-jc-center" style="width: 400px">
                <Card>
                    <template #header>
                    </template>
                    <template #title>
                        {{aboutScrum.theory.title}}
                    </template>
                    <template #subtitle>
                        {{aboutScrum.theory.subtitle}}
                    </template>
                    <template #content>
                        {{aboutScrum.theory.description}}
                    </template>
                    <template #footer>
                        <Button icon="pi pi-info-circle" label='Learn more'  @click="openTheoryDialog">
                        </Button>
                    </template>
                </Card>
            </div>
            <div class="p-col-12 p-md-6 p-lg-3 p-mx-2 p-jc-center" style="width: 400px">
                <Card>
                    <template #header>
                    </template>
                    <template #title>
                        {{aboutScrum.values.title}}
                    </template>
                    <template #subtitle>
                        {{aboutScrum.values.subtitle}}
                    </template>
                    <template #content>
                        {{aboutScrum.values.description}}
                    </template>
                    <template #footer>
                        <Button icon="pi pi-info-circle" label='Learn more'  @click="openValuesDialog">
                        </Button>
                    </template>
                </Card>
            </div>
            <div class="p-col-12 p-md-6 p-lg-3 p-mx-2 p-jc-center" style="width: 400px">
                <Card>
                    <template #header>
                    </template>
                    <template #title>
                        {{aboutScrum.workflow.title}}
                    </template>
                    <template #subtitle>
                        {{aboutScrum.workflow.subtitle}}
                    </template>
                    <template #content>
                        {{aboutScrum.workflow.description}}
                    </template>
                    <template #footer>
                        <Button icon="pi pi-info-circle" label='Learn more' @click="openWorkflowDialog">
                        </Button>
                    </template>
                </Card>
            </div>
        </div>
        <div>
            <Dialog class="as-dialog" header="Scrum Artifacts" v-model:visible="displayArtifactsDialog" :style="{width: '50vw'}" :maximizable="true" :modal="true">
                <div v-html="aboutScrum.artifacts.content" style="text-align: justify;"/>
            </Dialog>
            <Dialog header="Scrum Team" v-model:visible="displayTeamDialog" :style="{width: '50vw'}" :maximizable="true" :modal="true">
                <div v-html="aboutScrum.team.content" style="text-align: justify;" />
            </Dialog>
            <Dialog header="Scrum Events" v-model:visible="displayEventsDialog" :style="{width: '50vw'}" :maximizable="true" :modal="true">
                <div v-html="aboutScrum.events.content" style="text-align: justify;" />
            </Dialog>
            <Dialog header="Scrum Theory" v-model:visible="displayTheoryDialog" :style="{width: '50vw'}" :maximizable="true" :modal="true">
                <div v-html="aboutScrum.theory.content" style="text-align: justify;" />
            </Dialog>
            <Dialog header="Scrum Values" v-model:visible="displayValuesDialog" :style="{width: '50vw'}" :maximizable="true" :modal="true">
                <div v-html="aboutScrum.values.content" style="text-align: justify;" />
            </Dialog>
            <Dialog header="Scrum Workflow" v-model:visible="displayWorkflowDialog" :style="{width: '50vw'}" :maximizable="true" :modal="true">
                <div v-html="aboutScrum.workflow.content" style="text-align: justify;" />
            </Dialog>
        </div>
    </div>
</template>

<script>
import aboutScrumJSON from '../content/aboutScrum.json'
export default {
    data(){
        return{
            displayArtifactsDialog: false,
            displayTeamDialog: false,
            displayEventsDialog: false,
            displayTheoryDialog: false,
            displayValuesDialog: false,
            displayWorkflowDialog: false,
            aboutScrum: aboutScrumJSON
        }
    },
    methods: {
        openArtifactsDialog(){
            this.displayArtifactsDialog = true;
        },
        openTeamDialog(){
            this.displayTeamDialog = true;
        },
        openEventsDialog(){
            this.displayEventsDialog = true;
        },
        openTheoryDialog(){
            this.displayTheoryDialog = true;
        },
        openValuesDialog(){
            this.displayValuesDialog = true;
        },
        openWorkflowDialog(){
            this.displayWorkflowDialog = true;
        }
    }
    
}
</script>

<style scoped>
.as-card{
    width: 400px;
    margin-bottom: 20px;
    justify-self: center;
}
.as-panel{
    min-width: 400px;
    max-width: 1400px;
    margin-bottom: 40px;
    
}
.as-dialog{
    text-align: left;
}
</style>