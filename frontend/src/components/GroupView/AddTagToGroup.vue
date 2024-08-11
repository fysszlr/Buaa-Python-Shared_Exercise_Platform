<template>
    <v-dialog max-width="500px" v-model="isActive">
        <v-card>
            <v-toolbar>
                <v-btn icon="mdi-close" @click="isActive = false" />
                <v-toolbar-title>共享题目组到此共享群组</v-toolbar-title>
            </v-toolbar>

            <v-select
                v-model="addtagid"
                :items="current_user_tag"
                item-title="tagname"
                item-value="tagid"
                :rules="[(v) => !!v || '请选择要共享的题目组']"
                label="要共享的题目组"
                variant="outlined"
                class="ma-2" />
            <template v-slot:actions>
                <v-btn @click="isActive = false">取消</v-btn>
                <v-btn
                    color="primary"
                    :disabled="addtagid == ''"
                    :loading="submit_loading"
                    @click="onAddTagToGroupClick"
                    >共享题目组</v-btn
                >
            </template>
        </v-card>
    </v-dialog>
</template>

<script lang="ts" setup name="AddTagToGroup">
    import { callapi } from "@/utils/callapi"
    import emitter from "@/utils/emitter"
    import { ref } from "vue"

    const props = defineProps(["current_user_tag", "groupid"])

    const emit = defineEmits(["add_finish"])

    let isActive = defineModel({ default: false })

    let submit_loading = ref(false)
    let addtagid = ref()

    function onAddTagToGroupClick() {
        submit_loading.value = true
        callapi.post(
            "form-data",
            "Group",
            "addTagToGroup",
            {
                groupid: props.groupid,
                tagid: addtagid.value,
            },
            (data) => {
                emit("add_finish")
                emitter.emit("success_snackbar", "共享题目组成功")
                addtagid.value = null
                submit_loading.value = false
                isActive.value = false
            },
            (errCode) => {
                submit_loading.value = false
            }
        )
    }
</script>

<style scoped></style>
