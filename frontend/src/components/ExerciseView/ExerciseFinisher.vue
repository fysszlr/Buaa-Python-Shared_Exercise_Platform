<template>
    <v-card elevation="2" min-width="800px" max-width="800px" class="px-4 pb-0">
        <v-overlay v-model="loading" class="align-center justify-center" contained scrim="grey-lighten-1"> </v-overlay>

        <v-card-title>{{ exercise.title }}</v-card-title>
        <v-card-subtitle class="custom_subtitle"
            >题目类型:{{ exerciseType[exercise.type] }} 题目创建者:{{ exercise.createusername }}
        </v-card-subtitle>
        <v-card-subtitle class="custom_subtitle"></v-card-subtitle>
        <v-card-item>
            <p class="text-subtitle-2">所属题目组</p>
            <v-chip-group :model-value="tagActive" selected-class="bg-green-darken-3" readonly>
                <v-chip v-for="(item, index) in exercise.tag" :key="item.tagid" :value="item.tagid" size="small">
                    {{ item.tagname }}
                </v-chip>
            </v-chip-group>
        </v-card-item>

        <v-divider />
        <v-card-item>
            <pre>{{ exercise.content }}</pre>
        </v-card-item>
        <v-divider />

        <v-card-text class="text-subtitle-1">请作答</v-card-text>
        <v-card-item class="mt-n4">
            <!-- ****************判断题****************** -->
            <v-radio-group v-if="exercise.type === 0" v-model="userAnswer.answer[0]" hide-details>
                <v-radio label="正确" value="A" color="success" />
                <v-radio label="错误" value="B" color="red" />
            </v-radio-group>

            <!-- ****************单选题****************** -->
            <v-radio-group v-if="exercise.type === 1" v-model="userAnswer.answer[0]" hide-details>
                <v-radio
                    v-for="(option, index) in exercise.option"
                    :key="'S' + option"
                    :label="String.fromCharCode(65 + index) + '. ' + exercise.option[index]"
                    :value="String.fromCharCode(65 + index)"
                    color="success" />
            </v-radio-group>

            <!-- ****************多选题****************** -->
            <div v-if="exercise.type === 2">
                <div v-for="(option, index) in exercise.option" :key="'M' + option">
                    <v-checkbox
                        v-model="userAnswer.answer"
                        color="success"
                        hide-details
                        density="compact"
                        :value="String.fromCharCode(65 + index)"
                        :label="String.fromCharCode(65 + index) + '. ' + exercise.option[index]" />
                </div>
            </div>

            <!-- ****************填空题****************** -->
            <div v-if="exercise.type === 10">
                <v-text-field
                    v-model="userAnswer.answer[0]"
                    label="答案"
                    variant="outlined"
                    color="primary"
                    density="compact"
                    hide-details
                    :rules="[(v:string) => !!v]"
                    class="my-2" />
            </div>
        </v-card-item>

        <v-divider />

        <v-card-actions class="d-flex justify-end">
            <v-btn v-if="isFinish && !isEnd" color="green" size="large" prepend-icon="mdi-arrow-right" @click="next"
                >下一题</v-btn
            >
            <v-btn v-else-if="isFinish && isEnd" color="green" size="large" disabled
                >已完成答题，点击左上角返回按钮以返回</v-btn
            >
            <v-btn v-else color="orange" size="large" prepend-icon="mdi-check-circle" @click="submit">完成并提交</v-btn>
        </v-card-actions>
    </v-card>

    <v-dialog max-width="500px" v-model="dialogActive">
        <v-card>
            <v-toolbar>
                <v-btn icon="mdi-close" @click="dialogActive = false" />
                <v-toolbar-title>{{ isRight ? "恭喜你，回答正确！" : "抱歉，回答错误！" }}</v-toolbar-title>
            </v-toolbar>

            <v-img v-if="isRight" src="static/img/right.png" cover></v-img>
            <v-img v-else src="static/img/wrong.png" cover></v-img>

            <template v-slot:actions>
                <v-btn color="primary" @click="dialogActive = false">关闭</v-btn>
            </template>
        </v-card>
    </v-dialog>
</template>

<script lang="ts" setup name="ExerciseFinisher">
    import type { GotExercise } from "@/types"
    import { callapi } from "@/utils/callapi"
    import { computed, ref } from "vue"

    const props = defineProps<{ exercise: GotExercise; isEnd: boolean }>()
    const loading = defineModel("loading", {
        default: false,
    })
    const emit = defineEmits(["next", "showComment"])

    const exerciseType = {
        0: "判断题",
        1: "单选题",
        2: "多选题",
        10: "填空题",
    }

    const tagActive = computed(() => {
        if (props.exercise.tag) {
            return props.exercise.tag.map((value) => value.tagid)
        } else {
            return <number[]>[]
        }
    })

    let userAnswer = ref({
        answer: <string[]>[],
    })

    let isFinish = ref(false)
    let isRight = ref(false)
    let dialogActive = ref(false)

    function submit() {
        isFinish.value = true
        isRight.value = checkAnswer()
        emit("showComment")
        dialogActive.value = true
        if (isRight.value) {
            callapi.post("form-data", "Log", "addRightLog", {
                exerciseid: props.exercise.exerciseid,
            })
        } else {
            callapi.post("form-data", "Log", "addWrongLog", {
                exerciseid: props.exercise.exerciseid,
            })
        }
    }

    function checkAnswer() {
        if (props.exercise.answer.length !== userAnswer.value.answer.length) {
            return false
        }
        const sortedUserAnswer = userAnswer.value.answer.sort()
        const sortedExerciseAnswer = props.exercise.answer.sort()
        for (let i = 0; i < sortedUserAnswer.length; i++) {
            if (sortedUserAnswer[i] !== sortedExerciseAnswer[i]) {
                return false
            }
        }
        return true
    }

    function next() {
        isFinish.value = false
        userAnswer.value.answer = <string[]>[]
        emit("next")
    }
</script>

<style scoped>
    .custom_subtitle {
        color: #55a319;
        font-weight: bold;
    }

    pre {
        white-space: pre-wrap;
    }
</style>
