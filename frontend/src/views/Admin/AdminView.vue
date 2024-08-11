<template>
    <v-navigation-drawer expand-on-hover rail permanent>
        <v-list>
            <v-list-item :prepend-avatar="userInfo.avatarurl" :title="userInfo.username" subtitle="管理员" />
        </v-list>

        <v-divider />

        <v-list density="compact" v-model:selected="selected" mandatory nav>
            <v-list-item prepend-icon="mdi-account-circle" title="用户管理" value="userManagement" />
            <v-list-item prepend-icon="mdi-pencil-ruler" title="题目管理" value="exerciseManagement" />
            <v-list-item prepend-icon="mdi-account-star" title="管理员管理" value="adminManagement" />
        </v-list>
    </v-navigation-drawer>

    <v-app-bar density="compact" elevation="1">
        <v-app-bar-title>{{ title_dict[selected[0]] }}</v-app-bar-title>
        <v-spacer />
        <v-btn icon @click="onLogoutClick">
            <v-icon>mdi-logout-variant</v-icon>
        </v-btn>
    </v-app-bar>

    <v-main>
        <RouterView />
    </v-main>
</template>

<script lang="ts" setup name="AdminView">
    import { useToken } from "@/stores/token"
    import { useUserInfo } from "@/stores/userinfo"
    import { callapi } from "@/utils/callapi"
    import { ref, watch } from "vue"
    import { RouterView, useRoute, useRouter } from "vue-router"
    const route = useRoute()
    const router = useRouter()
    const token = useToken()
    const userInfo = useUserInfo()

    const title_dict: {
        [key: string]: string
    } = {
        userManagement: "用户管理",
        exerciseManagement: "题目管理",
        adminManagement: "管理员管理",
    }

    let selected = ref(<string[]>[route.name])

    watch(selected, (newValue) => {
        router.push({ name: newValue[0] })
    })

    function onLogoutClick() {
        callapi.post("form-data", "Auth", "adminLogout", null, (data) => {
            token.clear()
            userInfo.clear()
            router.replace("/")
        })
    }
</script>

<style scoped></style>
