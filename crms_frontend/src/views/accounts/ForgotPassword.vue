<template>
    <div class="max-w-md mx-auto p-4">
      <!-- Email Entry Form -->
      <div v-if="!codeSent" class="space-y-4">
        <h2 class="text-xl font-bold">Forgot Password</h2>
        <form @submit.prevent="requestResetCode">
          <label for="email" class="block text-sm font-medium text-gray-700">Email Address</label>
          <input
            v-model="email"
            type="email"
            id="email"
            class="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm"
            required
          />
          <button
            type="submit"
            class="mt-4 bg-blue-500 text-white px-4 py-2 rounded-md shadow-sm hover:bg-blue-600"
          >
            Send Reset Code
          </button>
          <p v-if="message" class="mt-2 text-sm text-green-600">{{ message }}</p>
          <svg
            v-if="loading"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="1.5"
            stroke="currentColor"
            class="animate-spin h-6 w-6 text-blue-500"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0 3.181 3.183a8.25 8.25 0 0 0 13.803-3.7M4.031 9.865a8.25 8.25 0 0 1 13.803-3.7l3.181 3.182m0-4.991v4.99"
            />
          </svg>
        </form>
      </div>
      
      <!-- Code Entry Form -->
      <div v-if="codeSent && !passwordUpdated" class="space-y-4">
        <h2 class="text-xl font-bold">Enter Reset Code</h2>
        <form @submit.prevent="verifyResetCode">
          <label for="code" class="block text-sm font-medium text-gray-700">Reset Code</label>
          <input
            v-model="code"
            type="text"
            id="code"
            class="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm"
            required
          />
          <button
            type="submit"
            class="mt-4 bg-blue-500 text-white px-4 py-2 rounded-md shadow-sm hover:bg-blue-600"
          >
            Verify Code
          </button>
          <p v-if="message" class="mt-2 text-sm text-red-600">{{ message }}</p>
        </form>
      </div>
      
      <!-- Password Update Form -->
      <div v-if="codeSent && passwordUpdated" class="space-y-4">
        <h2 class="text-xl font-bold">Update Password</h2>
        <form @submit.prevent="updatePassword">

        <div class="relative">
          <label for="new_password" class="block text-sm font-medium text-gray-700">New Password</label>
          <input
            v-model="newPassword"
            :type="passwordField"
            id="new_password"
            class="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm"
            required
          />
          <button type="button" @click="togglePassword" class="absolute inset-y-5 right-0 flex items-center pr-3 top-1/2 translate-y-1/2">
                  <svg v-if="isPasswordVisible1" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                  </svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88" />
                  </svg>
            </button>
        </div>

          <template v-if="errors.length > 0">
                <div class="bg-red-300 text-white rounded-lg p-6 mt-4">
                    <ul class="list-disc pl-5">
                    <li v-for="(error, index) in errors" :key="index">{{ error }}</li>
                    </ul>
                </div>
            </template>
          


          <button type="submit" class="mt-4 bg-blue-500 text-white px-4 py-2 rounded-md shadow-sm hover:bg-blue-600">
            Reset Password
          </button>
          <p v-if="message" class="mt-2 text-sm text-green-600">{{ message }}</p>
        </form>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue';
  import { useRouter } from 'vue-router';
  import axios from 'axios';
  import { useToastStore } from '@/stores/toast';
      
      const email = ref('');
      const code = ref('');
      const newPassword = ref('');
      const codeSent = ref(false);
      const passwordUpdated = ref(false);
      const message = ref('');
      const loading = ref(false);
      const errors = ref([]);
      
      const toastStore = useToastStore();
      const router = useRouter();

      // Password visibility states
      const isPasswordVisible1 = ref(false)
      const passwordField = computed(() => isPasswordVisible1.value ? 'text' : 'password')
      function togglePassword() {
        isPasswordVisible1.value = !isPasswordVisible1.value
      }

      const requestResetCode = async () => {
        loading.value = true;
        try {
          const response = await axios.post('/api/accounts/request-password-reset/', { email: email.value });
          message.value = response.data.detail;
          codeSent.value = true;
        } catch (error) {
          message.value = error.response.data.detail || 'An error occurred';
        } finally {
          loading.value = false;
        }
      };
  
      const verifyResetCode = async () => {
        loading.value = true;
        try {
          const response = await axios.post('/api/accounts/verify-reset-code/', {
            email: email.value,
            code: code.value
          });
          message.value = response.data.detail;
          passwordUpdated.value = true;
        } catch (error) {
          message.value = error.response.data.detail || 'An error occurred';
        } finally {
          loading.value = false;
        }
      };
      
      const updatePassword = async () => {
        loading.value = true;
        errors.value = [];
        try {
          const response = await axios.post('/api/accounts/reset-password/', {
            email: email.value,
            code: code.value,
            new_password: newPassword.value
          });
          if (response.data.message === 'success') {
            // ADD SUCCESS MESSAGE.
            toastStore.showToast(5000, 'Password updated successfully', 'bg-green-500');
          // Redirect to a different route upon success
          router.push('/login'); // Adjust this route as needed
          } else {
            toastStore.showToast(5000, 'An error occurred. Please try again.', 'bg-red-500');
          }
        } catch (error) {
            if (error.response) {
              // Check for detailed error messages from the server
              if (error.response.data.detail) {
                toastStore.showToast(5000, error.response.data.detail, 'bg-red-500');
              } else if (error.response.data.errors) {
                // Display validation errors
                errors.value = error.response.data.errors;
              } else {
                // Handle generic error messages
                toastStore.showToast(5000, 'An error occurred. Please try again later.', 'bg-red-500');
              }
            } else {
              // Handle network or connection errors
              toastStore.showToast(5000, 'Network error. Please check your connection.', 'bg-red-500');
            }
          } finally {
            loading.value = false;
          }
};

  </script>