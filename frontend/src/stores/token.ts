import { defineStore } from "pinia"

export const useToken = defineStore("token", {
    state: () => {
        return {
            type: "init",
            token: "0",
        }
    },
    actions: {
        setUser(token: string) {
            this.type = "user"
            this.token = token
        },
        setAdmin(token: string) {
            this.type = "admin"
            this.token = token
        },
        clear() {
            this.type = "init"
            this.token = "0"
        },
    },
    getters: {
        isInit(): boolean {
            return this.type == "init"
        },
        isUser(): boolean {
            return this.type == "user"
        },
        isAdmin(): boolean {
            return this.type == "admin"
        },
    },
    persist: true,
})
