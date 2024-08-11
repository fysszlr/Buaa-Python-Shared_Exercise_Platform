<template>
    <v-container fluid class="pa-6">
        <p class="text-h4 mt-6 mb-4">我的题目</p>
        <p class="text-subtitle-2 mb-4">点击题目组，查看题目</p>

        <v-chip-group v-model="seletedTagId" mandatory selected-class="bg-green-darken-3">
            <v-chip v-for="item in currentUserTag" :key="item.tagid" :value="item.tagid">
                {{ item.tagname }}
            </v-chip>
        </v-chip-group>

        <v-data-table
            :headers="headers"
            :items="exerciseFromTag"
            item-value="exerciseid"
            :loading="table_loading"
            disable-sort
            sticky
            items-per-page="20"
            no-data-text="未选择题目组或无题目"
            loading-text="加载中">
            <template v-slot:item.title="{ item }">
                <p class="text-break">{{ item.title }}</p>
            </template>

            <template v-slot:item.type="{ item }">
                {{ exerciseType[item.type] }}
            </template>

            <template v-slot:bottom>
                <div class="text-center mt-2">
                    <v-pagination v-model="nowPage" :length="exercisePages"></v-pagination>
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
                    color="green"
                    class="me-1"
                    :disabled="item.createusername != userInfo.username"
                    @click="editDialog(index)">
                    <v-icon size="default"> mdi-pencil </v-icon>
                </v-btn>
            </template>
        </v-data-table>
    </v-container>

    <v-fab
        color="primary"
        prepend-icon="mdi-plus"
        location="top end"
        size="x-large"
        position="sticky"
        text="添加题目组"
        extended
        app
        @click="addTagDialogActive = true"
        class="mt-4" />

    <v-dialog max-width="500px" v-model="editDialogActive">
        <v-toolbar>
            <v-btn icon="mdi-close" @click="editDialogActive = false" />
            <v-toolbar-title>编辑题目</v-toolbar-title>
        </v-toolbar>

        <ExerciseUpdater
            v-model="editExercise"
            :limit_textarea="true"
            :current_user_tag="currentUserTag"
            @add_tag="addTagDialogActive = true" />
    </v-dialog>

    <AddTag v-model="addTagDialogActive" @add_finish="getCurrentUserTag" />
</template>

<script lang="ts" setup name="MyExercise">
    import AddTag from "@/components/AddTag.vue"
    import ExerciseUpdater from "@/components/ExerciseUpdater.vue"
    import type {
        PublicTag,
        GetCurrentUserTagResponse,
        GetListExerciseResponse,
        GotExercise,
        NewExerciseItem,
    } from "@/types"
    import { callapi } from "@/utils/callapi"
    import { onMounted, ref, watch } from "vue"
    import { useUserInfo } from "@/stores/userinfo"
    const userInfo = useUserInfo()

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

    let currentUserTag = ref(<PublicTag[]>[])

    function getCurrentUserTag() {
        callapi.get("Tag", "getCurrentUserTag", null, (data) => {
            currentUserTag.value = (<GetCurrentUserTagResponse>data).tag
        })
    }

    onMounted(() => {
        getCurrentUserTag()
    })

    let seletedTagId = ref()
    let exerciseFromTag = ref(<GotExercise[]>[])
    let exercisePages = ref(0)
    let nowPage = ref(1)
    let table_loading = ref(false)

    function getExerciseFromTag(page: number) {
        table_loading.value = true
        exerciseFromTag.value = <GotExercise[]>[]
        callapi.get(
            "Tag",
            "getExerciseFromTag",
            {
                tagid: seletedTagId.value,
                page: page,
            },
            (data) => {
                const result = <GetListExerciseResponse>data
                exercisePages.value = result.pages
                exerciseFromTag.value = result.thispage
                table_loading.value = false
            },
            (errCode) => {
                table_loading.value = false
            }
        )
    }

    watch(nowPage, (newValue) => {
        getExerciseFromTag(newValue)
    })

    watch(seletedTagId, (newValue) => {
        getExerciseFromTag(1)
    })

    let editDialogActive = ref(false)
    let editExerciseIndex = ref(0)
    let editExercise = ref(<NewExerciseItem>{})

    function editDialog(index: number) {
        editExerciseIndex.value = index
        editExercise.value = {
            exerciseid: exerciseFromTag.value[index].exerciseid,
            exercise: {
                type: exerciseFromTag.value[index].type,
                title: exerciseFromTag.value[index].title,
                content: exerciseFromTag.value[index].content,
                option: exerciseFromTag.value[index].option,
                answer: exerciseFromTag.value[index].answer,
                tag: exerciseFromTag.value[index].tag.map((value) => value.tagid),
            },
        }
        editDialogActive.value = true
    }

    watch(editDialogActive, (newValue, oldValue) => {
        if (oldValue && !newValue) {
            getExerciseFromTag(nowPage.value)
        }
    })

    let addTagDialogActive = ref(false)
</script>

<style scoped></style>
