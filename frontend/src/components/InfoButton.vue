<template>
    <div>
        <Button class="floater-right p-button-rounded" icon="pi pi-info-circle" :rounded="true" @click="openDialog"></Button>
        <Dialog v-model:visible="isOpen" :modal="true" header="Help" class="dialog">
            <TabView>
                <TabPanel header="General">
                    <p>
                        This is Scrum Verifier help.
                    </p>
                    <p>
                        If you notice any bugs, something is unclear to you or you have any improvement ideas,
                        please write to us as soon as possible.
                    </p>
                </TabPanel>
                <TabPanel header="Projects">
                    <p>
                        In 'Projects' you can see all projects you're part of.
                    </p>
                    <p>
                        You can search projects, or filter them.
                    </p>
                    <p>
                        Note, that you cannot change the projects here. To do that, navigate to 'Teams'.
                    </p>
                </TabPanel>
                <TabPanel header="Teams">
                    <p>
                        In 'Teams' there are visible the teams that you are part of.
                    </p>
                    <p>
                        If you are the teams owner, you can also add and remove projects and members of team, as well as assign
                        members their Scrum Team roles.
                    </p>
                </TabPanel>
                <TabPanel header="About Scrum">
                    <ScrumInfo/>
                </TabPanel>
            </TabView>
            

        </Dialog>    
    </div>
</template>

<script>
export default {
    events: ['open'],
    data(){
        return{
            isOpen: false
        }
    },
    methods: {
        openDialog(){
            this.isOpen = true
        },
        closeDialog(){
            this.isOpen = false
        }
    }
}
</script>

<style>
.floater-right{
	position:fixed;
	bottom:40px;
	right:40px;
}
.dialog{
    width: 600px;
    height: 600px;
    background-color: var(--surface-a);
    text-align: left;
}
</style>