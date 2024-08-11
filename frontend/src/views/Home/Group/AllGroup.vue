<template>
    <p class="text-h4 mt-6 mb-4">共享群组</p>
    <p class="text-subtitle-2 mb-4">通过共享群组共享题目</p>

    <v-container fluid class="d-flex fill-height">
        <v-card v-for="group in currentUserGroup" width="23%" class="my-3 me-3">
            <v-card-title>{{ group.groupname }}</v-card-title>
            <v-card-text>
                <p class="mb-3">群组ID： {{ group.groupid }}</p>
                <span>
                    创建者：
                    <v-avatar :image="group.createavatarurl" size="small" rounded="50" />
                    {{ group.createusername }}</span
                >
            </v-card-text>
            <v-card-actions>
                <v-btn color="deep-purple-lighten-2" block variant="tonal" @click="goTo(group.groupid)"
                    >进入共享群组</v-btn
                >
            </v-card-actions>

            <v-card-actions>
                <v-btn
                    v-if="group.createusername == userInfo.username"
                    color="red-lighten-2"
                    block
                    variant="tonal"
                    @click="confirmDialog(true, group.groupname, group.groupid)"
                    >删除</v-btn
                >

                <v-btn
                    v-else
                    color="orange-lighten-2"
                    block
                    variant="tonal"
                    @click="confirmDialog(false, group.groupname, group.groupid)"
                    >退出</v-btn
                >
            </v-card-actions>
        </v-card>
    </v-container>

    <v-fab
        color="primary"
        prepend-icon="mdi-account-multiple-check"
        location="top end"
        size="x-large"
        position="sticky"
        text="创建共享群组"
        extended
        app
        @click="createGroupDialogActive = true"
        class="mt-4" />

    <v-fab
        color="purple"
        prepend-icon="mdi-account-multiple-plus"
        location="bottom end"
        size="x-large"
        position="sticky"
        text="加入共享群组"
        extended
        app
        @click="joinGroupDialogActive = true"
        class="mt-4" />

    <CreateGroup v-model="createGroupDialogActive" @add_finish="getCurrentUserGroup" />

    <JoinGroup v-model="joinGroupDialogActive" @add_finish="getCurrentUserGroup" />

    <v-dialog max-width="500px" v-model="confirmDialogActive">
        <v-card>
            <v-toolbar>
                <v-btn icon="mdi-close" @click="confirmDialogActive = false" />
                <v-toolbar-title>{{ confirmDialogType ? "删除" : "退出" }}共享群组</v-toolbar-title>
            </v-toolbar>

            <v-card-item>
                确定要{{ confirmDialogType ? "删除" : "退出" }}共享群组“{{ confirmDialogGroupName }}”？
            </v-card-item>

            <template v-slot:actions>
                <v-btn @click="confirmDialogActive = false">取消</v-btn>
                <v-btn color="red" :loading="submit_loading" @click="onBlockUnblockClick">
                    {{ confirmDialogType ? "删除" : "退出" }}
                </v-btn>
            </template>
        </v-card>
    </v-dialog>
</template>

<script lang="ts" setup name="AllGroup">
    import CreateGroup from "@/components/GroupView/CreateGroup.vue"
    import JoinGroup from "@/components/GroupView/JoinGroup.vue"
    import router from "@/router"
    import { useUserInfo } from "@/stores/userinfo"
    import type { GetCurrentUserGroupResponse, GotGroup } from "@/types"
    import { callapi } from "@/utils/callapi"
    import emitter from "@/utils/emitter"
    import { onMounted, ref, watch } from "vue"
    const userInfo = useUserInfo()

    let currentUserGroup = ref(<GotGroup[]>[])

    function getCurrentUserGroup() {
        callapi.get("Group", "getCurrentUserGroup", null, (data) => {
            currentUserGroup.value = (<GetCurrentUserGroupResponse>data).group
        })
    }

    onMounted(() => {
        getCurrentUserGroup()
    })

    function goTo(index: number) {
        router.push({
            name: "groupDetail",
            params: {
                groupid: index,
            },
        })
    }

    let createGroupDialogActive = ref(false)

    let joinGroupDialogActive = ref(false)

    let confirmDialogActive = ref(false)
    let confirmDialogType = ref(false)
    let confirmDialogGroupName = ref("")
    let confirmDialogGroupID = ref(0)

    function confirmDialog(isDelete: boolean, groupname: string, groupid: number) {
        confirmDialogType.value = isDelete
        confirmDialogGroupName.value = groupname
        confirmDialogGroupID.value = groupid
        confirmDialogActive.value = true
    }

    let submit_loading = ref(false)

    function onBlockUnblockClick() {
        submit_loading.value = true
        callapi.post(
            "form-data",
            "Group",
            confirmDialogType.value ? "deleteGroup" : "exitGroup",
            {
                groupid: confirmDialogGroupID.value,
            },
            (data) => {
                emitter.emit(
                    "success_snackbar",
                    (confirmDialogType.value ? "删除" : "退出") + confirmDialogGroupName.value + "成功"
                )
                submit_loading.value = false
                confirmDialogActive.value = false
            },
            (errCode) => {
                submit_loading.value = false
            }
        )
    }

    watch(confirmDialogActive, (newValue, oldValue) => {
        if (oldValue && !newValue) {
            getCurrentUserGroup()
        }
    })
</script>

<style scoped></style>
