<template>
    <v-card-subtitle class="text-center card-subtitle"> Welcome back! </v-card-subtitle>

    <v-card-text>
        <v-form :readonly="submit_loading" @submit.prevent="onLoginSubmit">
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
                class="mb-3"
                :type="password_visible ? 'text' : 'password'"
                :append-inner-icon="password_visible ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append-inner="password_visible = !password_visible" />
            <v-btn
                block
                variant="flat"
                color="#3073C4"
                size="x-large"
                class="mb-6"
                type="submit"
                :loading="submit_loading"
                >Log In</v-btn
            >
            <v-btn block variant="tonal" color="#3073C4" size="x-large" @click="onSignUpClick">Sign Up</v-btn>
        </v-form>
    </v-card-text>
</template>

<script lang="ts" setup name="Login">
    import { useToken } from "@/stores/token"
    import { useUserInfo } from "@/stores/userinfo"
    import type { GetUserInfoResponse, LoginResponse } from "@/types"
    import { callapi } from "@/utils/callapi"
    import emitter from "@/utils/emitter"
    import { ref } from "vue"
    import { useRouter } from "vue-router"
    const router = useRouter()
    const token = useToken()
    const userInfo = useUserInfo()

    let password_visible = ref(false)
    let username = ref("")
    let password = ref("")
    let submit_loading = ref(false)

    function onLoginSubmit(event: SubmitEvent) {
        submit_loading.value = true
        if (username.value == "" || password.value == "") {
            submit_loading.value = false
        } else {
            callapi.post(
                "form-data",
                "Auth",
                "login",
                {
                    username: username.value,
                    password: password.value,
                },
                (data) => {
                    token.setUser((<LoginResponse>data).token)
                    callapi.get("UserInfo", "getCurrentUserInfo", null, (data) => {
                        userInfo.fillUser(<GetUserInfoResponse>data)
                        emitter.emit("success_snackbar", "登录成功")
                        router.replace("/home")
                    })
                },
                (errCode) => {
                    submit_loading.value = false
                }
            )
        }
    }

    function onSignUpClick() {
        router.push({ name: "register" })
    }
</script>

<style scoped>
    .card-subtitle {
        font-size: 20px;
        color: black;
    }
</style>
