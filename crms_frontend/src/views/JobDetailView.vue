<template>

    <div class="top-0 left-0 mb-5 ml-0 space-x-4">
        <div class="hidden md:flex md:space-x-5 list-none">
            <li>
                <RouterLink :to="{ name: 'misc_note', params: { customerId: customer.id } }"
                    class="text-base font-normal text-gray-500 list-none hover:text-gray-900 flex items-center">

                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="w-4 h-4">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5 3 12m0 0 7.5-7.5M3 12h18" />
                    </svg>
                    <span class="ml-2">Back to Notes</span> </RouterLink>
            </li>
        </div>
    </div>

    <main class="px-4 md:px-8 py-4 md:py-0 bg-gr-100">
        <div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-4">

            <!-- The Customer INfo BOX -->
            <div class="main-left md:col-span-1">
                <div class="p-4 bg-white border border-gray-200 text-center rounded-lg"
                    v-if="customer && customer.user">
                    <p><strong>{{ customer.user.first_name }} {{ customer.user.last_name }}</strong></p>

                    <div class="mt-6 flex flex-col md:justify-around">

                        <p class="text-xs text-gray-500">{{ customer.user.phone_number }}</p>
                        <p class="text-xs text-gray-500">{{ customer.user.email }}</p>
                    </div>
                    <br></br>
                    <RouterLink :to="{ name: 'job_creation', params: { customerId: customer.id } }">
                        <button class="py-3 px-6 bg-green-400 text-white rounded-lg hover:bg-green-500 mb-3">
                            Add Job
                        </button>
                    </RouterLink>
                    <br></br>
                    <!-- <RouterLink :to="{ name: 'misc_note', params: { customerId: customer.id } }">
                        <button class="py-3 px-6 bg-green-400 text-white rounded-lg hover:bg-green-500">
                            Notes
                        </button>
                    </RouterLink> -->

                </div>
            </div>

            <!-- Jobs table -->
            <div class="row-span-3 bg-white shadow rounded-lg overflow-hidden md:col-span-3">
                <div class="overflow-x-auto">
                    <form>
                        <table class="min-w-full divide-y divide-gray-200 table-auto">

                            <thead class="bg-gray-100">
                                <tr>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Job Name</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Primary Contact</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Secondary Contact</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Due Date</th>
                                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                                </tr>
                            </thead>

                            <tbody class="bg-white divide-y divide-gray-200">
                                <tr v-for="job in jobs" :key="job.id">

                                    <td v-if="!job.editing"
                                        class="px-6 py-4 whitespace-no-wrap text-sm  font-medium text-blue-600 hover:underline w-1/4">
                                        <RouterLink
                                            :to="{ name: 'job_notes_view', params: { customerId: customer.id, jobId: job.id } }">
                                            {{ job.name }}
                                        </RouterLink>
                                    </td>
                                    <td v-else>
                                        <input type="text" v-model="job.name"
                                            class="border border-gray-300 rounded-lg w-40 px-2 py-1">
                                    </td>

                                    <td v-if="!job.editing"
                                        class="px-6 py-2 whitespace-no-wrap text-sm font-medium text-gray-900">
                                        {{ job.status }}
                                    </td>
                                    <td v-else>
                                            <select id="job_status" v-model="selectedStatus"
                                                 class="w-full border border-gray-300 rounded-lg py-1 px-2">
                                                <option value="">Select</option>
                                                <option v-for="option in sortedJobStatusOptions" :value="option.value"
                                                    :key="option.value">{{ option.label }}</option>
                                            </select>
                                    </td>

                                    <td v-if="!job.editing"
                                        class="px-6 py-4 whitespace-no-wrap text-sm font-medium text-gray-900 ">
                                        {{ job.lead ? `${job.lead.first_name} ${job.lead.last_name}` : '' }}
                                    </td>
                                    <td v-else>
                                            <select id="job_lead" v-model.lazy="selectedLead"
                                                class="w-full border border-gray-300 rounded-lg py-1 px-2">
                                                <option value="">Select</option>
                                                <option v-for="option in sortedJobLeadOptions" :value="option.value"
                                                    :key="option.value">{{ option.label }}
                                                </option>
                                            </select>  
                                    </td>

                                    <td v-if="!job.editing"
                                        class="px-6 py-4 whitespace-no-wrap text-sm font-medium text-gray-900 ">
                                        {{ job.lead_two ? `${job.lead_two.first_name} ${job.lead_two.last_name}` : '' }}
                                    </td>
                                    <td v-else>
                                            <select id="job_lead_two" v-model.lazy="selectedLeadTwo"
                                                class="w-full border border-gray-300 rounded-lg py-1 px-2">
                                                <option value="">Select</option>
                                                <option v-for="option in sortedJobLeadOptions" :value="option.value"
                                                    :key="option.value">{{ option.label }}
                                                </option>
                                            </select>  
                                    </td>


                                    <td v-if="!job.editing"
                                        class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                                        {{ job.due_date }}
                                    </td>
                                    <td v-else>
                                        <input type="date" v-model="job.due_date"
                                            class="border border-gray-300 rounded-lg w-full px-2 py-1">
                                    </td>

                                    <td v-if="!job.editing" class="px-4 py-3 whitespace-no-wrap text-sm font-medium text-gray-900">
                
                                        <button @click="editJob(job)" class="text-emerald-500 hover:text-emerald-700">
                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                                stroke="currentColor" class="size-6">
                                                <path stroke-linecap="round" stroke-linejoin="round"
                                                    d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
                                            </svg>
                                        </button>

                                        <!-- <button class="px-4 py-2 bg-red-400 text-white rounded-lg hover:bg-red-500"
                                            @click.prevent="deleteJob(job.id)">Delete</button> -->

                                            <button type="button" @click="showConfirmationPopup(job.id)" class="text-red-500 hover:text-red-700">
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
                                                    <p>Are you sure you want to delete this note?</p>
                                                    <div class="mt-4 flex justify-end">
                                                        <button @click="cancelDelete"
                                                            class="mr-2 px-4 py-2 bg-gray-300 text-gray-800 rounded-lg">Cancel</button>
                                                        <button type="button" @click.prevent="deleteJob()" class="px-4 py-2 bg-red-500 text-white rounded-lg">
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
                                    <td v-else
                                        class="px-4 py-3 whitespace-no-wrap text-sm font-medium text-gray-900">
                                        <button
                                            class="px-4 py-2 mr-4 bg-green-400 text-white rounded-lg hover:bg-green-500"
                                            @click="submitForm(job, $event)">Save</button>
                                        <button class="px-4 py-2 bg-yellow-400 text-white rounded-lg hover:bg-yellow-500"
                                            @click="cancelEdit(job)">Cancel</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </form>
                </div>
            </div>


        </div>
    </main>
</template>




<script setup>
import axios from 'axios';
import { ref, computed, onMounted, watch } from 'vue';
import { useUserStore } from '@/stores/user';
import { useToastStore } from '@/stores/toast';
import { useRoute } from 'vue-router';

    const userStore = useUserStore();
    const toastStore = useToastStore();

    const jobs = ref([]);
    const customer = ref([]);
    const editing = ref(false);
    const selectedLead = ref('');
    const selectedLeadTwo = ref('');
    const selectedStatus = ref('');
    const jobLeadOptions = ref([]);
    const jobStatusOptions = ref([]);
    const currentLeadId = ref(null);
    const currentStatusId = ref(null);
    const route = useRoute();
    const showPopup = ref(false);
    const jobId = ref(null);
    

    const showConfirmationPopup = (id) => {
    console.log("showConfirmationPopup called with id:", id);
    jobId.value = id; 
    showPopup.value = true;
    };

    const cancelDelete = () => {
        showPopup.value = false;
    };

    const sortedJobLeadOptions = computed(() => {
      const sortedOptions = [...jobLeadOptions.value];
      if (currentLeadId.value) {
        const currentIndex = sortedOptions.findIndex(option => option.value === currentLeadId.value);
        if (currentIndex !== -1) {
          const currentOption = sortedOptions.splice(currentIndex, 1)[0];
          sortedOptions.unshift(currentOption);
        }
      }
      return sortedOptions;
    });

    const sortedJobStatusOptions = computed(() => {
      const sortedOptions = [...jobStatusOptions.value];
      if (currentStatusId.value) {
        const currentIndex = sortedOptions.findIndex(option => option.value === currentStatusId.value);
        if (currentIndex !== -1) {
          const currentOption = sortedOptions.splice(currentIndex, 1)[0];
          sortedOptions.unshift(currentOption);
        }
      }
      return sortedOptions;
    });

    const getJobs = () => {
      axios.get(`/api/notes/${route.params.customerId}/get_jobs/`)
        .then((response) => {
          console.log('job data', response.data);
          jobs.value = response.data.jobs;
          customer.value = response.data.customer;
        })
        .catch((error) => {
          console.log('error', error);
        });
    };

    const getJobLeadOptions = () => {
            axios.get('/api/notes/job_leads/')
                .then((response) => {
                    // Access employees and organization owners
                    const employees = response.data.leads.employees || [];
                    const organizationOwners = response.data.leads.organization_owners || [];
                    // Combine employees and organization owners
                    const combinedLeads = [...employees, ...organizationOwners];
                    // Map to desired format
                    const leads = combinedLeads.map(lead => ({
                        value: lead.id,
                        label: `${lead.first_name} ${lead.last_name}`
                    }));
                    jobLeadOptions.value = leads;
                })
                .catch((error) => {
                    console.log("error", error);
                });
        };

    const getJobStatusOptions = () => {
      axios.get('/api/notes/job_status/')
        .then((response) => {
          console.log('data', response.data);
          jobStatusOptions.value = response.data.status.map(status => ({
            value: status,
            label: status
          }));
        })
        .catch((error) => {
          console.log('error', error);
        });
    };

    const editJob = (job) => {
      job.editing = true;
      job.original = { ...job };
      selectedLead.value = job.lead ? job.lead.id : '';
      selectedLeadTwo.value = job.lead_two ? job.lead_two.id : '';
      currentLeadId.value = job.lead ? job.lead.id : null;
      selectedStatus.value = job.status;
      currentStatusId.value = job.status;
    };

    const cancelEdit = (job) => {
      job.editing = false;
    };

    const deleteJob = async () => {
      try {
        console.log("Deleting job with ID:",(jobId.value));
        const response = await axios.delete(`/api/notes/jobs/${jobId.value}/`);
        toastStore.showToast(5000, 'Job deleted successfully.', 'bg-green-500');
        jobs.value = jobs.value.filter(job => job.id !== jobId.value);
      } catch (error) {
        if (error.response) {
            console.error("Error deleting job:", error.response.data);
            console.error("Status code:", error.response.status);
            toastStore.showToast(5000, 'Something went wrong. Please try again.', 'bg-red-500');
        } else if (error.request) {
            console.error("Error deleting job:", error.request);
            toastStore.showToast(5000, 'No response from server. Please try again.', 'bg-red-500');
        } else {
            console.error("Error deleting job:", error.message);
            toastStore.showToast(5000, 'Request error. Please try again.', 'bg-red-500');
        }
      } finally {
        showPopup.value = false;
      }
    };

    const submitForm = (job, event) => {
      event.preventDefault();
      const formData = new FormData();
      formData.append('lead', selectedLead.value);
      formData.append('lead_two', selectedLeadTwo.value);
      formData.append('name', job.name);
      formData.append('status', selectedStatus.value);
      formData.append('due_date', job.due_date || '');
      job.status = selectedStatus.value;

      axios.put(`/api/notes/jobs/${job.id}/`, formData)
        .then((response) => {
          job.editing = false;
          if (response.data.name) job.name = response.data.name;
          if (response.data.lead) job.lead = response.data.lead;
          getJobs();


        })
        .catch((error) => {
          console.log('error', error);
        });
    };

    onMounted(() => {
      getJobs();
      getJobLeadOptions();
      getJobStatusOptions();
    });

    watch(() => route.params.customerId, () => {
      getJobs();
    });

</script>