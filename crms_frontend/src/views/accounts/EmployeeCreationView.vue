<template>
    <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
      <div class="main-left">
        <div class="p-12 bg-white border border-gray-200 rounded-lg">
          <h1 class="mb-6 text-2xl">Employee Creation</h1>
          <p class="mb-6 text-gray-500">
            Welcome to the employee creation page. After creating an employee you can search for them using the magnifying glass in the searchbar above.
          </p>
        </div>
      </div>
  
      <div class="main-right">
        <div class="p-12 bg-white border border-gray-200 rounded-lg">
          <form class="space-y-6" @submit.prevent="submitForm">
            <div>
              <label>First Name</label><br>
              <input type="text" v-model="form.first_name" placeholder="Your First Name" class="w-full mt-2 py-4 px-6 border border-grey-200 rounded-lg" />
            </div>
  
            <div>
              <label>Last Name</label><br>
              <input type="text" v-model="form.last_name" placeholder="Your Last Name" class="w-full mt-2 py-4 px-6 border border-grey-200 rounded-lg" />
            </div>
  
            <div>
              <label>Phone Number</label><br>
              <input type="text" v-model="form.phone_number" placeholder="Phone Number" class="w-full mt-2 py-4 px-6 border border-grey-200 rounded-lg" />
            </div>
  
            <div>
              <label>Email</label><br>
              <input type="email" v-model="form.email" placeholder="Your e-mail address" class="w-full mt-2 py-4 px-6 border border-grey-200 rounded-lg" />
            </div>
  
            <div>
              <label>Password</label><br>
              <div class="relative">
                <input :type="passwordFieldType1" v-model="form.password1" placeholder="Your password"
                  class="w-full mt-2 py-4 px-6 border border-grey-200 rounded-lg pr-12" />
                <button type="button" @click="togglePasswordVisibility1" class="absolute inset-y-0 right-0 flex items-center pr-3">
                  <svg v-if="isPasswordVisible1" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                  </svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88" />
                  </svg>
                </button>
              </div>
            </div>
  
            <div>
              <label>Repeat Password</label><br>
              <div class="relative">
                <input :type="passwordFieldType2" v-model="form.password2" placeholder="Repeat your password"
                  class="w-full mt-2 py-4 px-6 border border-grey-200 rounded-lg pr-12" />
                <button type="button" @click="togglePasswordVisibility2" class="absolute inset-y-0 right-0 flex items-center pr-3">
                  <svg v-if="isPasswordVisible2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                  </svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88" />
                  </svg>
                </button>
              </div>
            </div>
            
            <div class="max-w-md mx-auto p-6 bg-white border border-gray-200 rounded-lg shadow-md">
              <h2 class="text-xl font-semibold mb-4">Password Requirements</h2>
              <ul class="list-disc list-inside text-gray-700">
                <li class="mb-2">At least 8 characters long</li>
                <li class="mb-2">Contains at least one letter</li>
                <li class="mb-2">Contains at least one digit</li>
                <li class="mb-2">Contains at least one special character</li>
              </ul>
            </div>
  
            <template v-if="errors.length > 0">
                <div class="bg-red-300 text-white rounded-lg p-6">
                    <ul class="list-disc pl-5">
                    <li v-for="(error, index) in errors" :key="index">{{ error }}</li>
                    </ul>
                </div>
            </template>
  
            <div>
              <button type="submit" class="py-4 px-6 bg-purple-600 text-white rounded-lg">Sign up</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, computed } from 'vue';
  import axios from 'axios';
  import { useToastStore } from '@/stores/toast';
  import { useRouter } from 'vue-router';
  
  export default {
    name: 'EmployeeCreation',
    setup() {
      const form = ref({
        email: '',
        first_name: '',
        last_name: '',
        phone_number: '',
        password1: '',
        password2: '',
      });
  
      const errors = ref([]);
      const toastStore = useToastStore();
      const router = useRouter();

      // Password visibility states
      const isPasswordVisible1 = ref(false)
      const isPasswordVisible2 = ref(false)
  
      const passwordFieldType1 = computed(() => isPasswordVisible1.value ? 'text' : 'password')
      const passwordFieldType2 = computed(() => isPasswordVisible2.value ? 'text' : 'password')
  
      function togglePasswordVisibility1() {
        isPasswordVisible1.value = !isPasswordVisible1.value
      }
  
      function togglePasswordVisibility2() {
        isPasswordVisible2.value = !isPasswordVisible2.value
      }
  
      const submitForm = async () => {
        errors.value = [];
  
        try {
          const response = await axios.post('/api/accounts/employees', form.value);
          if (response.data.message === 'success') {
            toastStore.showToast(5000, 'The user is registered.', 'bg-green-500');
            form.value.email = '';
            form.value.first_name = '';
            form.value.last_name = '';
            form.value.phone_number = '';
            form.value.password1 = '';
            form.value.password2 = '';
          } else {
            const data = JSON.parse(response.data.message);
            for (const key in data) {
              data[key].forEach(errorObj => {
                errors.value.push(errorObj.message);
              });
            }
            toastStore.showToast(5000, 'Something went wrong. Please try again.', 'bg-red-500');
          }
        } catch (error) {
          toastStore.showToast(5000, 'Something went wrong. Please try again.', 'bg-red-500');
        }
      };
  
      return {
        form,
        errors,
        submitForm,
        togglePasswordVisibility1,
        togglePasswordVisibility2,
        isPasswordVisible1,
        isPasswordVisible2,
        passwordFieldType1,
        passwordFieldType2,
      };
    },
    beforeRouteEnter(to, from, next) {
      axios.get('/api/accounts/owner_permissions/')
        .then(response => {
          if (response.data.is_organization_owner) {
            next();
          } else {
            router.go(-1);
          }
        })
        .catch(error => {
          console.error('Error checking permissions:', error);
        });
    }
  };
  </script>