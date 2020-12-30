<template>
    <div class="accordion">
        <Accordion>
            <AccordionTab :header="aboutScrum.about.title">
                <div class="p-text-justify" v-html="aboutScrum.about.content" />
            </AccordionTab>
            <AccordionTab :header="aboutScrum.artifacts.title">
                <div class="p-text-justify" v-html="aboutScrum.artifacts.content" />
            </AccordionTab>
            <AccordionTab :header="aboutScrum.team.title">
                <div class="p-text-justify" v-html="aboutScrum.team.content" />
            </AccordionTab>
            <AccordionTab :header="aboutScrum.events.title">
                <div class="p-text-justify" v-html="aboutScrum.events.content" />
            </AccordionTab>
            <AccordionTab :header="aboutScrum.theory.title">
                <div class="p-text-justify" v-html="aboutScrum.theory.content" />
            </AccordionTab>
            <AccordionTab :header="aboutScrum.values.title">
                <div class="p-text-justify" v-html="aboutScrum.values.content" />
            </AccordionTab>
            <AccordionTab :header="aboutScrum.workflow.title">
                <div class="p-text-justify" v-html="aboutScrum.workflow.content" />
            </AccordionTab>
        </Accordion>
    </div>
</template>

<script>
import aboutScrumJSON from '../content/aboutScrum.json'
export default {
    data(){
        return{
            aboutScrum: aboutScrumJSON
        }
    }
}
</script>

<style scoped>

</style>