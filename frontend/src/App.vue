<template>
  <div>
    <nav>
      <NavBar/>
    </nav>
    <router-view></router-view>
    <InfoButton v-if="isLoggedIn()"/>
  </div>
</template>

<script>
import AuthService from './services/AuthService'
export default {
  name: 'App',
  methods:{
      isLoggedIn(){
        return AuthService.isLoggedIn()
      }
  }
}
</script>

<style>
body{
  /* background-color:rgba(165, 206, 230, 0.185); */
  /* color: var(--text-color); */
  /* background-color: var(--surface-d); */
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  /* color: #2c3e50; */
  margin-top: 0px;
}
.menu-bar{
  margin-bottom: 20px;
}
.content{
  margin-left: 10vw;
  margin-right: 10vw;
  margin-bottom: 5vh;
  padding: 0;
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
</style>
