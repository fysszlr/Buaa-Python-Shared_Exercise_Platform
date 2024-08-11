<template>
    <v-container class="my-3">
        <v-card prepend-icon="mdi-account-circle" title="个人信息" max-width="600px" location="bottom">
            <v-divider />
            <v-row no-gutters class="my-10" align="center" justify="center">
                <v-col cols="4">
                    <v-row justify="center">
                        <v-avatar :image="userInfo.avatarurl" size="x-large" rounded="50" />
                    </v-row>
                    <v-row class="py-2" justify="center">
                        <v-col cols="8">
                            <v-divider />
                        </v-col>
                    </v-row>
                    <v-row justify="center" class="mb-2">
                        <div class="text-h5">{{ userInfo.username }}</div>
                    </v-row>
                    <v-row justify="center">
                        <v-btn
                            ref="change_avatar_button"
                            variant="text"
                            prepend-icon="mdi-pencil"
                            color="primary"
                            size="large">
                            修改头像
                        </v-btn>
                    </v-row>
                </v-col>
                <v-divider vertical />
                <v-col>
                    <v-list>
                        <v-list-item prepend-icon="mdi-account">
                            <v-list-item-title>
                                用户名
                                <span class="mx-1"></span>
                                {{ userInfo.username }}
                            </v-list-item-title>
                        </v-list-item>
                        <v-list-item prepend-icon="mdi-card-account-details">
                            <v-list-item-title>
                                学号
                                <span class="mx-1"></span>
                                {{ userInfo.studentid ? userInfo.studentid : "未填写" }}
                            </v-list-item-title>
                            <template v-slot:append>
                                <v-btn variant="text" color="primary" ref="change_studentid_button">修改学号</v-btn>
                            </template>
                        </v-list-item>
                    </v-list>
                </v-col>
            </v-row>
        </v-card>

        <v-card prepend-icon="mdi-certificate" title="能力信息" max-width="600px" class="mt-10" location="bottom">
            <v-divider />
            <div class="d-flex justify-center w-100">
                <v-chart
                    :option="evaluationChartOption"
                    style="max-width: 400px; height: 300px"
                    :tooltip-visible="false"
                    :legend-visibl="false" />
            </div>
        </v-card>

        <v-card prepend-icon="mdi-gift-open" title="题目推荐" max-width="600px" class="mt-10" location="bottom">
            <v-divider />
            <v-row class="mt-4 px-3">
                <v-col cols="7">
                    <v-text-field
                        v-model="recommendPattern"
                        label="推荐题目关键词"
                        prepend-inner-icon="mdi-magnify"
                        variant="outlined"
                        density="comfortable"
                        clearable />
                </v-col>
                <v-col cols="5">
                    <v-text-field
                        v-model="recommendQuantity"
                        label="数量"
                        variant="outlined"
                        density="comfortable"
                        type="number"
                        clearable>
                        <template #append>
                            <v-btn
                                style="background: linear-gradient(45deg, #1e90ff, #8a2be2); color: white"
                                size="large"
                                variant="flat"
                                :loading="submit_loading"
                                :disabled="
                                    recommendPattern == '' || recommendQuantity == '' || recommendQuantity == null
                                "
                                @click="recommend">
                                AI推荐
                            </v-btn>
                        </template>
                    </v-text-field>
                </v-col>
            </v-row>
        </v-card>
    </v-container>

    <ChangeAvatar :activator="change_avatar_button" />
    <ChangeStudentID :activator="change_studentid_button" />
</template>

<script lang="ts" setup name="UserCenter">
    import ChangeAvatar from "@/components/UserCenter/ChangeAvatar.vue"
    import ChangeStudentID from "@/components/UserCenter/ChangeStudentID.vue"
    import { useUserInfo } from "@/stores/userinfo"
    import type { GetCurrentEvaluationResponse, GetRecommendExerciseResponse } from "@/types"
    import { callapi } from "@/utils/callapi"
    import { onMounted, ref, watch } from "vue"
    import { use } from "echarts/core"
    import { CanvasRenderer } from "echarts/renderers"
    import { PieChart, BarChart, LineChart } from "echarts/charts"
    import { GridComponent } from "echarts/components"
    import { TitleComponent, TooltipComponent, LegendComponent } from "echarts/components"
    import VChart from "vue-echarts"
    import { useGlobalExerciseList } from "@/stores/globalexerciselist"
    import emitter from "@/utils/emitter"

    use([
        CanvasRenderer,
        PieChart,
        BarChart,
        LineChart,
        TitleComponent,
        TooltipComponent,
        GridComponent,
        LegendComponent,
    ])

    const userInfo = useUserInfo()
    const globalexerciselist = useGlobalExerciseList()

    let change_avatar_button = ref()
    let change_studentid_button = ref()

    let evaluationChartOption = ref({
        xAxis: {
            type: "category",
            data: <string[]>[],
        },
        yAxis: {
            type: "value",
        },
        series: [
            {
                name: "能力分数折线图",
                type: "line",
                data: <number[]>[],
            },
            {
                name: "能力分数柱状图",
                type: "bar",
                data: <number[]>[],
                showBackground: true,
                backgroundStyle: {
                    color: "rgba(180, 180, 180, 0.2)",
                },
            },
        ],
    })

    function getCurrentEvaluation() {
        callapi.get("Log", "getCurrentEvaluation", null, (data) => {
            const result = <GetCurrentEvaluationResponse>data
            evaluationChartOption.value.xAxis.data = result.time
            evaluationChartOption.value.series[0].data = result.score
            evaluationChartOption.value.series[1].data = result.score
        })
    }

    onMounted(() => {
        getCurrentEvaluation()
    })

    let recommendPattern = ref("")
    let recommendQuantity = ref()

    watch(recommendQuantity, (newValue) => {
        if (newValue <= 0) {
            recommendQuantity.value = 1
        }
    })

    let submit_loading = ref(false)

    function recommend() {
        submit_loading.value = true
        callapi.get(
            "Log",
            "getRecommendExercise",
            {
                pattern: recommendPattern.value,
                quantity: recommendQuantity.value,
            },
            (data) => {
                const result = <GetRecommendExerciseResponse>data
                globalexerciselist.reload(result.recommend)
                if (!result.statisfy) {
                    emitter.emit("normalerror", "因题目数量不足，未能满足推荐数量需求")
                }
                submit_loading.value = false
                window.open("/exercise")
            },
            (errCode) => {
                submit_loading.value = false
            }
        )
    }
</script>

<style scoped></style>
