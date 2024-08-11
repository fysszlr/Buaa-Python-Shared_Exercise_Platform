<template>
    <v-container fluid class="pa-6">
        <p class="text-h4 mt-6 mb-4">所有用户</p>
        <p class="text-subtitle-2 mb-4">封禁、解封用户</p>

        <v-data-table :headers="headers" :items="allUser" item-value="exerciseid" disable-sort sticky>
            <template v-slot:item.avatarurl="{ item }">
                <v-avatar :image="item.avatarurl" size="small" rounded="50" />
            </template>

            <template v-slot:item.studentid="{ item }">
                {{ item.studentid ? item.studentid : "未填写" }}
            </template>

            <template v-slot:item.actions="{ item }">
                <v-btn
                    v-if="item.isblock"
                    variant="tonal"
                    icon
                    density="comfortable"
                    color="green"
                    class="me-1"
                    @click="dialog(true, item.username, item.userid)">
                    <v-icon size="default"> mdi-account-check </v-icon>
                </v-btn>
                <v-btn
                    v-else
                    variant="tonal"
                    icon
                    density="comfortable"
                    color="red"
                    class="me-1"
                    @click="dialog(false, item.username, item.userid)">
                    <v-icon size="default"> mdi-account-off </v-icon>
                </v-btn>
            </template>
        </v-data-table>
    </v-container>

    <v-dialog max-width="500px" v-model="dialogActive">
        <v-card>
            <v-toolbar>
                <v-btn icon="mdi-close" @click="dialogActive = false" />
                <v-toolbar-title>{{ dialogType ? "解封" : "封禁" }}用户</v-toolbar-title>
            </v-toolbar>

            <v-card-item> 确定要{{ dialogType ? "解封" : "封禁" }}用户“{{ dialogUserName }}”？ </v-card-item>

            <template v-slot:actions>
                <v-btn @click="dialogActive = false">取消</v-btn>
                <v-btn :color="dialogType ? 'green' : 'red'" :loading="submit_loading" @click="onBlockUnblockClick">
                    {{ dialogType ? "解封" : "封禁" }}
                </v-btn>
            </template>
        </v-card>
    </v-dialog>
</template>

<script lang="ts" setup name="UserManagement">
    import type { AdminUser, GetAllUserResponse } from "@/types"
    import { callapi } from "@/utils/callapi"
    import emitter from "@/utils/emitter"
    import { onMounted, ref, watch } from "vue"

    const headers = [
        { title: "ID", value: "userid" },
        { title: "头像", key: "avatarurl" },
        { title: "用户名", key: "username" },
        { title: "学号", key: "studentid" },
        { title: "操作", key: "actions", sortable: false },
    ]

    let allUser = ref(<AdminUser[]>[])

    function getAllUser() {
        allUser.value = <AdminUser[]>[]
        callapi.get("Admin", "getAllUser", null, (data) => {
            allUser.value = (<GetAllUserResponse>data).users
        })
    }

    onMounted(() => {
        getAllUser()
    })

    let dialogActive = ref(false)
    let dialogType = ref(false)
    let dialogUserName = ref("")
    let dialogUserID = ref(0)

    function dialog(isunblock: boolean, username: string, userid: number) {
        dialogType.value = isunblock
        dialogUserName.value = username
        dialogUserID.value = userid
        dialogActive.value = true
    }

    let submit_loading = ref(false)

    function onBlockUnblockClick() {
        submit_loading.value = true
        callapi.post(
            "form-data",
            "Admin",
            dialogType.value ? "unblockUser" : "blockUser",
            {
                userid: dialogUserID.value,
            },
            (data) => {
                emitter.emit("success_snackbar", (dialogType.value ? "解封" : "封禁") + dialogUserName.value + "成功")
                submit_loading.value = false
                dialogActive.value = false
            },
            (errCode) => {
                submit_loading.value = false
            }
        )
    }

    watch(dialogActive, (newValue, oldValue) => {
        if (oldValue && !newValue) {
            getAllUser()
        }
    })
</script>

<style scoped></style>
