<template>
    <p class="text-h4 mt-6 mb-4">共享群组详情：{{ groupname }}</p>
    <p class="text-subtitle-2 mb-4">共享群组ID：{{ groupid }}</p>
    <p class="text-subtitle-2 mb-6">
        创建者：
        <v-avatar :image="createavatarurl" size="small" rounded="50" />
        {{ createusername }}
    </p>
    <p class="text-h6 mb-4">共享群组中的题目组：</p>

    <v-container fluid class="d-flex fill-height">
        <v-card v-for="tag in tagFromGroup" width="23%" class="my-3 me-3">
            <v-card-title>{{ tag.tagname }}</v-card-title>
            <v-card-text>
                创建者：
                <v-avatar :image="tag.createavatarurl" size="small" rounded="50" />
                {{ tag.createusername }}
            </v-card-text>
            <v-card-actions>
                <v-btn color="blue-lighten-2" block variant="tonal" @click="goTo(tag.tagid)">进入题目组</v-btn>
            </v-card-actions>
        </v-card>
    </v-container>

    <v-fab
        color="primary"
        prepend-icon="mdi-share"
        location="top end"
        size="x-large"
        position="sticky"
        text="共享题目组"
        extended
        app
        @click="addTagToGroupDialogActive = true"
        class="mt-4" />

    <AddTagToGroup
        v-model="addTagToGroupDialogActive"
        :current_user_tag="currentUserTag"
        :groupid="parseInt(groupid)"
        @add_finish="getTagFromGroup(parseInt(groupid))" />
</template>

<script lang="ts" setup name="GroupDetail">
    import AddTagToGroup from "@/components/GroupView/AddTagToGroup.vue"
    import router from "@/router"
    import type { FullTag, GetCurrentUserTagResponse, GetTagFromGroupResponse, GotGroup, PublicTag } from "@/types"
    import { callapi } from "@/utils/callapi"
    import { onMounted, ref, watch } from "vue"
    import { onBeforeRouteUpdate } from "vue-router"

    const props = defineProps<{ groupid: string }>()

    let groupname = ref("")
    let createusername = ref("")
    let createavatarurl = ref("")

    function getGroupInfo(groupid: number) {
        callapi.get(
            "Group",
            "getGroupInfoByID",
            {
                groupid: groupid,
            },
            (data) => {
                const result = <GotGroup>data
                groupname.value = result.groupname
                createusername.value = result.createusername
                createavatarurl.value = result.createavatarurl
            }
        )
    }

    let tagFromGroup = ref(<FullTag[]>[])

    function getTagFromGroup(groupid: number) {
        callapi.get(
            "Group",
            "getTagFromGroup",
            {
                groupid: groupid,
            },
            (data) => {
                tagFromGroup.value = (<GetTagFromGroupResponse>data).tag
            }
        )
    }

    let currentUserTag = ref(<PublicTag[]>[])

    function getCurrentUserTag() {
        callapi.get("Tag", "getCurrentUserTag", null, (data) => {
            currentUserTag.value = (<GetCurrentUserTagResponse>data).tag
        })
    }

    onMounted(() => {
        getGroupInfo(parseInt(props.groupid))
        getTagFromGroup(parseInt(props.groupid))
    })

    onBeforeRouteUpdate((to) => {
        getGroupInfo(parseInt(<string>to.params.groupid))
        getTagFromGroup(parseInt(<string>to.params.groupid))
    })

    function goTo(tagid: number) {
        router.push({
            name: "tagDetail",
            params: {
                groupid: props.groupid,
                tagid: tagid,
            },
        })
    }

    let addTagToGroupDialogActive = ref(false)

    watch(addTagToGroupDialogActive, (newValue, oldValue) => {
        if (newValue && !oldValue) {
            getCurrentUserTag()
        }
    })
</script>

<style scoped></style>
