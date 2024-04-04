import {useDispatch, useSelector} from 'react-redux';
import {updateUser, cleanUser} from "../Store/User.ts";
import axios from "axios";
import {useToken} from "./useToken";
import {DOMEN} from "../Consts.ts";
import {RootState} from "../Store/store.ts";

export function useAuth() {
    const selectedUserData = useSelector((state: RootState) => state.user);

    const {
        id_user,
        is_authenticated,
        is_moderator,
        username,
    } = selectedUserData;

    const dispatch = useDispatch()

    const setUser = (user_value: any) => {
        dispatch(updateUser(user_value));
    }

    const sendRequest = async () => {
        const {access_token} = useToken()
        await axios(`${DOMEN}/api/logout/`, {
            method: "POST",
            headers: {
                'authorization': `${access_token}`
            }
        })
            .then(response => {
                console.log(response.data)
            })
            .catch(error => {
                console.error(error);
            });
    }

    const logOut = async () => {
        sendRequest();
        dispatch(cleanUser());
    }

    return {
        id_user,
        is_authenticated,
        is_moderator,
        username,
        setUser,
        logOut,
    };
}