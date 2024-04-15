import "./ProfileMenu.sass"
import {useEffect, useState} from "react";
import Hamburger from "../Hamburger/Hamburger";
import {Link} from "react-router-dom";
import axios from "axios";
import UserInfo from "./UserInfo/UserInfo";
import {useAuth} from "../../../Hooks/useAuth";
import {useToken} from "../../../Hooks/useToken";
import {DOMEN} from "../../../Consts.ts";

export default function ProfileMenu() {
    const {access_token} = useToken()
    const {is_authenticated, is_moderator, setUser} = useAuth()

    const auth = async () => {
        const url = `${DOMEN}get_token/`;
        await axios.post(url, {}, {
            headers: {
                "Content-type": "application/json; charset=UTF-8",
                authorization: access_token,
            },
        })
            .then(response => {
                const user = {
                    id_user: response.data.account["id"],
                    is_authenticated: true,
                    username: response.data.account["username"],
                    is_moderator: response.data.account["is_moderator"],
                };
                setUser(user);
            })
            .catch(error => {
                if (error.response.status == 401) {
                    console.error("Не авторизирован");
                } else {
                    console.error("Ошибка!\n", error);
                }
            });
    };

    useEffect(() => {
        if (!is_authenticated) {
            auth();
        }
    }, [is_authenticated]);


    const [isOpen, setIsOpen] = useState<boolean>(false)

    if (is_authenticated) {
        return (
            <div className={"profile-menu-wrapper"}>
                <div className={"menu-wrapper " + (isOpen ? "open" : "")}>
                    <Link to="/home/" className="menu-item" style={{textDecoration: 'none'}}>
                        <span className="item">Главная</span>
                    </Link>
                    {!is_moderator &&
                        <Link to="/speech/" className="menu-item" style={{textDecoration: 'none'}}>
                            <span className="item">Проверьте свою речь</span>
                        </Link>
                    }
                    {!is_moderator &&
                        <Link to="/hearing/" className="menu-item" style={{textDecoration: 'none'}}>
                            <span className="item">Проверьте свой слух</span>
                        </Link>
                    }
                    {is_moderator &&
                        <Link to="/analysis/" className="menu-item"
                              style={{textDecoration: 'none'}}>
                            <span className="item">Анализ данных</span>
                        </Link>
                    }
                    <UserInfo/>
                </div>
                <Hamburger isOpen={isOpen} setIsOpen={setIsOpen}/>
            </div>
        )
    }

    return (
        <div className={"profile-menu-wrapper"}>
            <div className={"menu-wrapper " + (isOpen ? "open" : "")}>
                <Link to="/home/" className="menu-item" style={{textDecoration: 'none'}}>
                    <span className="item">Главная</span>
                </Link>
                <Link to="/speech/" className="menu-item" style={{textDecoration: 'none'}}>
                    <span className="item">Проверьте свою речь</span>
                </Link>
                <Link to="/hearing/" className="menu-item" style={{textDecoration: 'none'}}>
                    <span className="item">Проверьте свой слух</span>
                </Link>
                <Link to="/auth/" className="menu-item" style={{textDecoration: 'none'}}>
                    <span className="item">Вход</span>
                </Link>
            </div>
            <Hamburger isOpen={isOpen} setIsOpen={setIsOpen}/>
        </div>
    )
}