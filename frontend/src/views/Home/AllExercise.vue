<template>
    <v-container fluid class="pa-6">
        <p class="text-h4 mt-6 mb-4">所有题目</p>
        <p class="text-subtitle-2 mb-4">点击查看详情、添加到题目组、修改题目</p>
        <p class="text-subtitle-2 mb-8">选择题目，进入练习</p>

        <v-row justify="center" class="px-2">
            <v-col cols="4">
                <v-text-field
                    v-model="searchID"
                    placeholder="搜索题目ID"
                    persistent-placeholder
                    label="题目ID"
                    prepend-inner-icon="mdi-magnify"
                    variant="outlined"
                    class="me-2"
                    type="number"
                    density="comfortable"
                    clearable>
                    <template #append>
                        <v-btn
                            color="secondary"
                            size="large"
                            variant="flat"
                            :disabled="searchID == '' || searchID == null"
                            @click="idSearch">
                            搜索
                        </v-btn>
                    </template>
                </v-text-field>
            </v-col>
            <v-col cols="8" class="d-flex">
                <v-select
                    variant="outlined"
                    class="me-2"
                    max-width="200px"
                    density="comfortable"
                    :items="searchTypeList"
                    item-value="type"
                    v-model="searchType">
                    <template #prepend> 根据 </template>
                </v-select>
                <v-text-field
                    v-model="searchString"
                    placeholder="请输入搜索关键词"
                    prepend-inner-icon="mdi-magnify"
                    variant="outlined"
                    class="me-2"
                    density="comfortable"
                    clearable>
                    <template #append>
                        <v-btn
                            color="primary"
                            size="large"
                            variant="flat"
                            :disabled="searchString == ''"
                            @click="stringSearch">
                            搜索
                        </v-btn>
                    </template>
                </v-text-field>
            </v-col>
        </v-row>

        <v-data-table
            :headers="headers"
            :items="reachableExercise"
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
                <v-btn
                    variant="tonal"
                    icon
                    density="comfortable"
                    color="primary"
                    class="me-1"
                    :disabled="reachableExerciseBlock"
                    @click="infoDialog(index)">
                    <v-icon size="default"> mdi-file-document </v-icon>
                </v-btn>

                <v-btn
                    v-if="item.createusername == userInfo.username"
                    variant="tonal"
                    icon
                    density="comfortable"
                    color="green"
                    class="me-1"
                    :disabled="reachableExerciseBlock"
                    @click="editDialog(index)">
                    <v-icon size="default"> mdi-pencil </v-icon>
                </v-btn>

                <v-btn
                    v-else
                    variant="tonal"
                    icon
                    density="comfortable"
                    color="secondary"
                    class="me-1"
                    :disabled="reachableExerciseBlock"
                    @click="addToTagDialog(item.exerciseid, item.title)">
                    <v-icon size="default"> mdi-tag-plus </v-icon>
                </v-btn>
            </template>

            <template v-slot:bottom>
                <div class="text-center mt-2">
                    <v-pagination v-model="nowPage" :length="reachablePages"></v-pagination>
                </div>
            </template>
        </v-data-table>
    </v-container>

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

    <AddExerciseToTag
        v-model="addToTagDialogActive"
        :current_user_tag="currentUserTag"
        :exerciseid="addToTagExerciseID"
        :title="addToTagExerciseTitle"
        @add_finish="getReachableExercise(nowPage)" />

    <AddTag v-model="addTagDialogActive" @add_finish="getReachableExercise(nowPage)" />

    <ExerciseInfo v-model="infoDialogActive" :exercise="infoDialogExercise" :showAnswer="false" />
</template>

<script lang="ts" setup name="AllExercise">
    import AddTag from "@/components/AddTag.vue"
    import AddExerciseToTag from "@/components/AllExercise/AddExerciseToTag.vue"
    import ExerciseInfo from "@/components/ExerciseInfo.vue"
    import ExerciseUpdater from "@/components/ExerciseUpdater.vue"
    import { useGlobalExerciseList } from "@/stores/globalexerciselist"
    import { useUserInfo } from "@/stores/userinfo"
    import type {
        PublicTag,
        GetCurrentUserTagResponse,
        GetExerciseByIDResponse,
        GetListExerciseResponse,
        GotExercise,
        NewExerciseItem,
    } from "@/types"
    import { callapi } from "@/utils/callapi"
    import { onMounted, ref, watch } from "vue"
    const userInfo = useUserInfo()
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

    let currentUserTag = ref(<PublicTag[]>[])

    function getCurrentUserTag() {
        callapi.get("Tag", "getCurrentUserTag", null, (data) => {
            currentUserTag.value = (<GetCurrentUserTagResponse>data).tag
        })
    }

    onMounted(() => {
        getCurrentUserTag()
    })

    let reachableExerciseGetType = 0
    let reachableExercise = ref(<GotExercise[]>[])
    let reachableExerciseBlock = ref(false)
    let reachablePages = ref(1)
    let nowPage = ref(1)
    let table_loading = ref(false)

    function getReachableExercise(page: number) {
        table_loading.value = true
        reachableExercise.value = <GotExercise[]>[]
        switch (reachableExerciseGetType) {
            case 0:
                callapi.get(
                    "Exercise",
                    "getReachableExercise",
                    {
                        page: page,
                    },
                    (data) => {
                        const result = <GetListExerciseResponse>data
                        reachablePages.value = result.pages
                        reachableExerciseBlock.value = false
                        reachableExercise.value = result.thispage
                        table_loading.value = false
                    },
                    (errCode) => {
                        table_loading.value = false
                    }
                )
                break
            case 1:
            case 2:
                callapi.get(
                    "Exercise",
                    "searchExercise",
                    {
                        page: page,
                        type: reachableExerciseGetType === 1 ? "title" : "tag",
                        pattern: searchString.value,
                    },
                    (data) => {
                        const result = <GetListExerciseResponse>data
                        reachablePages.value = result.pages
                        reachableExerciseBlock.value = false
                        reachableExercise.value = result.thispage
                        table_loading.value = false
                    },
                    (errCode) => {
                        table_loading.value = false
                    }
                )
                break
            case 3:
                callapi.get(
                    "Exercise",
                    "getExerciseByID",
                    {
                        exerciseid: searchID.value,
                    },
                    (data) => {
                        const result = <GetExerciseByIDResponse>data
                        reachableExercise.value[0] = result.data
                        reachableExerciseBlock.value = result.isBlock
                        reachablePages.value = 1
                        table_loading.value = false
                    },
                    (errCode) => {
                        table_loading.value = false
                    }
                )
        }
    }

    onMounted(() => {
        getReachableExercise(1)
    })

    watch(nowPage, (newValue) => {
        getReachableExercise(newValue)
    })

    let editDialogActive = ref(false)
    let editExerciseIndex = ref(0)
    let editExercise = ref(<NewExerciseItem>{})

    function editDialog(index: number) {
        editExerciseIndex.value = index
        editExercise.value = {
            exerciseid: reachableExercise.value[index].exerciseid,
            exercise: {
                type: reachableExercise.value[index].type,
                title: reachableExercise.value[index].title,
                content: reachableExercise.value[index].content,
                option: reachableExercise.value[index].option,
                answer: reachableExercise.value[index].answer,
                tag: reachableExercise.value[index].tag.map((value) => value.tagid),
            },
        }
        editDialogActive.value = true
    }

    watch(editDialogActive, (newValue, oldValue) => {
        if (oldValue && !newValue) {
            getReachableExercise(nowPage.value)
        }
    })

    let addTagDialogActive = ref(false)

    let addToTagDialogActive = ref(false)
    let addToTagExerciseID = ref(-1)
    let addToTagExerciseTitle = ref("")

    function addToTagDialog(exerciseid: number, title: string) {
        addToTagExerciseID.value = exerciseid
        addToTagExerciseTitle.value = title
        addToTagDialogActive.value = true
    }

    let infoDialogActive = ref(false)
    let infoDialogExercise = ref(<GotExercise>{})

    function infoDialog(index: number) {
        infoDialogExercise.value = reachableExercise.value[index]
        infoDialogActive.value = true
    }

    const searchTypeList = [
        {
            title: "题目组",
            type: "tag",
        },
        {
            title: "标题",
            type: "title",
        },
    ]

    let searchType = ref("tag")
    let searchString = ref("")
    let searchID = ref(null)

    function stringSearch() {
        if (searchType.value == "title") {
            reachableExerciseGetType = 1
        } else {
            reachableExerciseGetType = 2
        }
        getReachableExercise(1)
    }

    watch(searchString, (newValue) => {
        if (newValue == "" || newValue == null) {
            reachableExerciseGetType = 0
            getReachableExercise(1)
        }
    })

    function idSearch() {
        reachableExerciseGetType = 3
        getReachableExercise(1)
    }

    watch(searchID, (newValue) => {
        if (newValue == "" || newValue == null) {
            reachableExerciseGetType = 0
            getReachableExercise(1)
        }
    })

    let selectedExercise = ref(<number[]>[])

    function doSelectedExercise() {
        globalexerciselist.reload(selectedExercise.value)
        window.open("/exercise")
    }
</script>

<style scoped></style>
