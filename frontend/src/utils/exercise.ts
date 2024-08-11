import type { NewExercise, NewExerciseItem } from "@/types"

export function getNewExerciseModel(): NewExercise {
    return {
        type: 0,
        title: "",
        content: "",
        option: [],
        answer: [],
        tag: [],
    }
}
