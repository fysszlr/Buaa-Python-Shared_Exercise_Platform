<template>
    <v-container fluid class="pa-6">
        <p class="text-h4 mt-6 mb-4">题目管理</p>
        <p class="text-subtitle-2 mb-4">封禁、解封题目</p>

        <v-data-table
            :headers="headers"
            :items="allExercise"
            item-value="exerciseid"
            disable-sort
            sticky
            items-per-page="20">
            <template v-slot:item.title="{ item }">
                <p class="text-break">{{ item.title }}</p>
            </template>

            <template v-slot:item.type="{ item }">
                {{ exerciseType[item.type] }}
            </template>

            <template v-slot:bottom>
                <div class="text-center mt-2">
                    <v-pagination v-model="nowPage" :length="allPages"></v-pagination>
                </div>
            </template>

            <template v-slot:item.tag="{ item }">
                <v-chip v-for="tag in item.tag" :key="tag.tagid" color="secondary" label class="me-1">{{
                    tag.tagname
                }}</v-chip>
            </template>

            <template v-slot:item.actions="{ item, index }">
                <v-btn
                    variant="tonal"
                    icon
                    density="comfortable"
                    color="primary"
                    class="me-1"
                    @click="infoDialog(index)">
                    <v-icon size="default"> mdi-file-document </v-icon>
                </v-btn>

                <v-btn
                    v-if="item.isBlock"
                    variant="tonal"
                    icon
                    density="comfortable"
                    color="green"
                    class="me-1"
                    @click="dialog(true, item.title, item.exerciseid)">
                    <v-icon size="default"> mdi-undo-variant </v-icon>
                </v-btn>
                <v-btn
                    v-else
                    variant="tonal"
                    icon
                    density="comfortable"
                    color="red"
                    class="me-1"
                    @click="dialog(false, item.title, item.exerciseid)">
                    <v-icon size="default"> mdi-cancel </v-icon>
                </v-btn>
            </template>
        </v-data-table>
    </v-container>

    <v-dialog max-width="500px" v-model="dialogActive">
        <v-card>
            <v-toolbar>
                <v-btn icon="mdi-close" @click="dialogActive = false" />
                <v-toolbar-title>{{ dialogType ? "解封" : "封禁" }}题目</v-toolbar-title>
            </v-toolbar>

            <v-card-item>
                确定要{{ dialogType ? "解封" : "封禁" }}题目ID为{{ dialogExerciseID }}的题目“{{
                    dialogExerciseTitle
                }}”？
            </v-card-item>

            <template v-slot:actions>
                <v-btn @click="dialogActive = false">取消</v-btn>
                <v-btn :color="dialogType ? 'green' : 'red'" :loading="submit_loading" @click="onBlockUnblockClick">
                    {{ dialogType ? "解封" : "封禁" }}
                </v-btn>
            </template>
        </v-card>
    </v-dialog>

    <ExerciseInfo v-model="infoDialogActive" :exercise="infoDialogExercise" :showAnswer="true" />
</template>

<script lang="ts" setup name="ExerciseManagement">
    import ExerciseInfo from "@/components/ExerciseInfo.vue"
    import type { AdminExercise, GetAllExerciseResponse } from "@/types"
    import { callapi } from "@/utils/callapi"
    import emitter from "@/utils/emitter"
    import { onMounted, ref, watch } from "vue"

    const exerciseType = {
        0: "判断题",
        1: "单选题",
        2: "多选题",
        10: "填空题",
    }

    const headers = [
        { title: "ID", value: "exerciseid", width: "70px", minWidth: "70px" },
        { title: "创建者", key: "createusername" },
        { title: "类型", key: "type", width: "75px", minWidth: "75px" },
        { title: "标题", key: "title", maxWidth: "450px" },
        { title: "题目组", key: "tag", maxWidth: "350px" },
        { title: "操作", key: "actions", sortable: false },
    ]

    let allExercise = ref(<AdminExercise[]>[])
    let allPages = ref(1)
    let nowPage = ref(1)

    function getAllExercise(page: number) {
        allExercise.value = <AdminExercise[]>[]
        callapi.get(
            "Admin",
            "getAllExercise",
            {
                page: page,
            },
            (data) => {
                const result = <GetAllExerciseResponse>data
                allPages.value = result.pages
                allExercise.value = result.thispage
            }
        )
    }

    onMounted(() => {
        getAllExercise(1)
    })

    watch(nowPage, (newValue) => {
        getAllExercise(newValue)
    })

    let dialogActive = ref(false)
    let dialogType = ref(false)
    let dialogExerciseTitle = ref("")
    let dialogExerciseID = ref(0)

    function dialog(isunblock: boolean, username: string, userid: number) {
        dialogType.value = isunblock
        dialogExerciseTitle.value = username
        dialogExerciseID.value = userid
        dialogActive.value = true
    }

    let submit_loading = ref(false)

    function onBlockUnblockClick() {
        submit_loading.value = true
        callapi.post(
            "form-data",
            "Admin",
            dialogType.value ? "unblockExercise" : "blockExercise",
            {
                exerciseid: dialogExerciseID.value,
            },
            (data) => {
                emitter.emit(
                    "success_snackbar",
                    (dialogType.value ? "解封" : "封禁") + dialogExerciseTitle.value + "成功"
                )
                submit_loading.value = false
                dialogActive.value = false
            },
            (errCode) => {
                submit_loading.value = false
            }
        )
    }

    watch(dialogActive, (newValue, oldValue) => {
        if (oldValue && !newValue) {
            getAllExercise(nowPage.value)
        }
    })

    let infoDialogActive = ref(false)
    let infoDialogExercise = ref(<AdminExercise>{})

    function infoDialog(index: number) {
        infoDialogExercise.value = allExercise.value[index]
        infoDialogActive.value = true
    }
</script>

<style scoped></style>
