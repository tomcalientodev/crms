<template>

<!--- NAV BUTTONS-->
<nav class="bg-white shadow dark:bg-gray-100">
    <div class="container flex items-center justify-center p-3 mb-5 mx-auto text-gray-600 capitalize dark:text-gray-500">

      <a href="#" class="border-b-2 border-transparent hover:text-gray-800 dark:hover:text-gray-200 hover:border-blue-500 mx-1.5 sm:mx-6">All Notes</a>

        <a href="#" class="border-b-2 border-transparent hover:text-gray-800 dark:hover:text-gray-200 hover:border-blue-500 mx-1.5 sm:mx-6">All Job</a>

        <a href="#" class="border-b-2 border-transparent hover:text-gray-800 dark:hover:text-gray-200 hover:border-blue-500 mx-1.5 sm:mx-6">Add Job</a>

    </div>
</nav>

  <main class="px-4 md:px-1 py-4 md:py-0 bg-gr-100">

    <div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-4">
      <!-- The Customer Info BOX -->
      <div class="main-left md:col-span-1" v-if="customer && customer.user">
        <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">

          <p><strong><u>Customer</u></strong></p>
          <p>{{ customer.user.first_name }} {{ customer.user.last_name }}</p>

          <div class="mt-6 flex flex-col md:justify-around">
            <p class="text-xs text-gray-500">{{ customer.user.format_phone_number }}</p>
            <p class="text-xs text-gray-500">{{ customer.user.email }}</p>
          </div>
        </div>
      </div>

      <!-- Button to toggle input box -->
      <div class="main-right md:col-span-2 space-y-4">
        <div class="flex justify-between">

          <!--QUESTION MARK POPOVER-->
          <div class="flex items-center justify-center mb-2">
            <span class="text-3xl ml-2">Notes</span>
            <div class="relative inline-block">
              <div class="text-gray-500 hover:text-gray-700 focus:outline-none focus:text-gray-700 cursor-pointer"
                @mouseenter="showNotesPopover = true" @mouseleave="showNotesPopover = false">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                  stroke="currentColor" class="w-4 h-4" @mouseenter="showPopover" @mouseleave="hidePopover">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />
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
          <form v-if="showInputBox" v-on:submit.prevent="submitForm" method="post" class="p-4">
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
            <FeedItem v-bind:note="note" :jobs="jobs" @note-updated="handleNoteUpdated" @note-deleted="handleNoteDeleted" />
          </div>
        </div>

      </div>

      <!-- The JOBS BOX -->
      <div class="main-right col-span-1 space-y-4">
        <div class="p-4 bg-white border border-gray-200 rounded-lg">


          <!--QUESTION MARK POPOVER-->
          <div class="flex items-center justify-center mb-2">
            <span class="text-2xl mr-2">Jobs</span>
            <div class="relative inline-block">
              <div class="text-gray-500 hover:text-gray-700 focus:outline-none focus:text-gray-700 cursor-pointer"
                @mouseenter="showJobsPopover = true" @mouseleave="showJobsPopover = false">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                  stroke="currentColor" class="w-4 h-4" @mouseenter="showPopover" @mouseleave="hidePopover">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 5.25h.008v.008H12v-.008Z" />
                </svg>
              </div>

              <div v-show="showJobsPopover"
                class="absolute top-full left-0 transform -translate-x-3/4 -translate-y-2 right-0 bg-white border border-gray-200 rounded-lg shadow-lg py-2 px-4 z-10 w-48">
                <p class="text-sm text-gray-700">Create a job or click on a created job to access it's info and notes.
                </p>
              </div>

            </div>
          </div>
          <!--QUESTION MARK POPOVER END-->

          
          <div class="flex justify-center mb-2">
            <button class="py-1 px-2 mr-3 bg-orange-400 text-white rounded-lg hover:bg-orange-500 mb-2">
              <RouterLink :to="{ name: 'job_detail_view', params: { customerId: customer.id } }" class=" inline-block">
                See All
              </RouterLink>
            </button>

            <button class="py-1 px-2 bg-orange-400 text-white rounded-lg hover:bg-orange-500 mb-2">
              <RouterLink :to="{ name: 'job_creation', params: { customerId: customer.id } }" class="inline-block">
                Add Job
              </RouterLink>
            </button>
          </div>

          <!--TODO: If no jobs display message.-->
          <div class="flex items-center justify-between" v-for="job in jobs">
            <p class="text-xs">
              <strong>
                <RouterLink class="text-blue-600 hover:underline"
                  :to="{ name: 'job_notes_view', params: { customerId: customer.id, jobId: job.id } }">
                  {{ job.name }}
                </RouterLink>
              </strong><br>
              <span class="text-gray-500">{{ job.status }}</span>
            <div class="mb-1"></div>
            </p>
            <!-- <a href="#" class="py-2 px-3 bg-green-400 text-white text-xs rounded-lg">Edit</a> -->
          </div>
        </div>
      </div>
    </div>
  </main>
</template>


<script setup>
import axios from "axios";
import { ref, reactive, toRefs, onMounted, watch } from "vue";
import { useRoute } from "vue-router";
import FeedItem from '@/components/FeedItem.vue';
import { useUserStore } from '@/stores/user';
import { useToastStore } from '@/stores/toast';

const userStore = useUserStore();
const toastStore = useToastStore();
const route = useRoute();

const showInputBox = ref(false);
const showNotesPopover = ref(false);
const showJobsPopover = ref(false);
const customerId = route.params.customerId;

const customer = ref({});
const notes = ref([]);
const jobs = ref([]);
const body = ref('');
const isPopoverOpen = ref(false);

const toggleInputBox = () => {
  showInputBox.value = !showInputBox.value;
};

const handleNoteDeleted = () => {
  getFeed(); 
};

const handleNoteUpdated = () => {
  getFeed();
};

const getFeed = async () => {
  try {
    const response = await axios.get(`/api/notes/${route.params.customerId}/get_notes`);
    console.log("data", response.data);
    notes.value = response.data.notes;
    customer.value = response.data.customer;
    jobs.value = response.data.jobs;

  } catch (error) {
    console.log("error", error);
  }
};

const submitForm = async () => {
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

const addRecentlyViewed = async (customerId) => {
  try {
    console.log('Adding recently viewed customer:', customerId);
    await axios.post(`/api/dashboards/recently_viewed_customers/${customerId}/`);
  } catch (error) {
    console.error('Error adding recently viewed customer:', error);
  }
};

const showPopover = () => {
  isPopoverOpen.value = true;
};

const hidePopover = () => {
  isPopoverOpen.value = false;
};

//used for initial data fetching, DOM manipulations, or setting up event listeners.
onMounted(() => {
  if (customerId) {
    addRecentlyViewed(customerId);
  }
  getFeed();
});

//Used for reactive updates based on changes in data, props, or computed properties.
watch(() => route.params.id, getFeed, { deep: true, immediate: true });


</script>