<template>
    <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
        <div class="main-left">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <h1 class="mb-6 text-2xl">Job Note Creation for {{ job.name }}</h1>

                <p class="mb-6 text-gray-500">
                <ul>
                    <li><b>Don't want to take a note? Just hit Cancel.</b> The job will still save you can take notes for this job at your convenience!</li> 
                </ul>
                </p>
            </div>
        </div>

        <div class="main-right">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <form class="space-y-6" v-on:submit.prevent="submitForm">
                    <!-- prevent means don't refresh screen, use the submitForm JS function below. -->

                    <div>
                        <label>Note Name</label><br>
                        <input type="text" v-model="form.name" placeholder="Note Name"
                            class="w-full mt-2 py-4 px-6 border border-grey-200 rounded-lg" />
                    </div>

                    <div>
                        <textarea v-model="form.body" class="p-4 w-full bg-gray-100 rounded-lg"
                            placeholder="Write a Job Note"></textarea>
                    </div>

                    <template v-if="errors.length > 0">
                        <div class="bg-red-300 text-white rounded-lg p-6">
                            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                            <!-- key makes error unique or it won't work.-->
                        </div>
                    </template>

                <div class="flex justify-between"> 
                    <div>
                        <button type="button" @click="backToCustomerView" class="py-4 px-6 bg-red-400 text-white rounded-lg">Cancel Note</button>
                    </div>

                    <div>
                        <button type="submit" class="py-4 px-6 bg-green-400 text-white rounded-lg">Create Job Note</button>
                    </div>
                </div>

                </form>
            </div>
        </div>

    </div>

</template>
<script setup>
import axios from 'axios';
import { ref, computed } from 'vue';
import { useToastStore } from '@/stores/toast';
import { useRoute, useRouter } from 'vue-router'; // Import useRoute

const toastStore = useToastStore();
const route = useRoute(); // Access route information
const router = useRouter();

const form = ref({
  name: '',
  body: '',
  id: null,
});

const job = ref({});

const errors = ref([]);

const getJob = async () => {
  try {
    const response = await axios.get(`/api/notes/jobs/${route.params.jobId}/`);
    console.log('data', response.data);
    job.value = response.data;
  } catch (error) {
    console.error('Error:', error);
  }
}

const submitForm = async () => {
  errors.value = []; // Reset errors on submit
  if (!form.value.name) {
    errors.value.push("Your Note Name is missing.");
  }
  if (!form.value.body) {
    errors.value.push("Your Note is missing.");
  }
  if (!errors.value.length) {
    try {
      const response = await axios.post(
        `/api/notes/${route.params.customerId}/${route.params.jobId}/job_note_creation/`,
        form.value
      );

      if (response.data.message === 'success') {
        toastStore.showToast(5000, 'The note was created for the job.', 'bg-green-500');
        // Navigate to customer view
        router.push({ name: 'customer_view', params: { customerId: route.params.id } });
      } else {
        console.error('Error:', response.data.error);
        toastStore.showToast(5000, 'Something went wrong. Please try again.', 'bg-red-500');
      }
    } catch (error) {
      console.error('error', error);
    }
  }
};

const backToCustomerView = () => {
  // Navigate to customer view (assuming same logic)
  router.push({ name: 'customer_view', params: { customerId: route.params.id } });
};

getJob();
</script>