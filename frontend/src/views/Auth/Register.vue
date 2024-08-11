<template>
    <v-card-subtitle class="text-center card-subtitle"> Let's start! </v-card-subtitle>

    <v-card-text>
        <v-form :readonly="submit_loading" @submit.prevent="onRegisterSubmit">
            <v-text-field
                label="Username"
                :rules="[(v) => !!v || 'Please input the username']"
                v-model="username"
                variant="outlined"
                color="#3073C4"
                prepend-inner-icon="mdi-account-outline"
                class="mb-3"
                type="text" />
            <v-text-field
                label="Password"
                :rules="[(v) => !!v || 'Please input the password']"
                v-model="password"
                variant="outlined"
                color="#3073C4"
                prepend-inner-icon="mdi-lock-outline"
                :type="password_visible ? 'text' : 'password'"
                :append-inner-icon="password_visible ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append-inner="password_visible = !password_visible" />
            <v-checkbox
                label="I agree to the Terms of Service."
                :rules="[(v) => !!v || 'Please agree the Terms of Service.']"
                v-model="agree"
                density="compact"
                color="green"
                class="mb-2" />
            <v-btn block variant="flat" color="#3073C4" size="x-large" type="submit" :loading="submit_loading"
                >Sign Up</v-btn
            >
        </v-form>
    </v-card-text>
</template>

<script lang="ts" setup name="Register">
    import { callapi } from "@/utils/callapi"
    import emitter from "@/utils/emitter"
    import { useRouter } from "vue-router"
    import { ref } from "vue"
    const router = useRouter()

    let password_visible = ref(false)
    let username = ref("")
    let password = ref("")
    let agree = ref(false)
    let submit_loading = ref(false)
    let success_snackbar = ref(false)

    function onRegisterSubmit(event: SubmitEvent) {
        submit_loading.value = true
        if (username.value == "" || password.value == "" || !agree.value) {
            submit_loading.value = false
        } else {
            callapi.post(
                "form-data",
                "Auth",
                "register",
                {
                    username: username.value,
                    password: password.value,
                },
                (data) => {
                    emitter.emit("success_snackbar", "注册成功")
                    router.replace({ name: "login" })
                },
                (errCode) => {
                    submit_loading.value = false
                }
            )
        }
    }
</script>

<style scoped>
    .card-subtitle {
        font-size: 20px;
        color: black;
    }
</style>
