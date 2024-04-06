import "./Styles/Main.sass"
import "./Styles/Reset.sass"
import Header from "./Components/Header/Header";
import {BrowserRouter, Route, Routes, Navigate, Outlet, useLocation} from "react-router-dom";
import ProfilePage from "./Pages/Profile/ProfilePage";
import HomePage from "./Pages/Home/Home";
import {store} from "./Store/store.ts"
import SignIn from "./Pages/Login/SignIn/SignIn";
import SignUp from "./Pages/Login/SignUp/SignUp";
import {Provider} from "react-redux"
import {QueryClient, QueryClientProvider} from "react-query";
import {useAuth} from "./Hooks/useAuth.ts";
import SpeechPage from "./Pages/Speech/Speech.tsx";
import HearingPage from "./Pages/Hearing/Hearing.tsx";

const LoginFormLayout = () => {
    return (
        <div className="login-wrapper">
            <Outlet/>
        </div>
    )
}

function App() {
    const queryClient = new QueryClient()

    return (
        <QueryClientProvider client={queryClient}>
            <Provider store={store}>
                <BrowserRouter basename="/Trainer">
                    <div className="App">
                        <div className="wrapper">
                            <Header/>
                            <div className={"content-wrapper"}>
                                <Routes>
                                    <Route path="/" element={<Navigate to="/home/" replace/>}/>
                                    {/*Начальное меню*/}
                                    <Route path="/home/" element={<HomePage/>}/>

                                    <Route path="/auth/" element={<LoginFormLayout/>}>
                                        <Route path="" element={<Navigate to="login/" replace/>}/>
                                        <Route path="login/" element={<SignIn/>}/>
                                        <Route path="register/" element={<SignUp/>}/>
                                    </Route>

                                    {/*Тренажер речи*/}
                                    <Route path="/speech/" element={<SpeechPage/>}/>

                                    {/*Тренажер слуха*/}
                                    <Route path="/hearing/" element={<HearingPage/>}/>

                                    {/*Личный кабинет*/}
                                    <Route path="/profile/" element={<ProfilePage/>}/>
                                    {/*Список географических объектов*/}
                                </Routes>
                            </div>
                        </div>
                    </div>
                </BrowserRouter>
            </Provider>
        </QueryClientProvider>
    )
}

export default App
