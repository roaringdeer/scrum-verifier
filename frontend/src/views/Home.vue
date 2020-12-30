<template>
  <div class="content">
    <div v-if="isLoggedIn()">
        <Suspense>
          <Dashboard />
        </Suspense>
    </div>
    <div v-else>
      <Landing />
    </div>
  </div>
</template>

<script>
import AuthService from '../services/AuthService'

export default {
  data(){
    return{

    }
  },
  methods:{
    isLoggedIn(){
      return AuthService.isLoggedIn()
    },
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