<template>
    <v-dialog max-width="500px" v-model="isActive">
        <v-card>
            <v-toolbar>
                <v-btn icon="mdi-close" @click="isActive = false" />
                <v-toolbar-title>添加题目组</v-toolbar-title>
            </v-toolbar>
            <v-text-field
                v-model="newtagname"
                :rules="[(v) => !!v || '请输入新题目组名称']"
                label="新题目组名称"
                variant="outlined"
                class="ma-2" />
            <template v-slot:actions>
                <v-btn @click="isActive = false">取消</v-btn>
                <v-btn color="primary" :disabled="newtagname == ''" :loading="submit_loading" @click="onAddTagClick"
                    >添加题目组</v-btn
                >
            </template>
        </v-card>
    </v-dialog>
</template>

<script lang="ts" setup name="AddTag">
    import { callapi } from "@/utils/callapi"
    import emitter from "@/utils/emitter"
    import { ref } from "vue"

    const emit = defineEmits(["add_finish"])

    let isActive = defineModel({ default: false })

    let submit_loading = ref(false)
    let newtagname = ref("")

    function onAddTagClick() {
        submit_loading.value = true
        callapi.post(
            "form-data",
            "Tag",
            "createTag",
            {
                tagname: newtagname.value,
            },
            (data) => {
                emit("add_finish")
                emitter.emit("success_snackbar", "添加题目组成功")
                newtagname.value = ""
                submit_loading.value = false
                isActive.value = false
            },
            (errCode) => {
                submit_loading.value = false
            }
        )
    }
</script>
