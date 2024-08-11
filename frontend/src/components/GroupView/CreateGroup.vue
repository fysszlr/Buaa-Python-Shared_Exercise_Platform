<template>
    <v-dialog max-width="500px" v-model="isActive">
        <v-card>
            <v-toolbar>
                <v-btn icon="mdi-close" @click="isActive = false" />
                <v-toolbar-title>创建共享群组</v-toolbar-title>
            </v-toolbar>
            <v-text-field
                v-model="newgroupname"
                :rules="[(v) => !!v || '请输入新共享群组名称']"
                label="新共享群组名称"
                variant="outlined"
                class="ma-2" />
            <template v-slot:actions>
                <v-btn @click="isActive = false">取消</v-btn>
                <v-btn
                    color="primary"
                    :disabled="newgroupname == ''"
                    :loading="submit_loading"
                    @click="onCreateGroupClick"
                    >创建共享群组</v-btn
                >
            </template>
        </v-card>
    </v-dialog>
</template>

<script lang="ts" setup name="CreateGroup">
    import { callapi } from "@/utils/callapi"
    import emitter from "@/utils/emitter"
    import { ref } from "vue"

    const emit = defineEmits(["add_finish"])

    let isActive = defineModel({ default: false })

    let submit_loading = ref(false)
    let newgroupname = ref("")

    function onCreateGroupClick() {
        submit_loading.value = true
        callapi.post(
            "form-data",
            "Group",
            "createGroup",
            {
                groupname: newgroupname.value,
            },
            (data) => {
                emit("add_finish")
                emitter.emit("success_snackbar", "创建共享群组成功")
                newgroupname.value = ""
                submit_loading.value = false
                isActive.value = false
            },
            (errCode) => {
                submit_loading.value = false
            }
        )
    }
</script>
