import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SignupOrganizationView from '../views/accounts/SignupOrganizationView.vue'
import PrivacyandTerms from '../views/PrivacyAndTerms.vue'
import LoginView from '../views/accounts/LoginView.vue'
import CustomerCreationView from '../views/accounts/CustomerCreationView.vue'
import EmployeeCreationView from '../views/accounts/EmployeeCreationView.vue'
import SearchView from '../views/SearchView.vue'

import ForgotPassword from '../views/accounts/ForgotPassword.vue'

import MiscNoteView from '../views/notes/MiscNoteView.vue'
import CustomerView from '../views/CustomerView.vue'
import JobCreationView from '../views/JobCreationView.vue'
import JobNoteCreationView from '../views/notes/JobNoteCreationView.vue'
import JobDetailView from '../views/JobDetailView.vue'
import JobNotesView from '../views/notes/JobNotesView.vue'

import WorkerDashboardView from '../views/WorkerDashboardView.vue'

import Settings from '../views/accounts/SettingsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/signup_organization',
      name: 'signup_organization',
      component: SignupOrganizationView
    },
    {
      path: '/privacyandterms',
      name: 'privacyandterms',
      component: PrivacyandTerms,
    },
    {
      path: '/customer_creation',
      name: 'customer_creation',
      component: CustomerCreationView
    },
    {
      path: '/employee_creation',
      name: 'employee_creation',
      component: EmployeeCreationView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/search',
      name: 'search',
      component: SearchView
    },
    {
      path: '/customer_view/:customerId/',
      name: 'customer_view',
      component: CustomerView
    },
    {
      path: '/misc_note/:customerId/',
      name: 'misc_note',
      component: MiscNoteView
    },
    {
      path: '/job_creation/:customerId/',
      name: 'job_creation',
      component: JobCreationView
    },
    {
      path: '/job_note_creation/:customerId/:jobId/',
      name: 'job_note_creation',
      component: JobNoteCreationView
    },
    {
    path: '/job_detail_view/:customerId/',
    name: 'job_detail_view',
    component: JobDetailView
  },
  {
    path: '/job_notes_view/:customerId/:jobId/',
    name: 'job_notes_view',
    component: JobNotesView
  },
  {
    path: '/worker_dashboard/:workerId/',
    name: 'worker_dashboard',
    component: WorkerDashboardView,
    props: true
  },
  {
    path: '/settings',
    name: 'settings',
    component: Settings,
  },
  {
    path: '/forgot_password',
    name: 'forgot_password',
    component: ForgotPassword,
  },



  ]
})

export default router
