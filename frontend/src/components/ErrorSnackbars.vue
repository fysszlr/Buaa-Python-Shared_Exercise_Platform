<template>
    <v-snackbar v-model="snackbar" :color="color" :timeout="hold ? -1 : 5000">
        {{ text }}
        <template v-slot:actions>
            <v-btn variant="text" @click="snackbar = false" v-if="!hold"> 关闭 </v-btn>
        </template>
    </v-snackbar>
</template>

<script lang="ts" setup name="ErrorSnackbars">
    import { ref } from "vue"
    import emitter from "@/utils/emitter"

    let snackbar = ref(false)
    let text = ref("")
    let hold = ref(false)
    let color = ref("red")

    emitter.on("apierror", (message) => {
        text.value = <string>message ? <string>message : "未知错误"
        hold.value = false
        color.value = "red"
        snackbar.value = true
    })

    emitter.on("fatalerror", (message) => {
        text.value = <string>message ? <string>message : "未知错误"
        hold.value = true
        color.value = "red"
        snackbar.value = true
    })

    emitter.on("normalerror", (message) => {
        text.value = <string>message ? <string>message : "未知错误"
        hold.value = false
        color.value = "orange-darken-3"
        snackbar.value = true
    })
</script>
