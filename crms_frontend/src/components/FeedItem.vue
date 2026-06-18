<template>


    <div class="mb-6 p-4 flex flex-col md:flex-row items-start justify-between">
        <div class="flex flex-col space-y-2">
        <p v-if="!note.related_job || !note.related_job.name">
            <strong>
                General Note
            </strong>
        </p>
        <p v-if="note.related_job && note.related_job.name">
            <strong>
             <RouterLink :to="{ name: 'job_notes_view', params: { customerId: note.related_customer, jobId: note.related_job.id } }" class="text-blue-500 hover:text-blue-800">
                {{ note.related_job.name }}
              </RouterLink>
            </strong>
        </p>
        </div>
        <p class="text-gray-600">{{ note.created_at_formatted }}</p>
    </div>

    <div v-if="!note.editing">
        <p class="p-4">{{ note.body }}</p>
    </div>

    <div v-else class="p-4">
        <textarea v-model="note.body" class="p-2 w-full bg-gray-100 rounded-lg"></textarea>
    </div>

    <div class="my-6 flex p-4">
        <div class="flex-grow">
            <div class="flex items-center space-x-8">
                
                <!-- Comment Bubble if needed
                <button class="relative inline-block">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="w-6 h-6">
                        <text x="50%" y="62%" text-anchor="middle" font-size="10"
                            class="text-gray-500 font-thin">0</text>
                        <path stroke="gray" stroke-linecap="round" stroke-linejoin="round"
                            d="M12 20.25c4.97 0 9-3.694 9-8.25s-4.03-8.25-9-8.25S3 7.444 3 12c0 2.104.859 4.023 2.273 5.48.432.447.74 1.04.586 1.641a4.483 4.483 0 01-.923 1.785A5.969 5.969 0 006 21c1.282 0 2.47-.402 3.445-1.087.81.22 1.668.337 2.555.337z">
                        </path>
                    </svg>
                    <span
                        class="absolute top-0 left-0 w-full h-full bg-gray-300 opacity-0 transition-opacity duration-200"></span>
                </button> -->

                <span class="text-gray-500 text-xs">Created: <p>{{ note.created_by.first_name }}
                        {{ note.created_by.last_name }}</p></span>
                <span class="text-gray-500 text-xs" v-if="note.updated_by">Updated: <p>{{ note.updated_by.first_name }}
                        {{ note.updated_by.last_name }}</p></span>
            </div>
        </div>

        <!-- Buttons on right side of note box-->
        <div class="flex items-center space-x-6">
            <!-- Button to trigger the edit feature -->
            <button v-if="!note.editing" @click="toggleEdit" class="text-emerald-500 hover:text-emerald-700">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                    stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round"
                        d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
                </svg>
            </button>

            <button v-else @click="saveNote" class="text-green-500 hover:text-green-700">
                Save
            </button>
            <button v-if="note.editing" @click="cancelEdit" class="text-red-500 hover:text-red-700">
                Cancel
            </button>

            <!-- Button to trigger the popup delete confirmation dialog -->
            <button @click="showConfirmationPopup" class="text-red-500 hover:text-red-700">
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
                        <button @click="deleteNote(note.id)" class="px-4 py-2 bg-red-500 text-white rounded-lg">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                stroke="currentColor" class="size-6">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>


<script setup>
import { ref, reactive, defineProps, defineEmits } from "vue";
import axios from 'axios';
import { useToastStore } from '@/stores/toast';

const props = defineProps({
    note: Object,
    jobs: Object,
    id: null,
});

const emit = defineEmits(['note-updated', 'note-deleted']);

// Reactive state
const state = reactive({
    notes: [],
    customer: {},
    jobs: [],
    id: null,
    isNoteDeleted: false // Added state for deletion feedback
});

// Local state
const showPopup = ref(false);
const toastStore = useToastStore();
const originalNoteBody = ref(props.note.body);

const showConfirmationPopup = () => {
    showPopup.value = true;
};

const cancelDelete = () => {
    showPopup.value = false;
};


const toggleEdit = () => {
    props.note.editing = !props.note.editing;
    if (!props.note.editing) {
        props.note.body = originalNoteBody.value;
    }
};

const handleSaveClick = () => {
    emit('saveNote', props.note.id);
};

//////CRUD//////

const saveNote = async () => {
    try {
        console.log("Saving note id:", props.note.id);
        await axios.put(`/api/notes/notes/${props.note.id}/`, { body: props.note.body });
        originalNoteBody.value = props.note.body;
        props.note.editing = false;
        emit('note-updated', props.note.id);
        toastStore.showToast(5000, 'Note updated successfully.', 'bg-green-500');
    } catch (error) {
        toastStore.showToast(5000, 'Error updating note', 'bg-red-500');
    }
};

const cancelEdit = () => {
    props.note.body = originalNoteBody.value;
    props.note.editing = false;
};

const deleteNote = async (id) => {
    try {
        await axios.delete(`/api/notes/notes/${id}/`);
        state.notes = state.notes.filter(note => note.id !== id);
        state.isNoteDeleted = true; // Temporary state variable
        // Optional: Set a timeout to reset the temporary variable after a short delay
        setTimeout(() => {
            state.isNoteDeleted = false;
        }, 100);
        toastStore.showToast(5000, 'Note deleted successfully.', 'bg-green-500');
        emit('note-deleted', props.note.id);
    } catch (error) {
        console.error("Error deleting note:", error);
        toastStore.showToast(5000, 'Something went wrong. Please try again.', 'bg-red-500');
    } finally {
        // Ensure the popup is always closed after operation completes (whether success or failure)
        showPopup.value = false;
    }
};

</script>