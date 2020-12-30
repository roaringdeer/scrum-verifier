import {createApp, defineAsyncComponent} from 'vue'
import App from './App.vue'
import router from './router'

//importing primevue css resources
import 'primeflex/primeflex.css'
import 'primevue/resources/themes/saga-blue/theme.css'       //theme
// import 'primevue/resources/themes/vela-blue/theme.css'       //theme

import 'primevue/resources/primevue.min.css'                 //core css
import 'primeicons/primeicons.css'                           //icons

import PrimeVue from 'primevue/config';

//importing primevue components
import Calendar from 'primevue/calendar'
import Menubar from 'primevue/menubar'
import TabMenu from 'primevue/tabmenu'
import Card from 'primevue/card'
import Button from 'primevue/button'
import SplitButton from 'primevue/splitbutton'
import Panel from 'primevue/panel'
import InputText from 'primevue/inputtext'
import Password from 'primevue/password'
import Dialog from 'primevue/dialog'
import BlockUI from 'primevue/blockui';
import PanelMenu from 'primevue/panelmenu'
import Listbox from 'primevue/listbox'
import Tree from 'primevue/tree';
import TabView from 'primevue/tabview';
import TabPanel from 'primevue/tabpanel';
import Inplace from 'primevue/inplace';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import ProgressBar from 'primevue/progressbar';
import Textarea from 'primevue/textarea'
import ProgressSpinner from 'primevue/progressspinner'
import Tag from 'primevue/tag'
import RadioButton from 'primevue/radiobutton';
import SelectButton from 'primevue/selectbutton';
import OverlayPanel from 'primevue/overlaypanel';
import Dropdown from 'primevue/dropdown';
import Sidebar from 'primevue/sidebar';
import Divider from 'primevue/divider';
import Checkbox from 'primevue/checkbox';
import Knob from 'primevue/knob';
import Chart from 'primevue/chart';
import ScrollPanel from 'primevue/scrollpanel';
import InputNumber from 'primevue/inputnumber';
import MultiSelect from 'primevue/multiselect';
import Badge from 'primevue/badge';
import Tooltip from 'primevue/tooltip';
import FullCalendar from 'primevue/fullcalendar';
import InputSwitch from 'primevue/inputswitch';
import Avatar from 'primevue/avatar';
import AvatarGroup from 'primevue/avatargroup';
import OrderList from 'primevue/orderlist';
import FileUpload from 'primevue/fileupload';
import Accordion from 'primevue/accordion';
import AccordionTab from 'primevue/accordiontab';
// import Chip from 'primevue/chip';

//importing own components
import NavBar from './components/NavBar';
import Dashboard from './components/Dashboard';
// import TeamView from './components/TeamView';
import TeamTabs from './components/TeamTabs';
import TeamInfo from './components/TeamInfo';
// import ProjectInfo from './components/ProjectInfo';
// import ProjectCardsList from './components/ProjectCardsList';

import ProjectTabs from './components/ProjectTabs';
import TaskCard from './components/TaskCard'
import TeamCard from './components/TeamCard'
import ProjectCard from './components/ProjectCard'
import SomethingWentWrong from './components/SomethingWentWrong'
// import ProjectMembers from './components/ProjectMembers'
// import ProjectStats from './components/ProjectStats'
import MemberCard from './components/MemberCard.vue'
import UserProfile from './components/UserProfile.vue'
import RoleTag from './components/RoleTag.vue'
import InfoButton from './components/InfoButton.vue'
import ScrumInfo from './components/ScrumInfo.vue'
import Landing from './components/Landing.vue'
import EventInfo from './components/EventInfo.vue'

//importing own async components
const TeamsSidebar = defineAsyncComponent(() =>
  import('./components/TeamsSidebar.vue')
)
const ProjectsSidebar = defineAsyncComponent(() =>
  import('./components/ProjectsSidebar.vue')
)
const TeamProjectsTable = defineAsyncComponent(() =>
  import('./components/TeamProjectsTable.vue')
)
const TeamMembersTable = defineAsyncComponent(() =>
  import('./components/TeamMembersTable.vue')
)
const Tasks = defineAsyncComponent(() =>
  import('./components/Tasks.vue')
)
const ProjectInfo = defineAsyncComponent(() =>
  import('./components/ProjectInfo.vue')
)
const ProjectMembers = defineAsyncComponent(() =>
  import('./components/ProjectMembers.vue')
)
const ProjectStats = defineAsyncComponent(() =>
  import('./components/ProjectStats.vue')
)
const ProjectCalendar = defineAsyncComponent(() =>
  import('./components/ProjectCalendar.vue')
)
const ProjectCardsList = defineAsyncComponent(() =>
  import('./components/ProjectCardsList.vue')
)
const TeamCardsList = defineAsyncComponent(() =>
  import('./components/TeamCardsList.vue')
)
const UserProfilePublic = defineAsyncComponent(() =>
  import('./components/UserProfilePublic.vue')
)

const app = createApp(App).use(router)

app.use(PrimeVue);

//adding Primevue components
app.component('Calendar', Calendar)
app.component('Menubar', Menubar)
app.component('TabMenu', TabMenu)
app.component('Card', Card)
app.component('Button', Button)
app.component('SplitButton', SplitButton)
app.component('Panel', Panel)
app.component('InputText', InputText)
app.component('Password', Password)
app.component('Dialog', Dialog)
app.component('BlockUI', BlockUI)
app.component('PanelMenu', PanelMenu)
app.component('Listbox', Listbox)
app.component('Tree', Tree)
app.component('TabView', TabView)
app.component('TabPanel', TabPanel)
app.component('Inplace', Inplace)
app.component('DataTable', DataTable)
app.component('Column', Column)
app.component('ProgressBar', ProgressBar)
app.component('Textarea', Textarea)
app.component('ProgressSpinner', ProgressSpinner)
app.component('Tag', Tag)
app.component('RadioButton', RadioButton)
app.component('SelectButton', SelectButton)
app.component('OverlayPanel', OverlayPanel)
app.component('Dropdown', Dropdown)
app.component('Sidebar', Sidebar)
app.component('Divider', Divider)
app.component('Checkbox', Checkbox)
app.component('Knob', Knob)
app.component('Chart', Chart)
app.component('ScrollPanel', ScrollPanel)
app.component('InputNumber', InputNumber)
app.component('MultiSelect', MultiSelect)
app.component('Badge', Badge)
app.component('FullCalendar', FullCalendar)
app.component('InputSwitch', InputSwitch)
app.component('Avatar', Avatar)
app.component('AvatarGroup', AvatarGroup)
app.component('OrderList', OrderList)
app.component('FileUpload', FileUpload)
app.component('Accordion', Accordion)
app.component('AccordionTab', AccordionTab)
// app.component('Chip', Chip)

// adding directive
app.directive('tooltip', Tooltip)

//adding own components
app.component('NavBar', NavBar)
app.component('Dashboard', Dashboard)
// app.component('TeamView', TeamView)
app.component('TeamTabs', TeamTabs)
app.component('TeamInfo', TeamInfo)
// app.component('ProjectView', ProjectView)
app.component('ProjectTabs', ProjectTabs)
app.component('TaskCard', TaskCard)
app.component('TeamCard', TeamCard)
app.component('ProjectCard', ProjectCard)
app.component('UserProfile', UserProfile)
app.component('SomethingWentWrong', SomethingWentWrong)
app.component('MemberCard', MemberCard)
app.component('RoleTag', RoleTag)
app.component('InfoButton', InfoButton)
app.component('ScrumInfo', ScrumInfo)
app.component('Landing', Landing)
app.component('EventInfo', EventInfo)

//adding own async components
app.component('TeamsSidebar', TeamsSidebar)
app.component('ProjectsSidebar', ProjectsSidebar)
app.component('TeamProjectsTable', TeamProjectsTable)
app.component('TeamMembersTable', TeamMembersTable)
app.component('Tasks', Tasks)
app.component('ProjectInfo', ProjectInfo)
app.component('ProjectCalendar', ProjectCalendar)
app.component('ProjectCardsList', ProjectCardsList)
app.component('TeamCardsList', TeamCardsList)

app.component('ProjectMembers', ProjectMembers)
app.component('ProjectStats', ProjectStats)
app.component('UserProfilePublic', UserProfilePublic)


app.mount('#app')



// app.config.globalProperties.$primevue = {ripple: true}; //add ripple animation

// app.mount('#app')


// // Polyfills
// import 'core-js/stable'
// import 'regenerator-runtime/runtime'

// // Imports
// import Vue from 'vue'
// import vuetify from '@/plugins/vuetify'

// new Vue({ vuetify }).$mount('#app')