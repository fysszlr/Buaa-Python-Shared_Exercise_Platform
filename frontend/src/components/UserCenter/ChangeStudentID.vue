<template>
    <v-dialog :activator="activator" max-width="500px" v-model="isActive">
        <v-card>
            <v-toolbar>
                <v-btn icon="mdi-close" @click="isActive = false" />
                <v-toolbar-title>修改学号</v-toolbar-title>
            </v-toolbar>
            <v-text-field
                v-model="newstudentid"
                :rules="[(v) => !!v || '请输入新学号']"
                label="新学号"
                variant="outlined"
                class="ma-2" />
            <template v-slot:actions>
                <v-btn @click="isActive = false">取消</v-btn>
                <v-btn
                    color="primary"
                    :disabled="newstudentid == ''"
                    :loading="submit_loading"
                    @click="onChangeStudentIDClick"
                    >修改学号</v-btn
                >
            </template>
        </v-card>
    </v-dialog>
</template>

<script lang="ts" setup name="ChangeStudentID">
    import { useUserInfo } from "@/stores/userinfo"
    import type { UpdateStudentIDResponse } from "@/types"
    import { callapi } from "@/utils/callapi"
    import emitter from "@/utils/emitter"
    import { ref } from "vue"

    defineProps(["activator"])

    const userInfo = useUserInfo()

    let isActive = ref(false)
    let submit_loading = ref(false)
    let newstudentid = ref("")

    function onChangeStudentIDClick() {
        submit_loading.value = true
        callapi.post(
            "form-data",
            "UserInfo",
            "updateStudentID",
            {
                newstudentid: newstudentid.value,
            },
            (data) => {
                userInfo.studentid = (<UpdateStudentIDResponse>data).studentid
                emitter.emit("success_snackbar", "修改学号成功")
                newstudentid.value = ""
                submit_loading.value = false
                isActive.value = false
            },
            (errCode) => {
                submit_loading.value = false
            }
        )
    }
</script>
