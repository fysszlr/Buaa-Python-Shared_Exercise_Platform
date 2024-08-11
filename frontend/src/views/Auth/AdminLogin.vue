<template>
    <v-card-subtitle class="text-center card-subtitle"> Administrator Login </v-card-subtitle>

    <v-card-text>
        <v-form :readonly="submit_loading" @submit.prevent="onAdminLoginSubmit">
            <v-text-field
                label="Administrator name"
                :rules="[(v) => !!v || 'Please input the administrator name']"
                v-model="adminname"
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
            <v-btn block variant="flat" color="#3073C4" size="x-large" type="submit" :loading="submit_loading"
                >Login In</v-btn
            >
        </v-form>
    </v-card-text>
</template>

<script lang="ts" setup name="AdminLogin">
    import { useToken } from "@/stores/token"
    import { useUserInfo } from "@/stores/userinfo"
    import type { LoginResponse } from "@/types"
    import { callapi } from "@/utils/callapi"
    import emitter from "@/utils/emitter"
    import { useRouter } from "vue-router"
    import { ref } from "vue"
    const router = useRouter()
    const token = useToken()
    const userInfo = useUserInfo()

    let password_visible = ref(false)
    let adminname = ref("")
    let password = ref("")
    let submit_loading = ref(false)

    function onAdminLoginSubmit(event: SubmitEvent) {
        submit_loading.value = true
        if (adminname.value == "" || password.value == "") {
            submit_loading.value = false
        } else {
            callapi.post(
                "form-data",
                "Auth",
                "adminLogin",
                {
                    adminname: adminname.value,
                    password: password.value,
                },
                (data) => {
                    token.setAdmin((<LoginResponse>data).token)
                    userInfo.fillAdmin(adminname.value)
                    emitter.emit("success_snackbar", "登录成功")
                    router.replace("/admin")
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
