<template>
    <v-container fluid class="pa-6">
        <p class="text-h4 mt-6 mb-4">管理员管理</p>
        <p class="text-subtitle-2 mb-4">添加删除管理员</p>

        <v-data-table :headers="headers" :items="allAdmin" item-value="exerciseid" disable-sort sticky>
            <template v-slot:item.actions="{ item }">
                <v-btn
                    variant="tonal"
                    icon
                    density="comfortable"
                    color="red"
                    class="me-1"
                    :disabled="item.adminname == userInfo.username || item.adminname == 'root'"
                    @click="delDialog(item.adminname, item.adminid)">
                    <v-icon size="default"> mdi-account-off </v-icon>
                </v-btn>
            </template>
        </v-data-table>
    </v-container>

    <v-fab
        ref="addDialogActivator"
        color="primary"
        prepend-icon="mdi-account-plus"
        location="top end"
        size="x-large"
        position="sticky"
        text="添加管理员"
        extended
        app
        class="mt-12" />

    <v-dialog :activator="addDialogActivator" max-width="500px" v-model="addDialogActive">
        <v-card>
            <v-toolbar>
                <v-btn icon="mdi-close" @click="addDialogActive = false" />
                <v-toolbar-title>添加管理员</v-toolbar-title>
            </v-toolbar>
            <v-text-field
                v-model="newAdminName"
                :rules="[(v) => !!v || '请输入新管理员名']"
                label="新管理员名"
                variant="outlined"
                class="ma-2" />
            <v-text-field
                v-model="newAdminPassword"
                type="password"
                :rules="[(v) => !!v || '请输入新管理员密码']"
                label="新管理员密码"
                variant="outlined"
                class="ma-2" />
            <template v-slot:actions>
                <v-btn @click="addDialogActive = false">取消</v-btn>
                <v-btn
                    color="primary"
                    :disabled="newAdminName == '' || newAdminPassword == ''"
                    :loading="submit_loading"
                    @click="onAddAdminClick"
                    >添加</v-btn
                >
            </template>
        </v-card>
    </v-dialog>

    <v-dialog max-width="500px" v-model="delDialogActive">
        <v-card>
            <v-toolbar>
                <v-btn icon="mdi-close" @click="delDialogActive = false" />
                <v-toolbar-title>删除管理员</v-toolbar-title>
            </v-toolbar>

            <v-card-item> 确定要删除管理员“{{ delDialogAdminName }}”？ </v-card-item>

            <template v-slot:actions>
                <v-btn @click="delDialogActive = false">取消</v-btn>
                <v-btn color="red" :loading="submit_loading" @click="onDelAdminClick"> 删除 </v-btn>
            </template>
        </v-card>
    </v-dialog>
</template>

<script lang="ts" setup name="AdminManagement">
    import { useUserInfo } from "@/stores/userinfo"
    import type { AdminAdmin, GetAllAdminResponse } from "@/types"
    import { callapi } from "@/utils/callapi"
    import emitter from "@/utils/emitter"
    import { onMounted, ref, watch } from "vue"
    const userInfo = useUserInfo()

    const headers = [
        { title: "ID", value: "adminid" },
        { title: "管理员名", key: "adminname" },
        { title: "操作", key: "actions", sortable: false },
    ]

    let allAdmin = ref(<AdminAdmin[]>[])

    function getAllAdmin() {
        allAdmin.value = <AdminAdmin[]>[]
        callapi.get("Admin", "getAllAdmin", null, (data) => {
            allAdmin.value = (<GetAllAdminResponse>data).admins
        })
    }

    onMounted(() => {
        getAllAdmin()
    })

    let submit_loading = ref(false)

    let addDialogActivator = ref()
    let addDialogActive = ref(false)
    let newAdminName = ref()
    let newAdminPassword = ref()

    function onAddAdminClick() {
        submit_loading.value = true
        callapi.post(
            "form-data",
            "Admin",
            "createAdmin",
            {
                adminname: newAdminName.value,
                password: newAdminPassword.value,
            },
            (data) => {
                emitter.emit("success_snackbar", "添加" + newAdminName.value + "成功")
                submit_loading.value = false
                addDialogActive.value = false
            },
            (errCode) => {
                submit_loading.value = false
            }
        )
    }

    watch(addDialogActive, (newValue, oldValue) => {
        if (oldValue && !newValue) {
            getAllAdmin()
        }
    })

    let delDialogActive = ref(false)
    let delDialogAdminName = ref("")
    let delDialogAdminID = ref(0)

    function delDialog(adminname: string, adminid: number) {
        delDialogAdminName.value = adminname
        delDialogAdminID.value = adminid
        delDialogActive.value = true
    }

    function onDelAdminClick() {
        submit_loading.value = true
        callapi.post(
            "form-data",
            "Admin",
            "deleteAdmin",
            {
                adminid: delDialogAdminID.value,
            },
            (data) => {
                emitter.emit("success_snackbar", "删除" + delDialogAdminName.value + "成功")
                submit_loading.value = false
                delDialogActive.value = false
            },
            (errCode) => {
                submit_loading.value = false
            }
        )
    }

    watch(delDialogActive, (newValue, oldValue) => {
        if (oldValue && !newValue) {
            getAllAdmin()
        }
    })
</script>

<style scoped></style>
