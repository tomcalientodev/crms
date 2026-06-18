<template>
  <div class="overflow-y-auto overflow-x-hidden">

    <div class="flex items-center justify-left ml-5 h-14 mt-4 ">
      <!-- <div class="text-sm"> Logged on as {{userStore.user.first_name}} {{userStore.user.last_name}} for {{userStore.user.organization_name}}</div> -->
      <div class="px-2 py-0.5 mr-1 text-sm font-medium tracking-wide text-orange-500 bg-red-50">
        Welcome, {{ userStore.user.first_name }} {{ userStore.user.last_name }} of {{ userStore.user.organization_name }}!
      </div>
    </div>

    <ul class="flex flex-col py-1 space-y-1">
      <li class="px-5 mt-5">
        <div class="flex flex-row items-center h-5">
          <div class="text-sm font-light tracking-wide text-gray-500">Worker Menu</div>
        </div>
      </li>

      <li>
        <RouterLink :to="{ name: 'worker_dashboard', params: { workerId: userStore.user.id } }">
          <div
            class="relative flex flex-row items-center h-11 focus:outline-none hover:bg-gray-50 text-gray-600 hover:text-gray-800 border-l-4 border-transparent hover:border-green-200 pr-6">
            <span class="inline-flex justify-center items-center ml-4">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6">
                </path>
              </svg>
            </span>
            <span class="ml-2 text-sm tracking-wide truncate">Worker Dashboard</span>
          </div>
        </RouterLink>
      </li>

      <li>
        <RouterLink to="/customer_creation"
          class="relative flex flex-row items-center h-11 focus:outline-none hover:bg-gray-50 text-gray-600 hover:text-gray-800 border-l-4 border-transparent hover:border-green-200 pr-6">
          <span class="inline-flex justify-center items-center ml-4">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
              stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="M18 7.5v3m0 0v3m0-3h3m-3 0h-3m-2.25-4.125a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0ZM3 19.235v-.11a6.375 6.375 0 0 1 12.75 0v.109A12.318 12.318 0 0 1 9.374 21c-2.331 0-4.512-.645-6.374-1.766Z" />
            </svg>
          </span>
          <span class="ml-2 text-sm tracking-wide truncate">Customer <p>Creation</p></span>
        </RouterLink>
      </li>


      <li v-if="isOrganizationOwner">
        <RouterLink to="/employee_creation"
          class="relative flex flex-row items-center h-11 focus:outline-none hover:bg-gray-50 text-gray-600 hover:text-gray-800 border-l-4 border-transparent hover:border-green-200 pr-6">
          <span class="inline-flex justify-center items-center ml-4">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
              stroke="currentColor" class="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="M18 7.5v3m0 0v3m0-3h3m-3 0h-3m-2.25-4.125a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0ZM3 19.235v-.11a6.375 6.375 0 0 1 12.75 0v.109A12.318 12.318 0 0 1 9.374 21c-2.331 0-4.512-.645-6.374-1.766Z" />
            </svg>
          </span>
          <span class="ml-2 text-sm tracking-wide truncate">Employee <p>Creation</p></span>
        </RouterLink>
      </li>


      <!-- TODO: Try using emit to make this faster,  or just gettingin with axios, or combining  watchersinto one.   -->  
      <li class="px-5 py-5" v-if="customerFirstName" >
        <div class="flex flex-row items-center h-5">
          <div class="text-sm font-light tracking-wide text-gray-500">Customer Menu for  {{ customerFirstName  }} {{ customerLastName  }}</div>
        </div>
      </li>

      <li class="px-5 py-5" v-else="!customerFirstName" >
        <div class="flex flex-row items-center h-5">
          <div class="text-sm font-light tracking-wide text-gray-500">Customer Menu </div>
        </div>
      </li>

      <!-- <li  v-if="!customerId">
          <span class="ml-2 text-sm tracking-wide truncate">Customer Options will be displayed once you visit a customers pages.</span>
      </li> -->

      <div  v-if="!customerId" class="flex items-center justify-left ml-5 h-14 mt-1 ">
        <div class="px-2 py-0.5 mr-1 text-sm font-medium tracking-wide text-orange-300 bg-red-50">
          View Customers or Jobs for Customer Menu to display.
        </div>
      </div>

      <li  v-if="customerId">
        <RouterLink :to="{ name: 'misc_note', params: { customerId: customerId } }"
          class="relative flex flex-row items-center h-1 focus:outline-none hover:bg-gray-50 text-gray-600 hover:text-gray-800 border-l-4 border-transparent hover:border-green-200 pr-6">
          <span class="inline-flex justify-center items-center ml-4">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
            </svg>
          </span>
          <span class="ml-2 text-sm tracking-wide truncate">Notes</span>
        </RouterLink>
      </li>








<!-- 
        <li>
        <a href="#"
          class="relative flex flex-row items-center h-11 focus:outline-none hover:bg-gray-50 text-gray-600 hover:text-gray-800 border-l-4 border-transparent hover:border-green-200 pr-6">
          <span class="inline-flex justify-center items-center ml-4">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9">
              </path>
            </svg>
          </span>
          <span class="ml-2 text-sm tracking-wide truncate">Notifications</span>
          <span class="px-2 py-0.5 ml-auto text-xs font-medium tracking-wide text-red-500 bg-red-50 rounded-full">Coming Soon</span>
        </a>
      </li> 


     <li class="px-5">
        <div class="flex flex-row items-center h-8">
          <div class="text-sm font-light tracking-wide text-gray-500">Settings</div>
        </div>
      </li>

      <li>
        <a href="#"
          class="relative flex flex-row items-center h-11 focus:outline-none hover:bg-gray-50 text-gray-600 hover:text-gray-800 border-l-4 border-transparent hover:border-indigo-500 pr-6">
          <span class="inline-flex justify-center items-center ml-4">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
            </svg>
          </span>
          <span class="ml-2 text-sm tracking-wide truncate">Profile (Coming Soon)</span>
        </a>
      </li>

      <li>
        <a href="#"
          class="relative flex flex-row items-center h-11 focus:outline-none hover:bg-gray-50 text-gray-600 hover:text-gray-800 border-l-4 border-transparent hover:border-indigo-500 pr-6">
          <span class="inline-flex justify-center items-center ml-4">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z">
              </path>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
            </svg>
          </span>
          <span class="ml-2 text-sm tracking-wide truncate">Settings</span>
        </a>
      </li>

      <li>
        <div
          class="relative flex flex-row items-center h-11 focus:outline-none hover:bg-gray-50 text-gray-600 hover:text-gray-800 border-l-4 border-transparent hover:border-indigo-500 pr-6">
          <span class="inline-flex justify-center items-center ml-4">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
            </svg>
          </span>
          <span class="ml-2 text-sm tracking-wide truncate">Logout</span>
        </div>
      </li>  -->

    </ul>
  </div>


</template>


<script setup>
import { useUserStore } from '@/stores/user'
import { ref, onMounted, watch } from 'vue'; // Import ref from Vue
import axios from 'axios';

const userStore = useUserStore();
const isOrganizationOwner = ref(false); // Define reactive variable for isOrganizationOwner
const customerId = ref(null);
const customerFirstName = ref(null);
const customerLastName = ref(null);

const getUserPermissions = () => { // Define getUserPermissions as a function
  axios.get('/api/accounts/owner_permissions/')
    .then(response => {
      console.log('User permissions:', response.data);
      isOrganizationOwner.value = response.data.is_organization_owner; // Update reactive variable
    })
    .catch(error => {
      console.error('Error fetching user permissions:', error);
    });
};

// Get customerId from localStorage
const getCustomerFromLocalStorage = () => {
  const storedCustomerId = localStorage.getItem('customerId');
  const storedCustomerFirstName = localStorage.getItem('customer_first_name');
  const storedCustomerLastName = localStorage.getItem('customer_last_name');

  customerId.value = storedCustomerId ? storedCustomerId : null; // Update reactive variable
  customerFirstName.value = storedCustomerFirstName ? storedCustomerFirstName : null;
  customerLastName.value = storedCustomerLastName ? storedCustomerLastName : null;
};


// Watchers for customerId, customerFirstName, and customerLastName
watch(() => userStore.customerId, (newCustomerId) => {
  customerId.value = newCustomerId;
});

watch(() => userStore.customerFirstName, (newCustomerFirstName) => {
  customerFirstName.value = newCustomerFirstName;
});

watch(() => userStore.customerLastName, (newCustomerLastName) => {
  customerLastName.value = newCustomerLastName;
});




onMounted(() => {
  getUserPermissions();
  getCustomerFromLocalStorage();
});


</script>
