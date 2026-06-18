<template>
    <div class="flex flex-col min-h-screen">

        <nav class="py-5 px-8 border-b border-gray-200 flex-grow-1">
            <div class="max-w-7xl mx-auto">

                <div class="flex items-center justify-between">
                    <RouterLink  to="/"   class="menu-left flex items-center space-x-2">
                        <img rel="icon" src="/src/assets/websitelogo.png" class="w-8 h-8">
                        <span class="text-xl">PeachpulseCRM</span>
                    </RouterLink>


                    <div class="menu-center flex space-x-12" v-if="userStore.user.isAuthenticated && userStore.user.id">
                        
                        <!-- Home Icon-->
                        <RouterLink  :to="{ name: 'worker_dashboard', params: { workerId: userStore.user.id } }" 
                            :class="{'bg-orange-300': isActive('worker_dashboard'), 'bg-orange-100': !isActive('worker_dashboard')}"
                            class="flex items-center justify-center w-10 h-10 text-black rounded-full transition-colors duration-300 ease-in-out hover:bg-orange-300 focus:outline-none">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                stroke="currentColor" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
                            </svg>
                        </RouterLink>

                        <!-- Magnifying Glass -->
                        <RouterLink to="/search" 
                           :class="{'bg-green-300': isActive('search'), 'bg-green-100': !isActive('search')}"
                           class="flex items-center justify-center w-10 h-10 text-black rounded-full transition-colors duration-300 ease-in-out hover:bg-green-300 focus:outline-none">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                stroke="currentColor" class="w-6 h-6">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z">
                                </path>
                            </svg>
                        </RouterLink>

                        <!-- Add Button with Dropdown -->
                        <div class="relative inline-block text-left">
                            <button @click="toggleDropdown"
                                :class="{'bg-red-300': isActive('customer_creation'), 'bg-red-100': !isActive('customer_creation')}"
                                class="flex items-center justify-center w-10 h-10 text-black rounded-full transition-colors duration-300 ease-in-out hover:bg-red-300 focus:outline-none"
                                  @mouseover="resetTimeout"
                                @mouseleave="resetTimeout"
                                >
                                <!-- Blue circle button option: <button @click="toggleDropdown" class="flex items-center justify-center w-10 h-10 bg-blue-500 text-white rounded-full transition-colors duration-300 ease-in-out hover:bg-blue-600"> -->
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                    stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
                                </svg>
                            </button>
                            <div v-if="dropdownOpen"
                                class="absolute right-0 w-48 mt-2 origin-top-right bg-white border border-gray-300 rounded-lg shadow-lg"
                                  @mouseover="resetTimeout"
                                @mouseleave="resetTimeout"
                                
                                >
                                <ul>
                                    <li>
                                        <RouterLink to="/customer_creation"
                                            class="block px-4 py-2 text-gray-700 hover:bg-gray-100">
                                            Create Customer
                                        </RouterLink>
                                    </li>
                                    <li>
                                        <RouterLink to="/employee_creation"
                                            class="block px-4 py-2 text-gray-700 hover:bg-gray-100">
                                            Create Employee
                                        </RouterLink>
                                    </li>
                                </ul>
                            </div>
                        </div>

                        <!-- Settings -->
                        <RouterLink to="/settings" 
                           :class="{'bg-blue-300': isActive('search'), 'bg-blue-100': !isActive('search')}"
                           class="flex items-center justify-center w-10 h-10 text-black rounded-full transition-colors duration-300 ease-in-out hover:bg-blue-300 focus:outline-none">
                           <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.325.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 0 1 1.37.49l1.296 2.247a1.125 1.125 0 0 1-.26 1.431l-1.003.827c-.293.241-.438.613-.43.992a7.723 7.723 0 0 1 0 .255c-.008.378.137.75.43.991l1.004.827c.424.35.534.955.26 1.43l-1.298 2.247a1.125 1.125 0 0 1-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.47 6.47 0 0 1-.22.128c-.331.183-.581.495-.644.869l-.213 1.281c-.09.543-.56.94-1.11.94h-2.594c-.55 0-1.019-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 0 1-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 0 1-1.369-.49l-1.297-2.247a1.125 1.125 0 0 1 .26-1.431l1.004-.827c.292-.24.437-.613.43-.991a6.932 6.932 0 0 1 0-.255c.007-.38-.138-.751-.43-.992l-1.004-.827a1.125 1.125 0 0 1-.26-1.43l1.297-2.247a1.125 1.125 0 0 1 1.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.086.22-.128.332-.183.582-.495.644-.869l.214-1.28Z" />
                            <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                            </svg>
                        </RouterLink>

                    </div>


                    <div class="menu-right">

                        <template v-if="userStore.user.isAuthenticated && userStore.user.id">
                            <div @click="logout" v-if="userStore.user.isAuthenticated && userStore.user.id"
                                class="flex items-center justify-center hover:bg-gray-200 px-4 py-2 rounded-lg">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                                    stroke-width="1.5" stroke="currentColor" class="w-6 h-6 mr-1">
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                        d="M15.75 9V5.25A2.25 2.25 0 0 0 13.5 3h-6a2.25 2.25 0 0 0-2.25 2.25v13.5A2.25 2.25 0 0 0 7.5 21h6a2.25 2.25 0 0 0 2.25-2.25V15m3 0 3-3m0 0-3-3m3 3H9" />
                                </svg> Logout
                            </div>
                        </template>

                        <template v-else>
                            <RouterLink to="/login" class="py-4 px-6 mr-4 bg-gray-600 text-white rounded-lg">Log in
                            </RouterLink>
                            <RouterLink to="/signup_organization" class="py-4 px-6 bg-green-400 text-white rounded-lg">
                                Sign up</RouterLink>
                        </template>

                    </div>
                </div>
            </div>
        </nav>

        <div class="flex flex-1">
            <!-- <Sidebar class="w-64" v-if="userStore.user.id" /> -->

            <main :class="mainClass" class=" px-8 py-6 flex-grow">
                <RouterView @job-created="handleJobCreated" />

            </main>
        </div>

        <Toast />
    </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useToastStore } from '@/stores/toast'
import { useUserStore } from '@/stores/user'
import Toast from '@/components/Toast.vue'
import Sidebar from '@/components/Sidebar.vue'
import axios from 'axios'

const userStore = useUserStore()
const toastStore = useToastStore();
const router = useRouter()
const route = useRoute()


const dropdownOpen = ref(false)
let timeout = null



const toggleDropdown = () => {
    dropdownOpen.value = !dropdownOpen.value
    // Clear previous timeout if any
    if (timeout) {
        clearTimeout(timeout)
    }
    // Set a new timeout to close the dropdown
    if (dropdownOpen.value) {
        timeout = setTimeout(() => {
            dropdownOpen.value = false
        }, 1000) // Close the dropdown after 3 seconds
    }
}

const resetTimeout = () => {
    // Clear previous timeout if any
    if (timeout) {
        clearTimeout(timeout)
    }
    // Restart the timeout to keep the dropdown open
    if (dropdownOpen.value) {
        timeout = setTimeout(() => {
            dropdownOpen.value = false
        }, 1000) // Close the dropdown after 3 seconds
    }
}

// Initialize the store
userStore.initStore()
userStore.trackUserActivity()

// Setup axios defaults
const token = userStore.user.access
axios.defaults.headers.common["Authorization"] = token ? `Bearer ${token}` : ""


const handleJobCreated = (payload) => {
    const { lead, lead_two, jobName } = payload;
    let message = `Job "${jobName}" has been created. Employee Contacts include: ${lead}`;
    if (lead_two) {
        message += `, ${lead_two}`;
    }
    toastStore.showToast(15000, message, 'bg-green-500');
};

const logout = () => {
    userStore.removeToken();
    router.push('/login')
};

//Controls background colors of pages on site.
const mainClass = computed(() => {
    switch (route.name) {
        case 'customer_view':
            return 'bg-rose-50';
        case 'worker_dashboard':
            return 'bg-gray-50';
        default:
            return 'bg-gray-100';
    }
});

const isActive = (routeName) => {
    return route.name === routeName
}

</script>