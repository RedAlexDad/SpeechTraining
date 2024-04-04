import Cookies from "universal-cookie";

export function useToken() {
    const cookies = new Cookies()
    const access_token = cookies.get("access_token");
    const setAccessToken = (value: string) => {
        cookies.set("access_token", value, {path: '/Trainer/', expires: new Date(Date.now() + 25920000)})
    }

    const resetAccessToken = () => {
        cookies.set("access_token", undefined, {path: '/Trainer/', expires: new Date(Date.now() + 25920000)})
    }

    const resetTokens = () => {
        resetAccessToken()
    }

    return {
        access_token,
        setAccessToken,
        resetAccessToken,
        resetTokens
    };
}