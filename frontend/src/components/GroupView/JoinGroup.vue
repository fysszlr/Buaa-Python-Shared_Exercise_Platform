<template>
    <v-dialog max-width="500px" v-model="isActive">
        <v-card>
            <v-toolbar>
                <v-btn icon="mdi-close" @click="isActive = false" />
                <v-toolbar-title>加入共享群组</v-toolbar-title>
            </v-toolbar>
            <v-text-field
                v-model="joingroupid"
                :rules="[(v) => !!v || '请输入共享群组ID']"
                label="共享群组ID"
                variant="outlined"
                type="number"
                class="ma-2" />
            <template v-slot:actions>
                <v-btn @click="isActive = false">取消</v-btn>
                <v-btn
                    color="primary"
                    :disabled="joingroupid == '' || joingroupid == null"
                    :loading="submit_loading"
                    @click="onJoinGroupClick"
                    >加入共享群组</v-btn
                >
            </template>
        </v-card>
    </v-dialog>
</template>

<script lang="ts" setup name="JoinGroup">
    import { callapi } from "@/utils/callapi"
    import emitter from "@/utils/emitter"
    import { ref } from "vue"

    const emit = defineEmits(["add_finish"])

    let isActive = defineModel({ default: false })

    let submit_loading = ref(false)
    let joingroupid = ref(null)

    function onJoinGroupClick() {
        submit_loading.value = true
        callapi.post(
            "form-data",
            "Group",
            "joinGroup",
            {
                groupid: joingroupid.value,
            },
            (data) => {
                emit("add_finish")
                emitter.emit("success_snackbar", "加入共享群组成功")
                joingroupid.value = null
                submit_loading.value = false
                isActive.value = false
            },
            (errCode) => {
                submit_loading.value = false
            }
        )
    }
</script>
