import axios from "axios"
import { useToken } from "@/stores/token"
import emitter from "./emitter"
import router from "@/router"

const __PRODUCE_ENV = false

const baseURL = "/api/v1"

interface errDescription {
    [key: number]: string
}

const errDescription: errDescription = {
    99999: "未知错误",
    99991: "登录信息失效，请重新登录",
    100101: "账号或密码错误",
    100102: "该账号已被封禁",
    100201: "该用户名已被占用",
    100202: "用户名或密码中包含非法字符",
    100301: "账号或密码错误",
    200201: "请求封禁的普通用户不存在",
    200301: "请求解封的普通用户不存在",
    200501: "请求封禁的题目不存在",
    200601: "请求解封的题目不存在",
    200801: "该管理员用户名已被占用",
    200802: "该管理员用户名或密码中包含非法字符",
    200901: "请求删除的管理员用户不存在",
    200902: "请求删除的管理员用户为超级管理员root",
    300201: "新头像超出服务器限制",
    300301: "新学号中包含非法字符",
    400101: "题目类型不受支持",
    400102: "请求添加到的题目组不存在",
    400103: "标题中包含非法字符或合规审查失败",
    400104: "正文中包含非法字符或合规审查失败",
    400105: "选项中包含非法字符或合规审查失败",
    400106: "答案中包含非法字符或合规审查失败（仅填空题）",
    400201: "当前用户无法管理该题目",
    400202: "题目类型不受支持",
    400203: "请求添加的题目组不存在",
    400204: "标题中包含非法字符或合规审查失败",
    400205: "正文中包含非法字符或合规审查失败",
    400206: "选项中包含非法字符或合规审查失败",
    400207: "答案中包含非法字符或合规审查失败（仅填空题）",
    400401: "无此ID对应的题目",
    400601: "已弃用",
    400602: "本地OCR服务错误",
    400801: "无此ID对应的题目",
    500101: "请求创建的题目组名称已被占用",
    500201: "题目组不存在或当前用户无法管理该题目组",
    500202: "请求加入到题目组的题目不存在",
    500301: "无此ID对应的题目组",
    500401: "无此ID对应的题目组",
    600201: "删除的共享群组不存在",
    600202: "当前用户无法管理该共享群组",
    600301: "加入的共享群组不存在",
    600401: "退出的共享群组不存在",
    600402: "请求退出的共享群组为公共共享区",
    600403: "请求退出的共享群组为自己创建的共享群组",
    600501: "题目组不存在或当前用户无法管理该题目组",
    600502: "请求加入到共享群组不存在",
    600601: "无此ID对应的共享群组",
    600701: "无此ID对应的共享群组",
    700101: "记录做错的题目不存在",
    700201: "记录做对的题目不存在",
    700401: "完成题目过少，无法推荐",
}

interface APIResponse {
    success: boolean
    errCode: number
    data: object
}

const callapi = {
    get: async function (
        module: string,
        method: string,
        params?: object | null,
        success?: (data: object) => any,
        error?: (errCode: number) => any
    ) {
        const token = useToken()
        const url = "/" + module + "/" + method + (__PRODUCE_ENV ? "/" : "")
        axios({
            method: "get",
            baseURL: baseURL,
            url: url,
            params: {
                token: token.token,
                ...params,
            },
            responseType: "json",
            responseEncoding: "utf8",
        })
            .then((response) => {
                const isAPIResponse = (data: any): data is APIResponse => {
                    return (
                        typeof data.success == "boolean" &&
                        typeof data.errCode == "number" &&
                        typeof data.data == "object"
                    )
                }
                if (response.status == 200 && isAPIResponse(response.data)) {
                    const result = <APIResponse>response.data
                    if (result.success) {
                        if (success != undefined) {
                            success(result.data)
                        }
                    } else {
                        emitter.emit("apierror", errDescription[result.errCode])
                        if (result.errCode == 99991) {
                            token.clear()
                            router.replace({ name: "login" })
                        } else if (error != undefined) {
                            error(result.errCode)
                        }
                    }
                } else {
                    emitter.emit("fatalerror", "网络错误：返回类型错误。请手动刷新页面")
                }
            })
            .catch((error) => {
                console.log(error)
                emitter.emit("fatalerror", "网络错误：" + error.code + "。请手动刷新页面")
            })
    },

    post: async function (
        type: "form-data" | "json",
        module: string,
        method: string,
        body?: object | null,
        success?: (data: object) => any,
        error?: (errCode: number) => any
    ) {
        const token = useToken()
        const url = "/" + module + "/" + method + (__PRODUCE_ENV ? "/" : "")
        axios({
            method: "post",
            baseURL: baseURL,
            url: url,
            headers: {
                "Content-Type": type == "form-data" ? "multipart/form-data" : "application/json",
            },
            params: {
                token: token.token,
            },
            data: body,
            responseType: "json",
            responseEncoding: "utf8",
        })
            .then((response) => {
                const isAPIResponse = (data: any): data is APIResponse => {
                    return (
                        typeof data.success == "boolean" &&
                        typeof data.errCode == "number" &&
                        typeof data.data == "object"
                    )
                }
                if (response.status == 200 && isAPIResponse(response.data)) {
                    const result = <APIResponse>response.data
                    if (result.success) {
                        if (success != undefined) {
                            success(result.data)
                        }
                    } else {
                        emitter.emit("apierror", errDescription[result.errCode])
                        if (result.errCode == 99991) {
                            token.clear()
                            router.replace({ name: "login" })
                        } else if (error != undefined) {
                            error(result.errCode)
                        }
                    }
                } else {
                    emitter.emit("fatalerror", "网络错误：返回类型错误。请手动刷新页面")
                }
            })
            .catch((error) => {
                console.log(error)
                emitter.emit("fatalerror", "网络错误：" + error.code + "。请手动刷新页面")
            })
    },
}

export { callapi }
