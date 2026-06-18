<template>
    <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
        <div class="main-left">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <!--TODO: Add persons name the job is for-->
                <h1 class="mb-6 text-2xl">Job Creation for {{ customer.user.first_name }} {{ customer.user.last_name }}
                   
                </h1>

                <p class="mb-6 text-gray-500">
                    After creating a Job. You will be directed to create a Job note.
                </p>
            </div>
        </div>

        <div class="main-right">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <form class="space-y-6" v-on:submit.prevent="submitForm">
                    <!-- prevent means don't refresh screen, use the submitForm JS function below. -->

                    <div>
                        <label>Job Name</label><br>
                        <input type="text" v-model="form.name" placeholder="Job Name"
                            class="w-full mt-2 py-4 px-6 border border-grey-200 rounded-lg" />
                    </div>

                    <div>
                        <label for="job_lead">Primary Contact</label><br>
                        <select id="job_lead" v-model="form.lead"
                            class="w-full mt-2 py-4 px-6 border border-grey-200 rounded-lg">
                            <option value=""></option>
                            <option v-for="option in jobLeadOptions" :value="option.value" :key="option.value">{{
                    option.label }}
                            </option>
                        </select>
                    </div>

                    <div>
                        <label for="job_lead">Secondary Contact (Optional)</label><br>
                        <select id="job_lead" v-model="form.lead_two"
                            class="w-full mt-2 py-4 px-6 border border-grey-200 rounded-lg">
                            <option value="">Select a Secondary Contact</option>
                            <option v-for="option in jobLeadOptions" :value="option.value" :key="option.value">{{
                    option.label }}
                            </option>
                        </select>
                    </div>

                    <div>
                        <label for="due_date" class="block text-sm font-medium text-gray-700">Due Date</label>
                        <input type="date" id="due_date" v-model="form.due_date"
                            class="w-full mt-2 py-3 px-4 border border-gray-300 rounded-lg shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
                    </div>

                    <!-- <div>
                        <label for="job_status">Job Status</label><br>
                        <select id="job_status" v-model="form.status"
                            class="w-full mt-2 py-4 px-6 border border-grey-200 rounded-lg">
                            <option value="">Select Job Status</option>
                            <option v-for="(value, label) in jobStatusOptions" :value="value" :key="value">{{ label }}
                            </option>
                        </select>
                    </div> -->

                    <template v-if="errors.length > 0">
                        <div class="bg-red-300 text-white rounded-lg p-6">
                            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                            <!-- key makes error unique or it won't work.-->
                        </div>
                    </template>

                    <div class="flex justify-between">
                        <div>
                            <button type="button" @click="cancelNote"
                                class="py-4 px-6 bg-red-400 text-white rounded-lg">Cancel Job/Go
                                Back</button>
                        </div>

                        <div>
                            <button type="submit" class="py-4 px-6 bg-green-600 text-white rounded-lg">Create
                                Job</button>
                        </div>
                    </div>

                </form>
            </div>
        </div>

    </div>

</template>

<script setup>
import { ref, onMounted, defineEmits } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useToastStore } from '@/stores/toast'

const emit = defineEmits(['job-created'])

const form = ref({
    name: '',
    lead: '',
    due_date: '',
    id: null,
});

const jobLeadOptions = ref([]);
const errors = ref([]);
const router = useRouter();
const toastStore = useToastStore();
const customer = ref({
  user: {
    first_name: '',
    last_name: '',
  }
});


const getCustomer = async () => {
  try {
    const response = await axios.get(`/api/accounts/customers/${router.currentRoute.value.params.customerId}/`);
    customer.value = response.data;
    console.log("data", response.data);
  } catch (error) {
    console.log("error", error);
  }
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

const cancelNote = () => {
    router.go(-1);
};
const submitForm = () => {
    errors.value = [];
    if (form.value.name === '') {
        errors.value.push("Your Job Name is missing.");
    }
    if (form.value.lead === '') {
        errors.value.push("Your Job Lead is missing.");
    }
    if (form.value.due_date === '') {
        form.value.due_date = null;
    }

    if (errors.value.length === 0) {
        axios.post(`/api/notes/${router.currentRoute.value.params.customerId}/job_creation/`, form.value)
            .then((response) => {
                if (response.data.message === 'success') {
                    toastStore.showToast(5000, 'Job has been created.', 'bg-green-500');
                
                    const selectedLead = jobLeadOptions.value.find(lead => lead.value === form.value.lead);
                    const leadName = selectedLead ? selectedLead.label : '';
                    const selectedLeadTwo = jobLeadOptions.value.find(lead_two => lead_two.value === form.value.lead_two);
                    const leadTwoName = selectedLeadTwo ? selectedLeadTwo.label : '';

                    console.log('lead name', leadName);

                    emit('job-created', {
                        lead: leadName,
                        lead_two: leadTwoName,
                        jobName: form.value.name,
                        // jobId: response.data.job.id
                    });

                    router.push({ name: 'job_note_creation', params: { customerId: router.currentRoute.value.params.id, jobId: response.data.job.id } });
                } else {
                    toastStore.showToast(5000, 'Something went wrong. Please try again.', 'bg-red-500');
                    console.log('Error:', response.data.error);
                }
            })
            .catch((error) => {
                console.log('error', error);
                toastStore.showToast(5000, 'Something went wrong. Please try again.', 'bg-red-500');
            });
    }
};

onMounted(() => {
    getCustomer();
    getJobLeadOptions(); // This will run when the component is mounted
});

</script>