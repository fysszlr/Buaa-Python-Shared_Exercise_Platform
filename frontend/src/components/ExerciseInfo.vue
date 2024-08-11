<template>
    <v-dialog ax-width="500px" v-model="isActive">
        <v-card>
            <v-toolbar>
                <v-btn icon="mdi-close" @click="isActive = false" />
                <v-toolbar-title>题目信息</v-toolbar-title>
            </v-toolbar>

            <v-expansion-panels multiple variant="accordion" v-model="defaultActive">
                <v-expansion-panel>
                    <v-expansion-panel-title>标题</v-expansion-panel-title>
                    <v-expansion-panel-text> {{ exercise.title }} </v-expansion-panel-text>
                </v-expansion-panel>
                <v-expansion-panel>
                    <v-expansion-panel-title>创建者</v-expansion-panel-title>
                    <v-expansion-panel-text> {{ exercise.createusername }} </v-expansion-panel-text>
                </v-expansion-panel>
                <v-expansion-panel>
                    <v-expansion-panel-title>类型</v-expansion-panel-title>
                    <v-expansion-panel-text> {{ exerciseType[exercise.type] }} </v-expansion-panel-text>
                </v-expansion-panel>
                <v-expansion-panel>
                    <v-expansion-panel-title>题面</v-expansion-panel-title>
                    <v-expansion-panel-text>
                        <pre>{{ exercise.content }}</pre>
                    </v-expansion-panel-text>
                </v-expansion-panel>
                <v-expansion-panel v-show="exercise.type != 0 && exercise.type != 10">
                    <v-expansion-panel-title>选项</v-expansion-panel-title>
                    <v-expansion-panel-text>
                        <pre>{{ computedOption }}</pre>
                    </v-expansion-panel-text>
                </v-expansion-panel>
                <v-expansion-panel v-if="showAnswer">
                    <v-expansion-panel-title>答案</v-expansion-panel-title>
                    <v-expansion-panel-text>
                        <pre>{{ computedAnswer }}</pre>
                    </v-expansion-panel-text>
                </v-expansion-panel>
                <v-expansion-panel>
                    <v-expansion-panel-title>题目组</v-expansion-panel-title>
                    <v-expansion-panel-text>
                        <v-chip v-for="tag in exercise.tag" :key="tag.tagid" color="secondary" label class="me-1">{{
                            tag.tagname
                        }}</v-chip>
                    </v-expansion-panel-text>
                </v-expansion-panel>
            </v-expansion-panels>
        </v-card>
    </v-dialog>
</template>

<script lang="ts" setup name="ExerciseInfo">
    import { computed, ref } from "vue"
    import type { GotExercise } from "@/types"

    const exerciseType = {
        0: "判断题",
        1: "单选题",
        2: "多选题",
        10: "填空题",
    }

    let isActive = defineModel({ default: false })

    const props = defineProps<{ exercise: GotExercise; showAnswer: boolean }>()

    let defaultActive = ref([0, 1, 2, 3, 4, 5, 6])

    const computedOption = computed(() => {
        if (props.exercise.type === 0 || props.exercise.type === 10) {
            return ""
        } else {
            return (
                "A. " +
                props.exercise.option.reduce((previousValue, currentValue, currentIndex) => {
                    return previousValue + "\n" + String.fromCharCode(65 + currentIndex) + ". " + currentValue
                })
            )
        }
    })

    const computedAnswer = computed(() => {
        if (props.exercise.type === 0) {
            if (props.exercise.answer[0] == "A") {
                return "正确"
            } else if (props.exercise.answer[0] == "B") {
                return "错误"
            }
        } else {
            return props.exercise.answer.reduce((previousValue, currentValue) => {
                return previousValue + ", " + currentValue
            })
        }
    })
</script>

<style scoped>
    pre {
        white-space: pre-wrap;
    }
</style>
