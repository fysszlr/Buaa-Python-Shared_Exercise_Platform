import { defineStore } from "pinia"

export const useGlobalExerciseList = defineStore("globalexerciselist", {
    state: () => {
        return {
            list: <number[]>[],
        }
    },
    actions: {
        reload(newlist: number[]) {
            this.list = newlist
        },
    },
    getters: {
        length(): number {
            return this.list.length
        },
    },
    persist: true,
})
