<template>

 <!-- <div class="flex justify-center items-center mb-5">
    <div class="p-5 bg-white shadow rounded-lg max-w-xs sm:max-w-sm md:max-w-md lg:max-w-lg xl:max-w-xl mx-auto">
      <div class="w-full flex justify-between items-center">
        <span class="text-2xl font-bold mr-0" v-if="customer && customer.user">
          Customer: {{ customer.user.first_name }} {{ customer.user.last_name }}
        </span>
      </div>
    </div> 
     <RouterLink :to="{ name: 'job_creation', params: { customerId: customer.id } }">
      <button class="py-3 px-6 mr-32 mt-6 bg-orange-400 text-white rounded-lg hover:bg-orange-500">
        Add Job
      </button>
    </RouterLink> 
  </div> -->

  <div class="max-w-7xl mx-auto flex flex-col md:flex-row space-y-4 md:space-y-0 md:space-x-4">
    <div class="flex-1 space-y-4">

       <!-- The Customer Info -->
        <div class="p-4 flex-1 bg-white shadow border border-gray-200 rounded-lg" v-if="customer && customer.user">
          <!-- <p><strong>{{ customer.user.first_name }} {{ customer.user.last_name }}'s Information</strong></p> -->

          <div class="mt-1 flex flex-col md:justify-around">
            <div class="flex flex-col space-y-2">
              <div v-if="editingCustomer">
                <input v-model="customer.user.first_name" class="border border-gray-300 rounded-lg p-1  w-full focus:outline-none focus:ring-2 focus:ring-orange-500 transition-all mb-2" />
                <input v-model="customer.user.last_name"class="border border-gray-300 rounded-lg p-1 w-full focus:outline-none focus:ring-2 focus:ring-orange-500 transition-all mb-2"/>
              </div>
              <div v-else>
                  <p class="text-xl font-semibold mb-4">{{ customer.user.first_name }} {{ customer.user.last_name }}
                  </p>
              </div>
            </div>
            <div class="flex flex-col space-y-22">
              <div v-if="editingCustomer">
                <input v-model="customer.user.phone_number" class="border border-gray-300 rounded-lg p-1 w-full focus:outline-none focus:ring-2 focus:ring-orange-500 transition-all mb-2" />
              </div>
              <div v-else>
                <p class="text-lg text-gray-500">{{ customer.user.phone_number }}</p>
              </div>
            </div>
            <div class="flex flex-col space-y-2">
              <div v-if="editingCustomer">
                <input v-model="customer.user.email" class="border border-gray-300 rounded-lg p-1 w-full focus:outline-none focus:ring-2 focus:ring-orange-500 transition-all" />
              </div>
              <div v-else>
                <p class="text-lg text-gray-500">{{ customer.user.email }}</p>
              </div>
              <!--Editing Pencil-->
              <button v-if="!editingCustomer" @click="customerEdit()" class="text-blue-500 hover:underline">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                  stroke="currentColor"
                  class="size-5 hover:stroke-blue-500 hover:scale-110 transition-transform duration-200">
                  <path stroke-linecap="round" stroke-linejoin="round"
                    d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
                </svg>
              </button>
            </div>
          </div>
          <div v-if="editingCustomer">
            <button @click="updateCustomer"
              class="py-1 px-3 mt-4 mr-3 bg-orange-500 text-white rounded-lg hover:bg-orange-600">
              Save
            </button>
            <button @click="cancelcustomerEdit" class="py-1 px-3 bg-red-500 text-white rounded-lg hover:bg-red-600">
              Cancel
            </button>
          </div>
        </div>
   
      <!-- End of The Customer Info -->

      <!--START OF MISC NOTES -->

      <!-- Button to toggle input box -->
      <div class="  space-y-4">
        <div class="flex justify-between p-4">
          <!--QUESTION MARK POPOVER-->
          <div class="flex items-center justify-center mb-2">
            <span class="text-3xl ml-2">Notes</span>
            <div class="relative inline-block">
              <div class="text-gray-500 hover:text-gray-700 focus:outline-none focus:text-gray-700 cursor-pointer"
                @mouseenter="showNotesPopover = true" @mouseleave="showNotesPopover = false">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                  stroke="currentColor" class="w-4 h-4" @mouseenter="showPopover" @mouseleave="hidePopover">
                  <path stroke-linecap="round" stroke-linejoin="round"
                    d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />
                </svg>
              </div>
              <div v-show="showNotesPopover"
                class="absolute top-full left-0 transform -translate-x-3/4 -translate-y-2 right-0 bg-white border border-gray-200 rounded-lg shadow-lg py-2 px-4 z-10 w-48">
                <p class="text-sm text-gray-700">Adding notes creates notes that are not tied to any
                  specific job.</p>
              </div>
            </div>
          </div>
          <!--QUESTION MARK POPOVER END-->

          <button @click="toggleInputBox" class="py-2 px-4 bg-orange-400 text-white rounded-lg  hover:bg-orange-500">
            Add Note
            <template v-if="!showInputBox">+</template>
            <template v-else>-</template>
          </button>
        </div>

        <!-- The INPUT BOX -->
        <div class="bg-white border border-gray-200 rounded-lg">
          <form v-if="showInputBox" v-on:submit.prevent="submitNoteForm" method="post" class="p-4">
            <textarea v-model="body" class="p-4 w-full bg-orange-100 rounded-lg" placeholder="Write a Note"></textarea>

            <div class="flex flex-col md:flex-row md:justify-between mt-4">

              <button class="w-full md:w-auto inline-block py-3 px-6 bg-amber-500 text-white rounded-lg">Post</button>
            </div>
          </form>
        </div>

        <!-- The Notes -->
        <div class="bg-white border border-gray-200 rounded-lg" v-for="note in notes" v-bind:key="note.uuid">
          <div class="p-4">
            <!-- TODO: Auto display the user that updates a note after they update it. -->
            <FeedItem v-bind:note="note" :jobs="jobs" @note-updated="handleNoteUpdated"
              @note-deleted="handleNoteDeleted" />
          </div>
        </div>
      </div>

    </div>
    <!--END OF MISC NOTES -->



    <!-- Jobs table -->
    <div class="rounded-lg overflow-hidden md:col-span-2">
          <RouterLink v-if="customer" :to="{ name: 'job_creation', params: { customerId: customer.id } }" aria-current="page" 
          class="inline-block p-2 text-md text-white bg-orange-400 rounded-t-lg active hover:bg-orange-500"
          >+ Add Job</RouterLink>
      <!-- If want table to be smaller<div class="flex-1"> -->
      <div class="overflow-x-auto">
        <!-- For padding: <div class="bg-white border border-gray-200 rounded-lg p-4"></div> -->
        <form>
          <table class="min-w-full divide-y divide-gray-200 table-auto">

            <thead class="bg-gray-100">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Job Name</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Primary
                  Contact
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Secondary
                  Contact
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Due Date</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>

            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="job in jobs" :key="job.id">

                <td v-if="!job.editing"
                  class="px-6 py-4 whitespace-no-wrap text-sm  font-medium text-blue-600 hover:underline w-1/4">
                  <RouterLink :to="{ name: 'job_notes_view', params: { customerId: customerId, jobId: job.id } }">
                    {{ job.name }}
                  </RouterLink>
                </td>
                <td v-else>
                  <input type="text" v-model="job.name" class="border border-gray-300 rounded-lg w-40 px-2 py-1">
                </td>

                <td v-if="!job.editing" class="px-6 py-2 whitespace-no-wrap text-sm font-medium text-gray-900">
                  {{ job.status }}
                </td>
                <td v-else>
                  <select id="job_status" v-model="selectedStatus"
                    class="w-full border border-gray-300 rounded-lg py-1 px-2">
                    <option value="">Select</option>
                    <option v-for="option in sortedJobStatusOptions" :value="option.value" :key="option.value">{{
                      option.label }}</option>
                  </select>
                </td>

                <td v-if="!job.editing" class="px-6 py-4 whitespace-no-wrap text-sm font-medium text-gray-900 ">
                  {{ job.lead ? `${job.lead.first_name} ${job.lead.last_name}` : '' }}
                </td>
                <td v-else>
                  <select id="job_lead" v-model.lazy="selectedLead"
                    class="w-full border border-gray-300 rounded-lg py-1 px-2">
                    <option value="">Select</option>
                    <option v-for="option in sortedJobLeadOptions" :value="option.value" :key="option.value">{{
                      option.label
                      }}
                    </option>
                  </select>
                </td>

                <td v-if="!job.editing" class="px-6 py-4 whitespace-no-wrap text-sm font-medium text-gray-900 ">
                  {{ job.lead_two ? `${job.lead_two.first_name} ${job.lead_two.last_name}` : '' }}
                </td>
                <td v-else>
                  <select id="job_lead_two" v-model.lazy="selectedLeadTwo"
                    class="w-full border border-gray-300 rounded-lg py-1 px-2">
                    <option value="">Select</option>
                    <option v-for="option in sortedJobLeadOptions" :value="option.value" :key="option.value">{{
                      option.label
                      }}
                    </option>
                  </select>
                </td>

                <td v-if="!job.editing" class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {{ job.due_date }}
                </td>
                <td v-else>
                  <input type="date" v-model="job.due_date" class="border border-gray-300 rounded-lg w-full px-2 py-1">
                </td>

                <td v-if="!job.editing" class="px-4 py-3 whitespace-no-wrap text-sm font-medium text-gray-900">

                  <button @click="editJob(job)"
                    class="text-emerald-500 hover:text-emerald-700 hover:scale-110 transition-transform duration-200">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                      stroke="currentColor" class="size-6 mr-4">
                      <path stroke-linecap="round" stroke-linejoin="round"
                        d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
                    </svg>
                  </button>

                  <!-- <button class="px-4 py-2 bg-red-400 text-white rounded-lg hover:bg-red-500"
                                            @click.prevent="deleteJob(job.id)">Delete</button> -->

                  <button type="button" @click="showConfirmationPopup(job.id)"
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
                      <p>Are you sure you want to delete this note?</p>
                      <div class="mt-4 flex justify-end">
                        <button @click="cancelDelete"
                          class="mr-2 px-4 py-2 bg-gray-300 text-gray-800 rounded-lg">Cancel</button>
                        <button type="button" @click.prevent="deleteJob()"
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

</template>

<script setup>
import axios from 'axios';
import { ref, computed, onMounted, watch, reactive } from 'vue';
import { useUserStore } from '@/stores/user';
import { useToastStore } from '@/stores/toast';
import { useRoute } from 'vue-router';
import FeedItem from '@/components/FeedItem.vue';

const userStore = useUserStore();
const toastStore = useToastStore();

const jobs = ref([]);
const customer = ref({
  user: {
    first_name: '',
    last_name: '',
    phone_number: '',
    email: '',
  }
});
// const editing = ref(false);
const notes = ref([]);
const body = ref('');
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
const isPopoverOpen = ref(false);
const showInputBox = ref(false);
const showNotesPopover = ref(false);
const showJobsPopover = ref(false);
const customerId = route.params.customerId;
const originalEmail = ref('');
const editingCustomer = ref(false);


//////////Customer Info Box/////////

const customerEdit = () => {
    editingCustomer.value = !editingCustomer.value;
};

const cancelcustomerEdit = () => {
  editingCustomer.value = false;
};

const updateCustomer = async () => {
  const dataToSubmit = {
    user: {
      first_name: customer.value.user.first_name,
      last_name: customer.value.user.last_name,
      phone_number: customer.value.user.phone_number,
    }
  };
  if (customer.value.user.email !== originalEmail.value) {
    dataToSubmit.user.email = customer.value.user.email;
  }
  try {
    const response = await axios.put(`/api/accounts/customers/${customerId}/`, dataToSubmit);
    toastStore.showToast(5000, 'Customer updated successfully.', 'bg-green-500');
  } catch (error) {
    console.log("error", error);
  } finally {
    cancelcustomerEdit();
  }
}

////////////JOBS TABLE//////////
const cancelEdit = (job) => {
  job.editing = false;
};

/////////////NOTES AREA///////////
const toggleInputBox = () => {
  showInputBox.value = !showInputBox.value;
};

const handleNoteDeleted = () => {
  getFeed();
};

const handleNoteUpdated = () => {
  getFeed();
};

const submitNoteForm = async () => {
  const formData = new FormData();
  formData.append('body', body.value);
  try {
    const response = await axios.post(`/api/notes/${route.params.customerId}/misc_note_create/`, formData);
    notes.value.unshift(response.data);
    body.value = '';
    showInputBox.value = false;
    toastStore.showToast(5000, 'Note saved successfully.', 'bg-green-500');
  } catch (error) {
    console.log("error", error);
  }
};

const showPopover = () => {
  isPopoverOpen.value = true;
};

const hidePopover = () => {
  isPopoverOpen.value = false;
};


////////////JOBS TABLE////////
const showConfirmationPopup = (id) => {
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


const deleteJob = async () => {
  try {
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


//Whole Page

const getFeed = async () => {
  try {
    const response = await axios.get(`/api/notes/${route.params.customerId}/get_notes`);
    notes.value = response.data.notes;
    customer.value = response.data.customer;
    originalEmail.value = customer.value.user.email;
    jobs.value = response.data.jobs;
  } catch (error) {
    console.log("error", error);
  }
};
//OTHER

const addRecentlyViewed = async (customerId) => {
  try {
    await axios.post(`/api/dashboards/recently_viewed_customers/${customerId}/`);
  } catch (error) {
    console.error('Error adding recently viewed customer:', error);
  }
};

onMounted(() => {
  getJobs();
  getJobLeadOptions();
  getJobStatusOptions();
  getFeed();

  if (customerId) {
    addRecentlyViewed(customerId);
  }
});

//Used for reactive updates based on changes in data, props, or computed properties.
watch(() => route.params.id, getFeed, { deep: true, immediate: true });

</script>

<style scoped>
.cursor-pointer {
  cursor: pointer;
}
</style>