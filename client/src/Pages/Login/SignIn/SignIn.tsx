import "../Login.sass"
import {FaLock} from "react-icons/fa6";
import {GrLogin} from "react-icons/gr";
import {Link, useNavigate} from "react-router-dom";
import axios from "axios";
import {useToken} from "../../../Hooks/useToken";
import {useAuth} from "../../../Hooks/useAuth";
import {DOMEN} from "../../../Consts.ts";
import Button from "@mui/material/Button";
import React from "react";

export default function SignIn() {
    const navigate = useNavigate()
    const {setAccessToken} = useToken()
    const {setUser} = useAuth()

    const login = async (data: any) => {
        const url: string = `${DOMEN}api/authentication/`;
        await axios.post(url, data, {
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            },
        })
            .then(response => {
                setAccessToken(response.data['access_token'])
                const user = {
                    id_user: response.data["id"],
                    is_authenticated: true,
                    username: response.data["username"],
                    is_moderator: response.data["is_moderator"],
                }
                setUser(user)
                navigate("/home");
            })
            .catch(error => {
                console.error("Ошибка!\n", error);
            });
    }

    const handleSubmit = async (e: React.MouseEvent<HTMLButtonElement>) => {
        e.preventDefault();

        const formElement = e.currentTarget.closest('form');
        if (formElement) {
            const formData = new FormData(formElement);
            const username = formData.get('username') as string;
            const password = formData.get('password') as string;
            const data = {
                username: username,
                password: password
            }
            await login(data);
        }
    };


    return (
        <div className="auth-container">
            <div className="header">
                <div className="text">
                    Вход
                </div>
            </div>
            <form className="inputs">
                <div className="input">
                    <GrLogin/>
                    <input type="text" name="username" placeholder="Логин" required/>
                </div>
                <div className="input">
                    <FaLock/>
                    <input type="password" name="password" placeholder="Пароль" required/>
                </div>
                <div className="sign-up-link-container">
                    <Link to="/auth/register/" style={{textDecoration: 'none'}}>
                        <span> Ещё нет аккаунта? </span>
                    </Link>
                </div>
                <Button
                    variant="outlined"
                    sx={{color: 'white', borderColor: 'white'}}
                    onClick={(e) => handleSubmit(e as React.MouseEvent<HTMLButtonElement>)}
                >
                    Войти
                </Button>
            </form>
        </div>
    )
}