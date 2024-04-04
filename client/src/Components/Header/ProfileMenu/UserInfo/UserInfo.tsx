import {useAuth} from "../../../../Hooks/useAuth";
import user_avatar from "./user.png";
import {Link, useNavigate} from "react-router-dom";
import {useToken} from "../../../../Hooks/useToken";
import {useState} from "react";
import Button from "@mui/material/Button";
import {useDesktop} from "../../../../Hooks/useDesktop.ts";

export default function UserInfo() {
    const navigate = useNavigate()
    const {resetTokens} = useToken()
    const {is_moderator, logOut} = useAuth()
    const [isOpen, setIsOpen] = useState(false);
    const {isDesktopMedium} = useDesktop();

    const doLogOut = () => {
        logOut()
        resetTokens()
        navigate("/home/")
    }

    return (
        <div className="user-info">
            {isDesktopMedium && <>
                <div className="user-info-wrapper-close">
                    <img src={user_avatar} className="user-avatar" onClick={() => setIsOpen(!isOpen)}
                         alt="User avatar"/>
                </div>
                <div className={`user-info-wrapper ${isOpen ? "open" : ""}`}>
                    {/*<span>Имя: {full_name}</span>*/}
                    {/*<span>Должность: {post}</span>*/}
                    {/*<span>Название организации: {name_organization}</span>*/}
                    {/*{address && <span>Адрес: {address}</span>}*/}
                    <span>Статус: {is_moderator ? "Модератор" : "Пользователь"}</span>

                    <Button variant="outlined" sx={{color: 'white', borderColor: 'white'}} onClick={doLogOut}>
                        Выйти
                    </Button>
                </div>
            </>
            }
            {!isDesktopMedium &&
                <div style={{padding: '30px'}}>
                    {/*<p style={{fontSize: '18px', color: '#fff'}}>Имя: {full_name}</p>*/}
                    {/*<br/>*/}
                    {/*<p style={{fontSize: '18px', color: '#fff'}}>Должность: {post}</p>*/}
                    {/*<br/>*/}
                    {/*<p style={{fontSize: '18px', color: '#fff'}}>Название организации: {name_organization}</p>*/}
                    {/*{address && <br/> && <span style={{fontSize: '18px', color: '#fff'}}>Адрес: {address}</span>}*/}
                    <p style={{fontSize: '18px', color: '#fff'}}> <br/> Статус: {is_moderator ? "Модератор" : "Пользователь"}</p>
                    <br/>
                    <Link to="/auth/" className="menu-item" style={{textDecoration: 'none'}}>
                        <Button variant="outlined" sx={{color: 'white', borderColor: 'white'}} onClick={doLogOut}>
                            Выйти
                        </Button>
                    </Link>
                </div>
            }
        </div>
    );
};