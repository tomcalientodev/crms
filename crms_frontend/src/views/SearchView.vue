<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-left col-span-3 space-y-4">
            <div class="bg-white border border-gray-200 rounded-lg">
                <!--Search User Form-->
                <form v-on:submit.prevent="submitForm" class="p-4 flex space-x-4">  
                    <input v-model="query" type="search" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="Search by Customer Name, Email or Phone #, or Job Name">

                    <button href="#" class="inline-block py-4 px-6 bg-orange-400 hover:bg-orange-500 text-white rounded-lg">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                            stroke="currentColor" class="w-6 h-6">
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"></path>
                        </svg>
                    </button>
                </form>
            </div>

             <!-- Searched Users-->
            <div class="p-4 bg-white border border-gray-200 rounded-lg  gap-4 flex flex-wrap"
                v-if="customers.length">
                <div 
                    class="p-4 text-center bg-gray-100 rounded-lg"
                    v-for="customer in customers"
                    v-bind:key="customer.id"
                    >
                    <p>
                        <RouterLink :to="{name: 'customer_view', params: {'customerId': customer.id}}" class="text-blue-600 hover:underline">
                            {{ customer.user.first_name}}
                            {{ customer.user.last_name}} - 
                            {{ customer.user.email}} -
                            {{ customer.user.format_phone_number}}
                        </RouterLink>
                    </p>
                </div>
            </div>

            <!-- Searched Jobs-->
            <div class="p-4 bg-white border border-gray-200 rounded-lg  gap-4 flex flex-wrap"
                v-if="jobs.length">
                <h2 class="w-full text-xl font-bold mb-4">Jobs</h2>
                <div 
                    class="p-4 text-center bg-gray-100 rounded-lg"
                    v-for="job in jobs" v-bind:key="job.id" >
                    <p>
                       <RouterLink :to="{name: 'job_notes_view', params: {'customerId': job.related_customer.id, 'jobId': job.id }}" class="text-blue-600 hover:underline">
                            {{ job.name }}
                        </RouterLink> 
                    </p>
                </div>
            </div>
    </div>

        <div class="main-right col-span-1 space-y-4">
            <!-- Space for components. -->
        </div>
    </div>
</template>


<script>
import axios from 'axios'

export default {
    name: 'SearchView',

    data() {
        return { 
            query: '',
            customers: [],
            jobs: [],
        }
    },

    methods: {
        submitForm() {
            console.log('submitForm', this.query)

            axios
                .post('/api/search/', {
                    query: this.query
                })
                .then(response => {
                    console.log('response:', response.data)

                    this.customers = response.data.customers
                    this.jobs = response.data.jobs

                })
                .catch(error => {
                    console.log('error:', error)
                })

        }
    }
}
</script>
