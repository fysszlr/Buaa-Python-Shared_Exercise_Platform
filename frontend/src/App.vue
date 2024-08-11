<template>
    <v-app theme="light">
        <RouterView />
    </v-app>
    <ErrorSnackbars />
    <SuccessSnackbars />
</template>

<script setup lang="ts" name="App">
    import { RouterView } from "vue-router"
    import ErrorSnackbars from "./components/ErrorSnackbars.vue"
    import SuccessSnackbars from "./components/SuccessSnackbars.vue"
</script>

<style scoped></style>
