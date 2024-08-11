<template>
    <v-snackbar v-model="snackbar" color="green">
        {{ text }}
        <template v-slot:actions>
            <v-btn color="white" variant="text" @click="snackbar = false"> 关闭 </v-btn>
        </template>
    </v-snackbar>
</template>

<script lang="ts" setup name="SuccessSnackbars">
    import { ref } from "vue"
    import emitter from "@/utils/emitter"

    let snackbar = ref(false)
    let text = ref("")

    emitter.on("success_snackbar", (message) => {
        text.value = <string>message
        snackbar.value = true
    })
</script>
