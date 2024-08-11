<template>
    <v-main>
        <v-progress-linear
            :model-value="(nowExercise / globalexerciselist.length) * 100"
            color="green-darken-1"
            absolute
            top></v-progress-linear>

        <v-fab
            color="green"
            prepend-icon="mdi-arrow-u-left-top"
            location="top start"
            position="sticky"
            size="x-large"
            text="返回"
            extended
            app
            @click="goBack"
            class="ml-4 mt-4" />

        <v-container fluid class="w-100 mt-10">
            <v-row class="w-100 justify-center mb-10">
                <p class="text-h4">题目 {{ nowExercise }} / {{ globalexerciselist.length }}</p>
            </v-row>
            <v-row class="w-100 justify-center mb-5">
                <ExerciseFinisher
                    v-model:loading="loading"
                    :exercise="exercise"
                    :isEnd="nowExercise == globalexerciselist.length"
                    @next="next"
                    @showComment="showComment = true" />
            </v-row>
            <v-row class="w-100 justify-center" v-if="showComment">
                <ExerciseComment
                    :exerciseid="exercise.exerciseid"
                    :comment="comment"
                    @refresh="getComment(exercise.exerciseid)" />
            </v-row>
        </v-container>
    </v-main>
</template>

<script lang="ts" setup name="ExerciseView">
    import ExerciseComment from "@/components/ExerciseView/ExerciseComment.vue"
    import ExerciseFinisher from "@/components/ExerciseView/ExerciseFinisher.vue"
    import { useGlobalExerciseList } from "@/stores/globalexerciselist"
    import type { GetCommentByIDResponse, GetExerciseByIDResponse, GotComment, GotExercise } from "@/types"
    import { callapi } from "@/utils/callapi"
    import { onMounted, ref } from "vue"

    const globalexerciselist = useGlobalExerciseList()

    let exercise = ref(<GotExercise>{})
    let comment = ref(<GotComment[]>[])
    let loading = ref(false)

    function getExercise(exerciseid: number) {
        loading.value = true
        callapi.get(
            "Exercise",
            "getExerciseByID",
            {
                exerciseid: exerciseid,
            },
            (data) => {
                exercise.value = (<GetExerciseByIDResponse>data).data
                loading.value = false
            }
        )
        getComment(exerciseid)
    }

    function getComment(exerciseid: number) {
        comment.value = <GotComment[]>[]
        callapi.get(
            "Exercise",
            "getCommentByID",
            {
                exerciseid: exerciseid,
            },
            (data) => {
                comment.value = (<GetCommentByIDResponse>data).comment
            }
        )
    }

    onMounted(() => {
        getExercise(globalexerciselist.list[0])
    })

    let nowExercise = ref(1)
    let showComment = ref(false)

    function next() {
        showComment.value = false
        nowExercise.value += 1
        getExercise(globalexerciselist.list[nowExercise.value - 1])
    }

    function goBack() {
        window.close()
    }
</script>

<style scoped></style>
