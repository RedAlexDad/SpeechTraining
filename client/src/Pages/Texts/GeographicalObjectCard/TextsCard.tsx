import "./TextsCard.sass";
import {GeographicalObject} from "../../../Types.ts";
import {Link} from "react-router-dom";
import mockImage from "../../../assets/mock.png";
import {useAuth} from "../../../Hooks/useAuth.ts";
import {useToken} from "../../../Hooks/useToken.ts";
import {useDispatch} from "react-redux";
// import {
//     updateGeographicalObject,
//     updateID_draft,
//     getCountGeographicalObjectByDraft
// } from "../../../store/GeographicalObject.ts";

import {Dispatch, SetStateAction, useEffect, useState} from "react";
import {Button} from "@mui/material";
// import {
//     ApiGeographicalObjectGetRequest,
//     ApiGeographicalObjectIdCreateServiceInTaskPostRequest,
//     // ApiGeographicalObjectIdDeleteDeleteRequest,
//     GeographicalObjectApi
// } from "../../../../swagger/generated-code";

// import {GeographicalObjectsMock} from "../../../Consts.ts";

export default function TextsCard({geographical_object, setUpdateTriggerParent}: {
    geographical_object: GeographicalObject;
    setUpdateTriggerParent: Dispatch<SetStateAction<boolean>>;
}) {
    const dispatch = useDispatch();
    const {is_authenticated} = useAuth();
    const {access_token} = useToken();
    const [photoUrl, setPhotoUrl] = useState('');

    // const get_photo = async () => {
    //     // Получаем ID географического объекта
    //     const geographicalObjectId = geographical_object?.id;
    //     if (geographicalObjectId === undefined || geographicalObjectId === null || geographicalObjectId === -1) {
    //         return;
    //     }
    //     const api = new GeographicalObjectApi();
    //     try {
    //         const response: Blob = await api.apiGeographicalObjectIdImageGet({
    //             id: geographicalObjectId,
    //         });
    //         if (response) {
    //             const blob = response as Blob;
    //             const url = URL.createObjectURL(blob);
    //             setPhotoUrl(url);
    //         } else {
    //             setPhotoUrl(mockImage);
    //         }
    //     } catch (error) {
    //         // console.error('Error fetching image:', error);
    //         setPhotoUrl(mockImage);
    //     }
    // };

    // const addGeographicalObjectInMarsStation = async () => {
    //     const api = new GeographicalObjectApi();
    //     const requestParameters: ApiGeographicalObjectIdCreateServiceInTaskPostRequest = {
    //         id: geographical_object.id,
    //         authorization: access_token,
    //     };
    //     await api.apiGeographicalObjectIdCreateServiceInTaskPost(requestParameters)
    //         .then(() => {
    //             // console.log("Успешно! Отправлена услуга на заявку!", response);
    //             searchGeographicalObject();
    //         })
    //         .catch(error => {
    //             console.error("Ошибка отправления!\n", error);
    //         })
    // };

    // const searchGeographicalObject = async () => {
    //     const api = new GeographicalObjectApi();
    //     const requestParameters: ApiGeographicalObjectGetRequest = {
    //         authorization: access_token,
    //     };
    //     api.apiGeographicalObjectGet(requestParameters)
    //         .then(response => {
    //             // console.log("Успешно!", response);
    //             dispatch(updateGeographicalObject([...response.results]));
    //             dispatch(updateID_draft(response.idDraftService));
    //             dispatch(getCountGeographicalObjectByDraft(response.countGeographicalObjectByDraft));
    //         })
    //         .catch(error => {
    //             console.error("Ошибка!\n", error);
    //             dispatch(updateGeographicalObject(GeographicalObjectsMock));
    //             return;
    //         })
    // };

    // const deleteGeographicalObject = async () => {
    //     try {
    //         const api = new GeographicalObjectApi();
    //         const requestParameters: ApiGeographicalObjectIdDeleteDeleteRequest = {
    //             id: geographical_object.id,
    //             authorization: access_token,
    //         };
    //         await api.apiGeographicalObjectIdDeleteDelete(requestParameters);
    //         // console.log("Успешно! Услуга удалена!");
    //         setUpdateTriggerParent(true);
    //     } catch (error) {
    //         console.error("Ошибка удаления!\n", error);
    //     }
    // };

    // useEffect(() => {
    //     get_photo();
    // }, [geographical_object.id]);

    return (
        <div className="card-wrapper">
            <Link to={`/geographical_object/${geographical_object.id}/`}
                  style={{textDecoration: 'none', color: 'inherit'}}>
                <div className="preview">
                    <img
                        src={photoUrl}
                        alt=""
                    />
                </div>
                <div className="card-content">
                    <div className="content-top">
                        <h3 className="title">{geographical_object.feature}</h3>
                    </div>
                </div>
            </Link>
            <div className="card-content">
                {/*{is_authenticated && (*/}
                {/*    <div style={{textAlign: 'center', marginTop: '0px', zIndex: '1'}}>*/}
                {/*        <Button variant="contained"*/}
                {/*                color="secondary"*/}
                {/*                onClick={addGeographicalObjectInMarsStation}*/}
                {/*        >*/}
                {/*            Добавить в полет*/}
                {/*        </Button>*/}
                {/*    </div>*/}
                {/*)}*/}
            </div>
        </div>
    );
};
