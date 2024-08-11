<template>
    <v-card elevation="4" class="pa-4 pb-0">
        <v-text-field
            v-model="modal.exercise.title"
            label="标题"
            variant="outlined"
            color="primary"
            density="compact"
            hide-details
            :rules="[(v:string) => !!v ]" />

        <p class="text-subtitle-2 mt-2">题目类型</p>
        <v-chip-group v-model="modal.exercise.type" mandatory selected-class="bg-blue-darken-3">
            <v-chip :value="0">判断题</v-chip>
            <v-chip :value="1">单选题</v-chip>
            <v-chip :value="2">多选题</v-chip>
            <v-chip :value="10">填空题</v-chip>
        </v-chip-group>

        <v-textarea
            v-model="modal.exercise.content"
            label="题面"
            variant="outlined"
            color="primary"
            density="compact"
            hide-details
            :auto-grow="!limit_textarea"
            no-resize
            clearable
            :rules="[(v:string) => !!v]"
            class="mt-2" />

        <v-divider />

        <!-- ****************判断题****************** -->
        <v-radio-group v-if="modal.exercise.type === 0" v-model="modal.exercise.answer[0]" hide-details>
            <p class="text-subtitle-2 mt-2">正确选项</p>
            <v-radio label="正确" value="A" color="success" />
            <v-radio label="错误" value="B" color="red" />
        </v-radio-group>

        <!-- ****************单选题****************** -->
        <v-radio-group v-if="modal.exercise.type === 1" v-model="modal.exercise.answer[0]" hide-details>
            <p class="text-subtitle-2 my-2">正确选项</p>
            <div v-for="(option, index) in options" :key="'S' + option" class="d-flex mb-2">
                <v-radio :value="option" color="success" :disabled="!modal.exercise.option[index]" />
                <v-text-field
                    v-model="modal.exercise.option[index]"
                    variant="outlined"
                    color="primary"
                    density="compact"
                    hide-details
                    clearable
                    :rules="[(v:string) => !!v]"
                    :prefix="option + '.'"
                    :placeholder="'请输入' + option + '选项'"
                    persistent-placeholder
                    class="w-100" />
                <v-btn variant="text" color="red" :disabled="options.length <= 2" @click="deleteOptions(index)">
                    删除
                </v-btn>
            </div>
            <v-btn v-if="options.length < 26" variant="text" color="green" @click="addOptions"> 添加选项 </v-btn>
        </v-radio-group>

        <!-- ****************多选题****************** -->
        <div v-if="modal.exercise.type === 2">
            <p class="text-subtitle-2 my-2">正确选项</p>

            <div v-for="(option, index) in options" :key="'M' + option" class="d-flex mb-2">
                <v-checkbox
                    v-model="modal.exercise.answer"
                    :value="option"
                    color="success"
                    density="compact"
                    hide-details
                    :disabled="!modal.exercise.option[index]"
                    class="ml-2 mr-3" />
                <v-text-field
                    v-model="modal.exercise.option[index]"
                    variant="outlined"
                    color="primary"
                    density="compact"
                    hide-details
                    clearable
                    :rules="[(v:string) => !!v]"
                    :prefix="option + '.'"
                    :placeholder="'请输入' + option + '选项'"
                    persistent-placeholder
                    class="w-100" />
                <v-btn variant="text" color="red" :disabled="options.length <= 2" @click="deleteOptions(index)">
                    删除
                </v-btn>
            </div>
            <v-btn v-if="options.length < 26" variant="text" color="green" @click="addOptions" class="w-100">
                添加选项
            </v-btn>
        </div>

        <!-- ****************填空题****************** -->
        <div v-if="modal.exercise.type === 10">
            <p class="text-subtitle-2 mt-2">正确答案</p>
            <v-text-field
                v-model="modal.exercise.answer[0]"
                label="答案"
                variant="outlined"
                color="primary"
                density="compact"
                hide-details
                :rules="[(v:string) => !!v]"
                class="my-2" />
        </div>

        <v-divider />

        <p class="text-subtitle-2 mt-2">所属题目组（必须属于一个题目组）</p>
        <v-chip-group v-model="modal.exercise.tag" mandatory multiple selected-class="bg-green-darken-3">
            <v-chip v-for="item in current_user_tag" :key="item.tagid" :value="item.tagid">
                {{ item.tagname }}
            </v-chip>
        </v-chip-group>
        <v-btn variant="text" color="green" class="w-100" @click="$emit('add_tag', null)"> 添加题目组 </v-btn>
        <v-divider />

        <v-card-actions class="d-flex justify-end">
            <span v-if="is_upload_success" style="color: green"> 成功上传于{{ last_upload_success_time }} </span>
            <v-btn
                color="orange"
                text="完成创建"
                size="large"
                prepend-icon="mdi-check-circle"
                :disabled="!canSubmit"
                :loading="submit_loading"
                @click="onExerciseSubmit">
                完成{{ modal.exerciseid === undefined ? "创建" : "修改" }}</v-btn
            >
        </v-card-actions>

        <!-- 如果放到v-card外面就会有一些暂时不能理解的问题 -->
    </v-card>
</template>

<script lang="ts" setup name="ExerciseUpdater">
    import { watch, ref, computed, onMounted } from "vue"
    import emitter from "@/utils/emitter"
    import type { CreateExerciseResponse, NewExerciseItem, PublicTag } from "@/types"
    import { getNewExerciseModel } from "@/utils/exercise"
    import { callapi } from "@/utils/callapi"

    // 无法自动推断类型，只能通过默认值的形式处理
    let modal = defineModel({
        default: <NewExerciseItem>{
            exerciseid: undefined,
            exercise: getNewExerciseModel(),
        },
    })

    defineProps<{ limit_textarea: boolean; current_user_tag: PublicTag[] }>()
    defineEmits(["add_tag"])

    let options = ref(["A", "B"])

    onMounted(() => {
        if (modal.value.exercise.option.length <= 2) {
            options.value = ["A", "B"]
        } else {
            let newOptions = <string[]>[]
            for (let i = 0; i < modal.value.exercise.option.length; i++) {
                newOptions.push(String.fromCharCode(65 + i))
            }
            options.value = newOptions
        }
    })

    function addOptions() {
        if (options.value.length >= 26) {
            emitter.emit("normalerror", "不能超过26个选项")
        } else {
            options.value.push(String.fromCharCode(65 + options.value.length))
        }
    }

    function deleteOptions(index: number) {
        if (options.value.length <= 2) {
            emitter.emit("normalerror", "不能少于2个选项")
        } else {
            modal.value.exercise.option.splice(index, 1)
            const charactar = String.fromCharCode(65 + index)
            const answer_index = modal.value.exercise.answer.indexOf(charactar)
            if (answer_index != -1) {
                modal.value.exercise.answer.splice(answer_index, 1)
            }
            options.value.pop()
        }
    }

    watch(
        () => modal.value.exercise.type,
        (newValue, oldValue) => {
            if (oldValue === 0 || oldValue === 10 || newValue === 0 || newValue === 10) {
                options.value = ["A", "B"]
                modal.value.exercise.option = []
            }
            modal.value.exercise.answer = []
        }
    )

    let canSubmit = computed(() => {
        const premise =
            !!modal.value.exercise.title &&
            !!modal.value.exercise.content &&
            modal.value.exercise.answer.length > 0 &&
            modal.value.exercise.tag.length > 0
        if (modal.value.exercise.type === 1 || modal.value.exercise.type === 2) {
            let append = modal.value.exercise.option.length >= 2
            options.value.forEach((value) => {
                append = append && !!modal.value.exercise.option[value.charCodeAt(0) - 65]
            })
            return premise && append
        } else {
            return premise
        }
    })

    let submit_loading = ref(false)
    let is_upload_success = ref(false)
    let last_upload_success_time = ref("")

    function onExerciseSubmit() {
        submit_loading.value = true
        if (modal.value.exerciseid == undefined) {
            callapi.post(
                "json",
                "Exercise",
                "createExercise",
                modal.value.exercise,
                (data) => {
                    submit_loading.value = false
                    modal.value.exerciseid = (<CreateExerciseResponse>data).exerciseid
                    last_upload_success_time.value = new Date().toLocaleString()
                    is_upload_success.value = true
                },
                (errCode) => {
                    submit_loading.value = false
                    is_upload_success.value = false
                }
            )
        } else {
            callapi.post(
                "json",
                "Exercise",
                "updateExercise",
                {
                    exerciseid: modal.value.exerciseid,
                    newdata: modal.value.exercise,
                },
                (data) => {
                    submit_loading.value = false
                    last_upload_success_time.value = new Date().toLocaleString()
                    is_upload_success.value = true
                },
                (errCode) => {
                    submit_loading.value = false
                    is_upload_success.value = false
                }
            )
        }
    }
</script>

<style scoped></style>
