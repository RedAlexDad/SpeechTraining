import "./NavMenu.sass"
import {Link} from "react-router-dom";

export default function NavMenu () {
    return (
        <div className="menu-wrapper">

            <Link to="/geographicalObject" className="menu-item">
                <span>Географические объекты</span>
            </Link>

            <Link to="/profile" className="menu-item">
                <span>Личный кабинет</span>
            </Link>

        </div>
    )
}