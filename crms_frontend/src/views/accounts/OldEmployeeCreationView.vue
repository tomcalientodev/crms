<template>
    <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
        <div class="main-left">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <h1 class="mb-6 text-2xl">Employee Creation</h1>
                <p class="mb-6 text-gray-500">
                    Lorem ipsum dolor sit amet consectetur adipisicing elit.
                    Lorem ipsum dolor sit amet consectetur adipisicing elit.
                </p>
            </div>
        </div>

        <div class="main-right">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <form class="space-y-6" v-on:submit.prevent="submitForm">
                    <!-- prevent means don't refresh screen, use the submitForm JS function below. -->

                    <div>
                        <label>First Name</label><br>
                        <input type="text" v-model="form.first_name" placeholder="Your First Name"
                            class="w-full mt-2 py-4 px-6 border border-grey-200 rounded-lg" />
                    </div>

                    <div>
                        <label>Last Name</label><br>
                        <input type="text" v-model="form.last_name" placeholder="Your Last Name"
                            class="w-full mt-2 py-4 px-6 border border-grey-200 rounded-lg" />
                    </div>

                    <div>
                        <label>Phone Number</label><br>
                        <input type="text" id="phone" v-model="form.phone_number" placeholder="Phone Number"
                            class="w-full mt-2 py-4 px-6 border border-grey-200 rounded-lg" />
                    </div>

                    <div>
                        <label>Email</label><br>
                        <input type="email" v-model="form.email" placeholder="Your e-mail address"
                            class="w-full mt-2 py-4 px-6 border border-grey-200 rounded-lg" />
                    </div>

                    <div>
                        <label>Password</label><br>
                        <input type="password" v-model="form.password1" placeholder="Your password"
                            class="w-full mt-2 py-4 px-6 border border-grey-200 rounded-lg" />
                    </div>

                    <div>
                        <label>Repeat Password</label><br>
                        <input type="password" v-model="form.password2" placeholder="Repeat your password"
                            class="w-full mt-2 py-4 px-6 border border-grey-200 rounded-lg" />
                    </div>

                    <template v-if="errors.length > 0">
                        <div class="bg-red-300 text-white rounded-lg p-6">
                            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                            <!-- key makes error unique or it won't work.-->
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

import axios from 'axios'
import { useToastStore } from '@/stores/toast'
import router from '@/router';

export default {
    setup() {
        const toastStore = useToastStore()

        return {
            toastStore
        }
    },
    data() {
        return {
            form: {
                email: '',
                first_name: '',
                last_name: '',
                phone_number: '',
                password1: '',
                password2: '',

            },
            errors: [],
        }
    },
    methods: {

        submitForm() {
            this.errors = [] //if we do anything wrong it will be reset.

            if (this.form.email === '') {
                this.errors.push("Your email is missing.") //push string into list of errors.
            }

            if (this.form.first_name === '') {
                this.errors.push("Your first name is missing.") //push string into list of errors.
            }

            if (this.form.last_name === '') {
                this.errors.push("Your last name is missing.") //push string into list of errors.
            }

            if (this.form.phone_number === '') {
                this.errors.push("Your phone number is missing."); // Push missing phone number error into list of errors.
            } else if (!this.validatePhoneNumber()) {
                this.errors.push('Invalid phone number. Please enter a 10-digit number.'); // Push invalid phone number error into list of errors.
            }

            if (this.form.password1 === '') {
                this.errors.push("Your password is missing.") //push string into list of errors.
            }

            if (this.form.password1 !== this.form.password2) {
                this.errors.push('The password does not match')
            }

            if (this.errors.length === 0) {
                axios
                    .post('/api/accounts/employees', this.form) //we stored the form data in beginning of script.
                    .then((response) => {
                        if (response.data.message === 'success') {
                            this.toastStore.showToast(5000, 'The user is registered. Please activate your account by clicking on the email link we sent.  ', 'bg-green-500')

                            this.form.email = ''
                            this.form.first_name = ''
                            this.form.last_name = ''
                            this.form.phone_number = ''
                            this.form.password1 = ''
                            this.form.password2 = '' //reset the form after user is created so no data is stored.

                        } else {
                            const data = JSON.parse(response.data.message); //see account>api.py>signup function for more info.
                            for (const key in data) {
                                this.errors.push(data[key][0].message) //.push makes it show up on the html page and you can use it to go to any page like a redirect.
                            }
                            this.toastStore.showToast(5000, 'Something went wrong. Pease try again.', 'bg-red-500'); // probably can delete this.
                        }
                    }) 
                
            }   
    },
        validatePhoneNumber() {
            const phoneRegex = /^\d{10}$/;
            return phoneRegex.test(this.form.phone_number);
        },

        
    
    },

    beforeRouteEnter(to, from, next) {
        // Check permissions before entering the route
        axios.get('/api/accounts/owner_permissions/')
            .then(response => {
                if (response.data.is_organization_owner) {
                    // If the user has permission, proceed to the route
                    next();
                } else {
                    // If the user doesn't have permission, redirect to another route
                    router.go(-1);
                }
            })
            .catch(error => {
                console.error('Error checking permissions:', error);
            });

    }
}
</script>
