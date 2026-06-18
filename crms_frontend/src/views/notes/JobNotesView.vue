<template>

    <div class="top-0 left-0 mb-5 ml-0 space-x-4">
        <div class="hidden md:flex md:space-x-5 list-none">
            <li>
                <RouterLink :to="{ name: 'customer_view', params: { customerId: customer.id } }"
                    class="text-base font-normal text-gray-500 list-none hover:text-gray-900 flex items-center">

                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="w-4 h-4">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5 3 12m0 0 7.5-7.5M3 12h18" />
                    </svg>
                    <span class="ml-2">Back to Customer Profile</span> </RouterLink>
            </li>
        </div>
    </div> 

    <main class="px-4 md:px-8 py-4 md:py-6 bg-gr-100">
        <div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-4">

            <!-- The Customer INfo BOX -->
            <div class="main-left md:col-span-1" v-if="customer && customer.user">
                
                <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">

                    <p><strong><u>Customer</u></strong></p>
                    <p >{{ customer.user.first_name }} {{customer.user.last_name}}</p>
                
                    <div class="mt-6 flex flex-col md:justify-around">
                        <p class="text-xs text-gray-500">{{customer.user.phone_number}}</p>
                        <p class="text-xs text-gray-500">{{customer.user.email}}</p>
                    </div>
                </div>
                <!-- The job INfo BOX -->
                <div class="main-left md:col-span-1" >
                    <div class="p-4 bg-white border border-gray-200 text-center rounded-lg mt-5">

                        <p><strong><u>Job Name:</u></strong></p>
                        <p >{{ job.name }}</p>
                   
                        <div class="mt-6 flex flex-col md:justify-around">
                            <p class="text-xs text-gray-500">You can add Job Notes on this page.</p>
                            <p class="text-xs text-gray-500"></p>
                        </div>
                    </div>
                </div> 

            </div> 


            <!-- The INPUT BOX -->
            <div class="main-center md:col-span-2 space-y-4">
                <button @click="toggleInputBox" class="py-3 px-6 bg-orange-400 text-white rounded-lg  hover:bg-orange-500">
                        Add Job Note
                        <template v-if="!showInputBox">+</template>
                        <template v-else>-</template>
                    </button>
                <div class="bg-white border border-gray-200 rounded-lg">
                    <form v-if="showInputBox" v-on:submit.prevent="submitForm" method="post" class="p-4">
                        <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg"
                            placeholder="Write a Note"></textarea>

                        <div class="flex flex-col md:flex-row md:justify-between mt-4">

                            <button
                                class="w-full md:w-auto inline-block py-3 px-6 bg-orange-400 hover:bg-orange-500 text-white rounded-lg">Post</button>
                        </div>
                    </form>
                </div>
         
                <!-- The Notes -->
                <div class="bg-white border border-gray-200 rounded-lg" v-for="note in notes" v-bind:key="note.id">
                    <div class="p-4">
                            <FeedItem v-bind:note="note" @note-deleted="handleNoteDeleted"  />
                        </div>
                </div>
                
            </div>


        </div>
    </main>
</template>


<script>
import axios from "axios";
import { ref, reactive, onMounted, watch } from "vue";
import FeedItem from '@/components/FeedItem.vue'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'
import { useRoute } from 'vue-router';

export default {
    name: "JobNotesView",

    components: {
        FeedItem
    },

    setup() {
        const userStore = useUserStore();
        const toastStore = useToastStore();
        const showInputBox = ref(false);
        const notes = ref([]);
        const customer = ref({});
        const job = ref({});
        const body = ref('');
        const route = useRoute();

        const toggleInputBox = () => {
            showInputBox.value = !showInputBox.value;
        };


            const handleNoteDeleted = (deletedNoteId) => {
            console.log("Note with id", deletedNoteId, "deleted!");
            // Update the feed data in the parent component (e.g., filter out the deleted note)
            getFeed(); // Re-fetch data or update existing data based on deletedNoteId
        };

        const getFeed = () => {
            axios
                .get(`/api/notes/${route.params.customerId}/${route.params.jobId}/get_job_notes/`)
                .then((response) => {
                    console.log('data', response.data);
                    notes.value = response.data.notes;
                    customer.value = response.data.customer;
                    job.value = response.data.job;
                })
                .catch((error) => {
                    console.log("error", error);
                });
        };

        const submitForm = () => {
            console.log('submitForm', body.value);

            let formData = new FormData();
            formData.append('body', body.value);

            axios
                .post(`/api/notes/${route.params.customerId}/${route.params.jobId}/job_note_creation/`, formData, {})
                .then(response => {
                    console.log('data', response.data);
                    notes.value.unshift(response.data.notes);
                    body.value = '';
                    showInputBox.value = false;
                })
                .catch((error) => {
                    console.log("error", error);
                });
        };

        onMounted(() => {
            getFeed();
        });

        watch(() => route.params.id, () => {
            getFeed();
        }, { deep: true, immediate: true });

        return {
            userStore,
            toastStore,
            showInputBox,
            notes,
            customer,
            job,
            body,
            toggleInputBox,
            getFeed,
            submitForm,
            handleNoteDeleted,
        };
    }
};
</script>


