<template>
  <div v-if="isLoggedIn()">
      <nav>
          <Menubar :model="loggedInItems" class="menu-bar">
              <template #start>
                <a href="/">
                    <img alt="logo" :src="img" height="40" class="p-mr-2">
                </a>
              </template>
              <template #end>
              
              </template>
          </Menubar>
      </nav>
  </div>
  <div v-else>
      <nav>
          <Menubar :model="notLoggedInItems" class="menu-bar">
              <template #start>
              <a href="/">
                  <img alt="logo" :src="img" height="40" class="p-mr-2">
              </a>
              </template>
              <template #end>
              
              </template>
          </Menubar>
      </nav>
  </div>
</template>

<script>
import AuthService from '../services/AuthService'
export default {
  data() {
    return{
      key: 0,
      img: require('../assets/sv_logo.png'),
      notLoggedInItems: [
        {
          label: 'Home',
          to: '/'
        },
        {
          label: 'About SCRUM',
          to: '/about-scrum'
        },
        {
          label: 'Log In',
          icon: 'pi pi-fw pi-power-off',
          to: '/login',
          class: 'media-login'
        },
      ],
      loggedInItems: [
        {
          label: 'Dashboard',
          to: '/'
        },
        {
            label: 'Projects',
            to: '/projects'
        },
        {
            label: 'Teams',
            to: '/teams'
        },
        {
          label: 'About SCRUM',
          to: '/about-scrum'
        },
        {
          label: 'My Account',
          items: [
            {
              label: 'Preview',
              to: '/me'
            },
            {
              label: 'Logout',
              to: '/',
              command: async () => {
                this.$router.push("/")
                await AuthService.logoutUser()
                window.location.reload();
              }
            }
          ]
        },
        
      ]
    }
  },
  methods:{
      isLoggedIn(){
        return AuthService.isLoggedIn()
      }
  }
}
</script>

<style>
.menu-bar{
  margin-bottom: 20px;
}
/* .menu-login{
  @media only screen and (max-width: 768px){
    position: absolute;
    right: 20px;
  } */
/* } */
</style>
