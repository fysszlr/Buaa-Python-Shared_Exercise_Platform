<template>
    <v-dialog :activator="activator" max-width="500px" v-model="isActive">
        <v-card>
            <v-toolbar>
                <v-btn icon="mdi-close" @click="isActive = false" />
                <v-toolbar-title>修改头像</v-toolbar-title>
            </v-toolbar>
            <v-file-input
                v-model="newavatar"
                :rules="[(v) => !!v.length || '请选择图片文件']"
                accept="image/*"
                label="新头像图片文件"
                clearable
                variant="outlined"
                class="ma-2" />
            <template v-slot:actions>
                <v-btn @click="isActive = false">取消</v-btn>
                <v-btn
                    color="primary"
                    :disabled="newavatar == null"
                    :loading="submit_loading"
                    @click="onChangeAvatarClick"
                    >更换头像</v-btn
                >
            </template>
        </v-card>
    </v-dialog>
</template>

<script lang="ts" setup name="ChangeAvatar">
    import { useUserInfo } from "@/stores/userinfo"
    import type { UpdateAvatarResponse } from "@/types"
    import { callapi } from "@/utils/callapi"
    import emitter from "@/utils/emitter"
    import { ref } from "vue"

    defineProps(["activator"])

    const userInfo = useUserInfo()

    let isActive = ref(false)
    let submit_loading = ref(false)
    let newavatar = ref(null)

    function onChangeAvatarClick() {
        submit_loading.value = true
        callapi.post(
            "form-data",
            "UserInfo",
            "updateAvatar",
            {
                newavatar: newavatar.value,
            },
            (data) => {
                userInfo.avatarurl = (<UpdateAvatarResponse>data).avatarurl
                emitter.emit("success_snackbar", "更换头像成功")
                newavatar.value = null
                submit_loading.value = false
                isActive.value = false
            },
            (errCode) => {
                submit_loading.value = false
            }
        )
    }
</script>
