<template>
  <main class="p-6 sm:p-1 space-y-6">
    <section class="grid gap-6">

      <!-- User Info Box-->
      <div class="flex items-center p-5 bg-white shadow rounded-lg max-w-xs sm:max-w-sm md:max-w-md lg:max-w-lg xl:max-w-xl mx-auto">
        <div>
          <span class="text-2xl font-bold mr-3" v-if="user">{{ user.first_name }} {{ user.last_name }} -</span>
          <span class="text-gray-500">{{ user.organization_name }}</span>
        </div>
      </div>

      <div class="grid md:grid-cols-2 gap-6">

        <!-- Recently Viewed Customers Box-->
        <div class="bg-white shadow rounded-lg">
          <div class="flex items-center justify-between px-6 py-5 font-semibold border-b border-gray-100">
            <span>Recently Viewed Customers</span>
          </div>

          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead>
                <tr>
                  <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Customer Name
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="cust in customers" :key="cust.id">
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-blue-600">
                    <RouterLink :to="{ name: 'customer_view', params: { customerId: cust.customer.id } }"
                      class="inline-block hover:text-blue-800 hover:underline">
                      {{ cust.customer.user.first_name }} {{ cust.customer.user.last_name }}
                    </RouterLink>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <!-- Recently Viewed Customers Box END-->

      <!-- All Customers Table -->
      <div class="bg-white shadow rounded-lg">
        <div class="flex items-center justify-between px-6 py-5 font-semibold border-b border-gray-100">
          <span>All Customers</span>
          <div>
            <button @click="sortBy('first_name')" class="px-4 py-2 mr-2 bg-red-200 hover:bg-red-300 rounded">Sort by First Name</button>
            <button @click="sortBy('last_name')" class="px-4 py-2 bg-orange-200 hover:bg-orange-300 rounded">Sort by Last Name</button>
          </div>
        </div>
        <div class="px-6 py-4">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Search Customers"
            class="w-full px-4 py-2 border rounded"
          />
        </div>
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead>
              <tr>
                <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  First Name
                </th>
                <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Last Name
                </th>
                <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Email
                </th>
                <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Phone
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="cust in filteredCustomers" :key="cust.id">

                <td class="px-6 py-4 whitespace-nowrap text-sm text-blue-600">
                    <RouterLink
                      :to="{ name: 'customer_view', params: { customerId: cust.id } }"
                      class="inline-block hover:text-blue-800 hover:underline">
                      {{ cust.user.first_name }}
                    </RouterLink>
                  </td>

                  <td class="px-6 py-4 whitespace-nowrap text-sm text-blue-600">
                    <RouterLink
                      :to="{ name: 'customer_view', params: { customerId: cust.id } }"
                      class="inline-block hover:text-blue-800 hover:underline">
                      {{ cust.user.last_name }}
                    </RouterLink>
                  </td>
               
                <td class="px-6 py-4 whitespace-nowrap text-sm">{{ cust.user.email }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm">{{ cust.user.format_phone_number }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <!-- All Customers Table END-->


        <!-- Your Jobs Box-->
        <div class="bg-white shadow rounded-lg">
          <div class="flex items-center justify-between px-6 py-5 font-semibold border-b border-gray-100">
            <span>Your Jobs</span>
          </div>

          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead>
                <tr>
                  <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Job Name
                  </th>
                  <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Customer
                  </th>
                  <th class="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Due Date
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="job in jobs" :key="job.id">
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-blue-600">
                    <RouterLink
                      :to="{ name: 'customer_view', params: { customerId: job.related_customer.id } }"
                      class="inline-block hover:text-blue-800 hover:underline">
                      {{ job.name }}
                    </RouterLink>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-semibold">
                    {{ job.status }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-semibold">
                    {{ job.related_customer.user.first_name}} {{ job.related_customer.user.last_name}}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-semibold">
                    {{ job.due_date }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <!-- Your Jobs Box END-->

      </div>
    </section>
  </main>
</template>


<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useRoute } from "vue-router";


const user = ref({});
const jobs = ref([]);
const customers = ref([]);
const all_customers = ref([]);
const searchQuery = ref('');
const route = useRoute();
const sortOrder = ref('asc');
const sortKey = ref('');

const getUser = async () => {
  try {
    const response = await axios.get(`/api/accounts/user_info/`);
    user.value = response.data;
    await getJobs(); // Call getJobs() after fetching user info
  } catch (error) {
    console.error("Error fetching user info:", error);
  }
};

const getJobs = async () => {
  try {
    const response = await axios.get(`/api/dashboards/${route.params.workerId}/lead_jobs/`);
    console.log("response.data.jobs", response.data.jobs);
    jobs.value = response.data.jobs;
  } catch (error) {
    console.error("Error fetching jobs:", error);
  }
};

const getRecentlyViewedCustomers = async () => {
  try {
    const response = await axios.get(`/api/dashboards/recently_viewed_customers/${route.params.workerId}/`);
    customers.value = response.data;
  } catch (error) {
    console.error("Error fetching recently viewed customers:", error);
  }
};


const getAllCustomers = async () => {
  try {
    const response = await axios.get(`/api/search/all_customers`);
    console.log("response.data.all_customers", response.data.all_customers);
    all_customers.value = response.data.all_customers;
  } catch (error) {
    console.error("Error fetching all customers:", error);
  }
}

const sortBy = (key) => {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
  } else {
    sortKey.value = key;
    sortOrder.value = 'asc';
  }
};

const filteredCustomers = computed(() => {
  let result = [...all_customers.value]; 

    if (searchQuery.value) {
      result = result.filter(cust =>
        cust.user.first_name.toLowerCase().startsWith(searchQuery.value.toLowerCase()) ||
        cust.user.last_name.toLowerCase().startsWith(searchQuery.value.toLowerCase()) 
      );
    }

    if (sortKey.value) {
    result = result.sort((a, b) => {
      let modifier = sortOrder.value === 'asc' ? 1 : -1;
      const aValue = a.user[sortKey.value].toLowerCase();
      const bValue = b.user[sortKey.value].toLowerCase();
      if (aValue < bValue) return -1 * modifier;
      if (aValue > bValue) return 1 * modifier;
      return 0;
    });
  }
      return result;
    });


onMounted(() => {
  getUser();
  getRecentlyViewedCustomers();
  getAllCustomers();
});
</script>