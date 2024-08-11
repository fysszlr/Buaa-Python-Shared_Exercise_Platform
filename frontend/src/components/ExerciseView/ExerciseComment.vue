<template>
    <v-card elevation="2" min-width="800px" max-width="800px" class="px-4 pb-0">
        <v-card-title class="mb-2">讨论区（{{ comment.length }}）</v-card-title>

        <v-textarea
            v-model="newComment"
            auto-grow
            no-resize
            variant="outlined"
            color="primary"
            :placeholder="'以' + userInfo.username + '的身份创建新的讨论'"
            hide-details
            :disabled="submit_loading"
            class="mb-2">
        </v-textarea>

        <v-btn
            color="primary"
            :disabled="newComment == ''"
            :loading="submit_loading"
            @click="onNewCommentClick"
            size="large"
            class="w-100">
            创建新讨论
        </v-btn>

        <v-list lines="three">
            <v-list-item v-for="item in comment" :subtitle="item.time" :title="item.createusername">
                <template v-slot:prepend>
                    <v-avatar :image="item.createavatarurl" size="small" rounded="50" />
                </template>

                <pre>{{ item.content }}</pre>
            </v-list-item>
        </v-list>
    </v-card>
</template>

<script lang="ts" setup name="ExerciseComment">
    import { useUserInfo } from "@/stores/userinfo"
    import type { GotComment } from "@/types"
    import { callapi } from "@/utils/callapi"
    import emitter from "@/utils/emitter"
    import { ref } from "vue"
    const userInfo = useUserInfo()

    const props = defineProps<{ exerciseid: number; comment: GotComment[] }>()
    const emit = defineEmits(["refresh"])

    let newComment = ref("")

    let submit_loading = ref(false)

    function onNewCommentClick() {
        submit_loading.value = true
        callapi.post(
            "form-data",
            "Exercise",
            "addComment",
            {
                exerciseid: props.exerciseid,
                comment: newComment.value,
            },
            (data) => {
                emit("refresh")
                emitter.emit("success_snackbar", "添加讨论区成功")
                newComment.value = ""
                submit_loading.value = false
            }
        )
    }
</script>

<style scoped>
    pre {
        white-space: pre-wrap;
    }
</style>
