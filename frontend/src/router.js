import { createWebHistory, createRouter } from "vue-router";
import AuthService from './services/AuthService'

// import useProjects from './store/projects'
// import useTeams from './store/teams'
// const {selectedProject} = useProjects()
// const {selectedTeam} = useTeams()

const routes = [
    {
        path: "/",
        name: "home",
        component: () => import("./views/Home"),
        meta: {
            isProtected: false
        }
    },
    {
        path: "/projects",
        name: "projects",
        component: () => import("./views/Projects"),
        meta: {
            isProtected: true
        }
    },
    {
        path: "/projects/view",
        name: "projectView",
        component: () => import("./views/ProjectView"),
        meta: {
            isProtected: true
        }
    },
    {
        path: "/teams",
        name: "teams",
        component: () => import("./views/Teams"),
        meta: {
            isProtected: true
        }
    },
    {
        path: "/teams/view",
        name: "teamView",
        component: () => import("./views/TeamView"),
        meta: {
            isProtected: true
        }
    },
    {
        path: "/about-scrum",
        name: "about-scrum",
        component: () => import("./views/AboutScrum"),
        meta: {
            isProtected: false
        }
    },
    {
        path: "/login",
        name: "login",
        component: () => import("./views/Login"),
        meta: {
            isProtected: false
        }
    },
    {
        path: "/register",
        name: "register",
        component: () => import("./views/Register"),
        meta: {
            isProtected: false
        }
    },
    {
        path: "/me",
        name: "me",
        component: () => import("./views/User"),
        meta: {
            isProtected: true
        }
    },
    {
        path: "/user/:username",
        name: "user",
        component: () => import("./views/UserPublic"),
        meta: {
            isProtected: true
        }
    },
    {
        path: "/:pathMatch(.*)*",
        component: () => import("./views/404"),
        meta: {
            isProtected: false
        }
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
  });

router.beforeEach((to, from, next) => {
    if (to.name == 'login' && AuthService.isLoggedIn()) {
        next({ path: '/' })
    }
    else if (to.meta.isProtected && !AuthService.isLoggedIn()) {
        next({
            path: '/login'
        })
    }
    else if (to.name == 'projectView' && from.name == 'projectView'){
        console.log('aaa')
        next({
            path: '/projects'
        })
    }
    else if (to.name == 'teamView' && from.name == 'teamView'){
        console.log('bbb')
        next({
            path: '/teams'
        })
    }
    else {
        next()
    }
})

// router.beforeResolve(async to =>{
    
// })

export default router;