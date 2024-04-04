import "./Header.sass"
// import NavMenu from "./NavMenu/NavMenu.tsx";
import ProfileMenu from "./ProfileMenu/ProfileMenu";

export default function Header() {
    return (
        <div className={"header-wrapper"}>
            <div className="right-container">
                <ProfileMenu/>
            </div>
        </div>
    )
}