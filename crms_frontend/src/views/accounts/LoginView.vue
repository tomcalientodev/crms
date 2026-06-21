<template>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full py-12">
      <div class="flex justify-center">
        <div class="max-w-lg w-full p-8 bg-white border border-gray-200 rounded-lg shadow-lg">
          <h1 class="mb-6 text-2xl text-center">Log in</h1>
  
          <form class="space-y-6" v-on:submit.prevent="submitForm">
            <div>
              <label>Email</label><br>
              <input type="email" v-model="form.email" placeholder="Your e-mail address"
                class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg" />
            </div>
  
            <div>
              <label>Password</label><br>
              <div class="relative">
                <input :type="passwordFieldType" v-model="form.password" placeholder="Your password"
                  class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg pr-12" />
                <button type="button" @click="togglePasswordVisibility" class="absolute inset-y-0 right-0 flex items-center pr-3">
                  <svg v-if="isPasswordVisible" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                  </svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88" />
                  </svg>
                </button>
              </div>
            </div>
  
            <template v-if="errors.length > 0">
              <div class="bg-red-300 text-white rounded-lg p-6">
                <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
              </div>
            </template>
             
              <div class="flex justify-between items-center">
              <button type="submit" class="py-4 px-6 bg-green-400 text-white rounded-lg">Log in</button>
            </div>

          </form>

            <div class="bg-white border border-yellow-200 rounded-lg p-4 mb-4 mt-4">
              <p class="font-semibold text-gray-800 mb-2">Demo Login Credentials</p>
              <p class="text-gray-700">
                <span class="font-medium">Email:</span>
                alincoln@libertyautoparts.demo<br />
                <span class="font-medium">Password:</span> DemoPassword123!
              </p>
            </div>

        </div>
      </div>
    </div>
  </template>
    


<script setup>
import axios from 'axios'
import { useUserStore } from '@/stores/user'
import { ref, computed, watch } from 'vue';
import { useRouter } from 'vue-router'; 


        const userStore = useUserStore();

        const form = ref({
            email: '',
            password: '',
        });

        const errors = ref([]);
        const isPasswordVisible = ref(false);

        const router = useRouter();

        const passwordFieldType = computed(() => {
            return isPasswordVisible.value ? 'text' : 'password';
         });

         const togglePasswordVisibility = () => {
            isPasswordVisible.value = !isPasswordVisible.value;
            };

        const submitForm = async () => {
            errors.value = [];

            if (!form.value.email) {
                errors.value.push("Your email is missing.");}
            if (!form.value.password) {
                errors.value.push("Your password is missing.");}

            if (errors.value.length === 0) {
                try {
                    const response = await axios.post('/api/accounts/token/', form.value);
                    userStore.setToken(response.data);
                    axios.defaults.headers.common['Authorization'] = "Bearer " +  response.data.access;
                } catch (error) {
                    console.error('Login error:', error);
                    errors.value.push('The email or password is incorrect! Or the user is not activated.');
                }
            }

            if (errors.value.length === 0) {
                try {
                    const response = await axios.get('/api/accounts/user_info');
                    await userStore.setUserInfo(response.data);
                    router.push({ name: 'worker_dashboard', params: { workerId: userStore.user.id} });
                } catch (error) {
                    console.error('User info error:', error);
                }
            }
        };
</script>
