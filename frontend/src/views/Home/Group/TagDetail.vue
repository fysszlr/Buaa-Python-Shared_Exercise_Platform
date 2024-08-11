<template>
    <p class="text-h4 mt-6 mb-4">题目组详情：{{ tagname }}</p>
    <p class="text-subtitle-2 mb-6">
        创建者：
        <v-avatar :image="createavatarurl" size="small" rounded="50" />
        {{ createusername }}
    </p>
    <p class="text-h6 mb-4">题目组中的所有题目：</p>
    <p class="text-subtitle-2 mb-4">选择题目，进入练习</p>

    <v-data-table
        :headers="headers"
        :items="exerciseFromTag"
        item-value="exerciseid"
        :loading="table_loading"
        disable-sort
        sticky
        items-per-page="20"
        show-select
        no-data-text="无题目"
        loading-text="加载中"
        v-model="selectedExercise">
        <template v-slot:item.title="{ item }">
            <p class="text-break">{{ item.title }}</p>
        </template>

        <template v-slot:item.type="{ item }">
            {{ exerciseType[item.type] }}
        </template>

        <template v-slot:item.tag="{ item }">
            <v-chip v-for="tag in item.tag" :key="tag.tagid" color="secondary" label class="me-1">{{
                tag.tagname
            }}</v-chip>
        </template>

        <template v-slot:item.actions="{ item, index }">
            <v-btn variant="tonal" icon density="comfortable" color="primary" class="me-1" @click="infoDialog(index)">
                <v-icon size="default"> mdi-file-document </v-icon>
            </v-btn>
        </template>

        <template v-slot:bottom>
            <div class="text-center mt-2">
                <v-pagination v-model="nowPage" :length="exercisePages"></v-pagination>
            </div>
        </template>
    </v-data-table>

    <v-fab
        color="green"
        prepend-icon="mdi-share"
        location="top end"
        size="x-large"
        position="sticky"
        text="练习所选题目"
        extended
        app
        :disabled="selectedExercise.length == 0"
        @click="doSelectedExercise"
        class="mt-4" />

    <ExerciseInfo v-model="infoDialogActive" :exercise="infoDialogExercise" :showAnswer="false" />
</template>

<script lang="ts" setup name="TagDetail">
    import ExerciseInfo from "@/components/ExerciseInfo.vue"
    import { useGlobalExerciseList } from "@/stores/globalexerciselist"
    import type { FullTag, GetListExerciseResponse, GotExercise } from "@/types"
    import { callapi } from "@/utils/callapi"
    import { onMounted, ref } from "vue"
    import { onBeforeRouteUpdate } from "vue-router"
    const globalexerciselist = useGlobalExerciseList()

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

    const props = defineProps<{ groupid: string; tagid: string }>()

    let tagname = ref("")
    let createusername = ref("")
    let createavatarurl = ref("")

    function getTagInfo(tagid: number) {
        callapi.get(
            "Tag",
            "getTagInfoByID",
            {
                tagid: tagid,
            },
            (data) => {
                const result = <FullTag>data
                tagname.value = result.tagname
                createusername.value = result.createusername
                createavatarurl.value = result.createavatarurl
            }
        )
    }

    let exerciseFromTag = ref(<GotExercise[]>[])
    let exercisePages = ref(0)
    let nowPage = ref(1)
    let table_loading = ref(false)

    function getExerciseFromTag(tagid: number, page: number) {
        table_loading.value = true
        exerciseFromTag.value = <GotExercise[]>[]
        callapi.get(
            "Tag",
            "getExerciseFromTag",
            {
                tagid: tagid,
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

    onMounted(() => {
        getTagInfo(parseInt(props.tagid))
        getExerciseFromTag(parseInt(props.tagid), 1)
    })

    onBeforeRouteUpdate((to) => {
        getTagInfo(parseInt(<string>to.params.tagid))
        getExerciseFromTag(parseInt(<string>to.params.tagid), 1)
    })

    let selectedExercise = ref(<number[]>[])

    function doSelectedExercise() {
        globalexerciselist.reload(selectedExercise.value)
        window.open("/exercise")
    }

    let infoDialogActive = ref(false)
    let infoDialogExercise = ref(<GotExercise>{})

    function infoDialog(index: number) {
        infoDialogExercise.value = exerciseFromTag.value[index]
        infoDialogActive.value = true
    }
</script>

<style scoped></style>
