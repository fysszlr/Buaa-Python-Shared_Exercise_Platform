<template>
    <v-dialog max-width="500px" v-model="isActive">
        <v-card>
            <v-toolbar>
                <v-btn icon="mdi-close" @click="isActive = false" />
                <v-toolbar-title>添加题目到题目组</v-toolbar-title>
            </v-toolbar>
            <v-card-item> 题目ID：{{ exerciseid }} </v-card-item>
            <v-card-item> 题目标题：{{ title }} </v-card-item>

            <v-select
                v-model="newtagid"
                :items="current_user_tag"
                item-title="tagname"
                item-value="tagid"
                :rules="[(v) => !!v || '请选择要添加到的题目组']"
                label="要添加到的题目组"
                variant="outlined"
                class="ma-2" />
            <template v-slot:actions>
                <v-btn @click="isActive = false">取消</v-btn>
                <v-btn color="primary" :disabled="newtagid == ''" :loading="submit_loading" @click="onAddToTagClick"
                    >添加题目组</v-btn
                >
            </template>
        </v-card>
    </v-dialog>
</template>

<script lang="ts" setup name="AddExerciseToTag">
    import { callapi } from "@/utils/callapi"
    import emitter from "@/utils/emitter"
    import { ref } from "vue"

    const props = defineProps(["current_user_tag", "exerciseid", "title"])

    const emit = defineEmits(["add_finish"])

    let isActive = defineModel({ default: false })

    let submit_loading = ref(false)
    let newtagid = ref()

    function onAddToTagClick() {
        submit_loading.value = true
        callapi.post(
            "form-data",
            "Tag",
            "addExerciseToTag",
            {
                tagid: newtagid.value,
                exerciseid: props.exerciseid,
            },
            (data) => {
                emit("add_finish")
                emitter.emit("success_snackbar", "添加到题目组成功")
                newtagid.value = null
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
