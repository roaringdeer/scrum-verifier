<template>
    <div>
        <div style="cursor: pointer">
            <Tag @click="showDialog" :rounded="true" severity="success" v-if="role=='dev'">Developer</Tag>
            <Tag @click="showDialog" :rounded="true" severity="warning" v-else-if="role=='sm'">Scrum Master</Tag>
            <Tag @click="showDialog" :rounded="true" severity="danger" v-else-if="role=='po'">Product Owner</Tag>
            <Tag @click="showDialog" :rounded="true" severity="info" v-else>None</Tag>
        </div>
        <Dialog v-model:visible="dialogVisible" :modal="true" style="width: 600px; text-align: justify;">
            <template #header>
                <b>Role: {{roleString}}</b>
            </template>
            <div v-if="role=='dev'">
                <p>
                    Developer is a member of Development Team, which creates the product. He is a part of a self-organizing and self-managing
                    structure. It means, that no one decides for them how to realize Sprint Goals.
                </p>
                <p>
                    Developer may be specialized in some areas, but should be knowlegable in other areas as well. Cross-functionality of the
                    Development Team is necessary to deliver Incremets. As a result, there are no sub-teams and no special titles for Developers.
                    Whole Team works as one entity, and is held accountable as such.
                </p>
            </div>
            <div v-else-if="role=='sm'">
                <p>
                    Srcum Master is a Serving Leader. His role is to protect Development Team from outside interferance and helps
                    them in removing impediments and adopting Agile development practices.
                </p>
                <p>
                    Scrum Master doesn't command or control anyone - he helps by guiding Scrum Team members around the world of Scrum and
                    Agile practices. He enables close cooperation between Developers and Product Owner and between Developers themselves.
                    However, they need to demand team-wise and personal self-organization, as well as need to address not following Scrum
                    guidelines.
                </p>
            </div>
            <div v-else-if="role=='po'">
                <p>
                    Product Owner defines what the product will look like and what features it should contain. He is the point of contact
                    between customers and Development Team. Product Owner guards the Srcum Team from unnecessary involvment in contact width
                    customers, enabling them to focus on developing and delivering the product.
                </p>
                <p>
                    He owns the Product Backlog, and has to ensure that it is understood by the Development Team. As a result, he constantly
                    refines Product Backlog and reprioritizes its items, according to client's needs. He has the power to accept or reject
                    new Product Backlog items.
                </p>
            </div>
            <div v-else>
                <p>
                    No role is set. This tag signifies a person that is not a Scrum Team Member.
                </p>
                <p v-if="$route.name=='projectView'">
                    Contact Team Owner if you should have a role assigned.
                </p>
            </div>
        </Dialog>
    </div>
</template>

<script>
export default {
    props: ["role"],
    data(){
        return{
            dialogVisible: false
        }
    },
    setup(){
    },
    computed: {
        roleString(){
            switch (this.role){
                case 'po':
                    return 'Product Owner'
                case 'sm':
                    return 'Scrum Master'
                case 'dev':
                    return 'Developer'
                default:
                    return 'None'
            }
        }
    },
    methods: {
        showDialog(){
            console.log(this.$route.name)
            this.dialogVisible = true
        },
        closeDialog(){
            this.dialogVisible = false
        },
        
    }
}
</script>

<style>

</style>