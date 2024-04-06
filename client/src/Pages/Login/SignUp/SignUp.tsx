import "../Login.sass"
import {FaLock, FaRegBuilding, FaSignsPost, FaUser} from "react-icons/fa6";
import {GrLogin} from "react-icons/gr";
import {Link, useNavigate} from "react-router-dom";
import axios from "axios";
import {useToken} from "../../../Hooks/useToken";
import {useAuth} from "../../../Hooks/useAuth";
import {DOMEN} from "../../../Consts.ts";
import Button from "@mui/material/Button";
import React from "react";

export default function SignUp() {
    const navigate = useNavigate()
    const {setAccessToken} = useToken()
    const {setUser} = useAuth()

    const login = async (data: any) => {
        const url: string = `${DOMEN}api/authentication/`;
        await axios.post(url, {
            username: data.username,
            password: data.password
        }, {
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            },
        })
            .then(response => {
                setAccessToken(response.data['access_token'])
                const permissions = {
                    is_authenticated: true,
                    id: response.data["id"],
                    username: response.data["username"],
                    is_moderator: response.data["is_moderator"],
                }
                setUser(permissions)
                navigate("/home/");
            })
            .catch(error => {
                console.error("Ошибка!\n", error);
            });
    }

    const register = async (data: any) => {
        const url: string = `${DOMEN}api/register/`;
        await axios.post(url, data, {
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            },
        })
            .then(response => {
                console.log(response.data)
                console.log(data)
                login(data)
            })
            .catch(error => {
                console.error("Ошибка!\n", error);
            });
    }
    const handleSubmit = async (e: any) => {
        e.preventDefault()
        const formElement = e.currentTarget.closest('form');
        if (formElement) {
            const formData = new FormData(formElement);
            const username = formData.get('username') as string;
            const password = formData.get('password') as string;
            const name = formData.get('name') as string;
            const lastname = formData.get('lastname') as string;
            const fathername = formData.get('fathername') as string;

            const data = {
                username: username,
                password: password,
                is_moderator: false,
                name: name,
                lastname: lastname,
                fathername: fathername,
            }
            await register(data)
        }
    }

    return (
        <div className="auth-container">
            <div className="header">
                <div className="text">
                    Регистрация
                </div>
            </div>
            <form className="inputs">
                <div className="input">
                    <GrLogin className="icon"/>
                    <input type="text" placeholder="Логин" name="username"/>
                </div>
                <div className="input">
                    <FaLock className="icon"/>
                    <input type="password" placeholder="Пароль" name="password"/>
                </div>
                <div className="input">
                    <FaUser className="icon"/>
                    <input type="text" placeholder="Фамилия" name="name"/>
                </div>
                <div className="input">
                    <FaSignsPost className="icon"/>
                    <input type="text" placeholder="Имя" name="lastname"/>
                </div>
                <div className="input">
                    <FaRegBuilding className="icon"/>
                    <input type="text" placeholder="Отчество" name="fathername"/>
                </div>
                <div className="sign-in-link-container">
                    <Link to="/auth/login/" style={{textDecoration: 'none'}}>
                        <span>Уже есть аккаут?</span>
                    </Link>
                </div>
                <Button
                    variant="outlined"
                    sx={{color: 'white', borderColor: 'white'}}
                    onClick={(e) => handleSubmit(e as React.MouseEvent<HTMLButtonElement>)}
                >
                    Зарегестрироваться
                </Button>
            </form>
        </div>
    )
}