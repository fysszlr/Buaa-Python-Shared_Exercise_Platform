<template>
    <v-container fluid class="fill-height">
        <v-row class="fill-height" justify="center" align-content="start">
            <v-col cols="6" align-self="start">
                <p class="text-h6">第一步：OCR识别</p>
                <p class="text-subtitle-1 mb-1">使用OCR提取文件中的问题</p>
                <OCR />
            </v-col>
            <v-col>
                <p class="text-h6">第二步：创建题目</p>
                <p class="text-subtitle-1 mb-1">可以同时创建多个题目</p>
                <div v-for="(value, key) in new_exercise_list" :key="key" class="mb-4">
                    <ExerciseUpdater
                        v-model="new_exercise_list[key]"
                        :limit_textarea="false"
                        :current_user_tag="currentUserTag"
                        @add_tag="addTagDialogActive = true" />
                </div>
            </v-col>
        </v-row>
    </v-container>

    <v-fab
        color="primary"
        prepend-icon="mdi-plus"
        location="top end"
        size="x-large"
        position="sticky"
        text="添加题目"
        extended
        app
        @click="pushNewExercise"
        class="mt-4" />

    <AddTag v-model="addTagDialogActive" @add_finish="getCurrentUserTag" />
</template>

<script lang="ts" setup name="CreateExercise">
    import OCR from "@/components/CreateExercise/OCR.vue"
    import ExerciseUpdater from "@/components/ExerciseUpdater.vue"
    import type { PublicTag, GetCurrentUserTagResponse, NewExerciseItem } from "@/types"
    import { callapi } from "@/utils/callapi"
    import { getNewExerciseModel } from "@/utils/exercise"
    import { onMounted, reactive, ref } from "vue"
    import AddTag from "@/components/AddTag.vue"

    interface NewExerciseList {
        [key: number]: NewExerciseItem
    }

    let addTagDialogActive = ref(false)
    let currentUserTag = ref(<PublicTag[]>[])

    function getCurrentUserTag() {
        callapi.get("Tag", "getCurrentUserTag", null, (data) => {
            currentUserTag.value = (<GetCurrentUserTagResponse>data).tag
        })
    }

    onMounted(() => {
        getCurrentUserTag()
    })

    let new_exercise_list = reactive(<NewExerciseList>{})

    function pushNewExercise() {
        new_exercise_list[Date.now()] = {
            exerciseid: undefined,
            exercise: getNewExerciseModel(),
        }
    }
</script>

<style scoped></style>
