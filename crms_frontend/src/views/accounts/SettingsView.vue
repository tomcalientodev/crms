<template>

<div class="min-h-screen flex">
            <!-- Sidebar -->
    <aside class="w-1/4 bg-blue-100 text-black p-5 rounded-lg">
                <h2 class="text-xl font-bold mb-5">Settings</h2>
                <nav>
                    <ul>
                        <li>
                            <a href="owner_management"
                                class="block py-2 px-4 mb-2 hover:bg-gray-300 rounded">
                                Employee Management
                            </a>
                        </li>
                        <li>
                            <a href="#cancel-subscription" class="block py-2 px-4 hover:bg-gray-300 rounded">
                                Cancel Subscription
                            </a>
                        </li>
                    </ul>
                </nav>
    </aside>


    
        <!-- Main Content -->
    <main class="w-3/4 bg-gray-100 p-10">
    
            <!-- Employees table -->
    <div class="rounded-lg overflow-hidden md:col-span-2">
      <!-- If want table to be smaller<div class="flex-1"> -->
      <div class="overflow-x-auto">
        <h3 class="m-5 ml-8 mb-9 text-2xl font-bold text-center ">Employee Management</h3>

        <!-- For padding: <div class="bg-white border border-gray-200 rounded-lg p-4"></div> -->
        <form>
          <table class="min-w-full divide-y divide-gray-200 table-auto">

            <thead class="bg-gray-100">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Employee Name</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Phone Number</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>

            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="employee in employees" :key="employee.id">

                <td v-if="!employee.editing"
                  class="px-6 py-4 whitespace-no-wrap text-sm  font-mediu w-1/4">
                    {{ employee.user.first_name }}  {{ employee.user.last_name }}
                </td>
                <td v-else>
                  <div class="flex gap-0">
                    <input type="text" v-model="employee.user.first_name" class="border border-gray-300 rounded-lg w-20 px-2 py-1 m-1 grow">
                    <input type="text" v-model="employee.user.last_name" class="border border-gray-300 rounded-lg w-20 px-2 py-1 m-1 grow">
                  </div>
                </td>

                <td v-if="!employee.editing"
                  class="px-6 py-4 whitespace-no-wrap text-sm  font-medium w-1/4">
                    {{ employee.user.format_phone_number }}
                </td>
                <td v-else>
                  <div class="flex">
                    <input type="text" v-model="employee.user.format_phone_number" class="border border-gray-300 rounded-lg w-20 px-2 py-1 m-1 grow ">                  </div>
                </td>

                <td v-if="!employee.editing"
                  class="px-6 py-4 whitespace-no-wrap text-sm  font-medium w-1/4">
                    {{ employee.user.email }}
                </td>
                <td v-else>
                  <div class="flex">
                    <input type="text" v-model="employee.user.email" class="border border-gray-300 rounded-lg w-20 px-2 py-1 m-1 grow ">                  </div>
                </td>

                <td v-if="!employee.editing" class="px-4 py-3 whitespace-no-wrap text-sm font-medium text-gray-900">
                  <button @click="editEmployee(employee)"
                    class="text-emerald-500 hover:text-emerald-700 hover:scale-110 transition-transform duration-200">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                      stroke="currentColor" class="size-6 mr-4">
                      <path stroke-linecap="round" stroke-linejoin="round"
                        d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
                    </svg>
                  </button>

                  <button type="button" @click="showConfirmationPopup(employee.id)"
                    class="text-red-500 hover:text-red-700 hover:scale-110 transition-transform duration-200">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                      stroke="currentColor" class="size-6">
                      <path stroke-linecap="round" stroke-linejoin="round"
                        d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                    </svg>
                  </button>
                  <!-- Popup confirmation dialog -->
                  <div v-if="showPopup"
                    class="fixed top-0 left-0 w-full h-full flex items-center justify-center bg-gray-800 bg-opacity-75">
                    <div class="bg-white p-4 rounded-lg">
                      <p>Are you sure you want to delete this Employee? <p>This will delete the employees account only, so they can't log On, </p> but it will not delete the notes they took for customers.</p>
                      <div class="mt-4 flex justify-end">
                        <button @click="cancelDelete"
                          class="mr-2 px-4 py-2 bg-gray-300 text-gray-800 rounded-lg">Cancel</button>
                        <button type="button" @click.prevent="deleteEmployee()"
                          class="px-4 py-2 bg-red-500 text-white rounded-lg">
                          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                            stroke="currentColor" class="size-6">
                            <path stroke-linecap="round" stroke-linejoin="round"
                              d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                          </svg>
                        </button>
                      </div>
                    </div>
                  </div>
                </td>

                <td v-else class="px-4 py-3 whitespace-no-wrap text-sm font-medium text-gray-900">
                  <button class="px-4 py-2 mr-4 bg-green-400 text-white rounded-lg hover:bg-green-500"
                   @click="updateEmployee(employee, $event)">Save</button>
                  <button class="px-4 py-2 bg-yellow-400 text-white rounded-lg hover:bg-yellow-500"
                    @click="cancelEdit(employee)">Cancel</button>
                </td>
              </tr>
            </tbody>
          </table>
        </form>
      </div>
    </div>





    </main>
  
</div>
    
    </template>


<script setup>
import axios from 'axios';
import { ref, computed, onMounted, watch } from 'vue';
import { useUserStore } from '@/stores/user';
import { useToastStore } from '@/stores/toast';
import { useRoute } from 'vue-router';

const userStore = useUserStore();
const toastStore = useToastStore();


const employees = ref([]);

const employee = ref({
  user: {
    first_name: '',
    last_name: '',
    format_phone_number: '',
    email: '',
    organization: '',
  }
});
const originalEmail = ref('');

const route = useRoute();
const showPopup = ref(false);
const isPopoverOpen = ref(false);
const employeeId = ref('');
const originalOrganization = ref('');



////////////Employee TABLE//////////
const cancelEdit = (employee) => {
  employee.editing = false;
};

const showConfirmationPopup = (id) => {
  employeeId.value = id;
  showPopup.value = true;
};

const cancelDelete = () => {
  showPopup.value = false;
};

const getEmployees = () => {
  axios.get(`/api/accounts/employees`)
    .then((response) => {
      console.log('data', response.data);
      employees.value = response.data;
      originalEmail.value = employees.value[0].user.email;
    })
    .catch((error) => {
      console.log('error', error);
    });
};

const editEmployee = (employee) => {
  employee.editing = true;
  employee.original = { ...employee };
};

const deleteEmployee = async () => {
  try {
    const response = await axios.delete(`/api/accounts/employees/${employeeId.value}/`);
    toastStore.showToast(5000, 'Employee deleted successfully.', 'bg-green-500');
    employees.value = employees.value.filter(emp => emp.id !== employeeId.value);
  } catch (error) {
    if (error.response) {
      console.error("Error deleting Employee:", error.response.data);
      console.error("Status code:", error.response.status);
      toastStore.showToast(5000, 'Something went wrong. Please try again.', 'bg-red-500');
    } else if (error.request) {
      console.error("Error deleting Employee:", error.request);
      toastStore.showToast(5000, 'No response from server. Please try again.', 'bg-red-500');
    } else {
      console.error("Error deleting Employee:", error.message);
      toastStore.showToast(5000, 'Request error. Please try again.', 'bg-red-500');
    }
  } finally {
    showPopup.value = false;
  }
};

const updateEmployee = (employee, event) => {
  event.preventDefault();
  const dataToSubmit = {
    user: {
      first_name: employee.user.first_name,
      last_name: employee.user.last_name,
      phone_number: employee.user.format_phone_number.replace(/-/g, ''),
      ...(employee.user.email !== originalEmail.value && { email: employee.user.email }),
    },
    // organization: {
    //   organization: userStore.organization
    // },
  };
  try {
    axios.put(`/api/accounts/employees/${employee.id}/`, dataToSubmit);
    toastStore.showToast(5000, 'Employee updated successfully.', 'bg-green-500');
  } catch (error) {
    console.log("error", error);
  } finally {
    cancelEdit(employee);
  }
}




onMounted(() => {
  getEmployees();
});

</script>

