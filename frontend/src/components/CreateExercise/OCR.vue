<template>
    <v-card elevation="4" class="pa-4">
        <v-file-input
            v-model="OCR_file"
            :rules="[(v) => !!v.length || '请选择文件']"
            accept="image/*,.pdf"
            label="请选择文件以进行OCR"
            variant="outlined"
            clearable>
            <template #append>
                <v-btn
                    color="primary"
                    :disabled="OCR_file == null"
                    :loading="submit_loading"
                    @click="onOCRClick"
                    variant="text"
                    size="large">
                    上传
                </v-btn>
            </template>
        </v-file-input>

        <v-text-field v-model="OCR_page" density="comfortable" variant="underlined" type="number" label="请输入页码">
            <template #prepend> （仅PDF文件有效）需要识别的页码： </template>
        </v-text-field>

        <v-textarea
            v-model="OCR_result"
            auto-grow
            no-resize
            variant="outlined"
            color="primary"
            bg-color="grey-lighten-3"
            placeholder="OCR结果将显示在这里"
            hide-details />
    </v-card>
</template>

<script lang="ts" setup name="OCR">
    import type { OCRResponse } from "@/types"
    import { callapi } from "@/utils/callapi"
    import emitter from "@/utils/emitter"
    import { ref, watch } from "vue"

    let OCR_file = ref(null)
    let OCR_result = ref("")
    let OCR_page = ref(1)
    let submit_loading = ref(false)

    watch(OCR_page, (newValue) => {
        if (newValue <= 0) {
            OCR_page.value = 1
        }
    })

    function onOCRClick() {
        submit_loading.value = true
        callapi.post(
            "form-data",
            "Exercise",
            "OCR",
            {
                file: OCR_file.value,
                page: OCR_page.value,
            },
            (data) => {
                OCR_result.value = (<OCRResponse>data).text
                emitter.emit("success_snackbar", "OCR识别成功")
                submit_loading.value = false
            },
            (errCode) => {
                submit_loading.value = false
            }
        )
    }
</script>
