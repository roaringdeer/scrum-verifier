<template>
    <div>
        <h1 class="center">Scrum-Verifier</h1>
        <img src="../assets/sv_logo.png">
        <h3 class="center">The intelligent Scrum help-and-advise tool.</h3>
        <Button label="Start now!" @click="goToLogin"/>
    </div>
</template>

<script>
export default {
  data(){
    return{

    }
  },
  methods:{
    goToLogin(){
      this.$router.push('/register');
    }
  }
}
</script>

<style>
.center{
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
}

</style>