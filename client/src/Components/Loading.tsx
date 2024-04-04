import Backdrop from '@mui/material/Backdrop';
import CircularProgress from '@mui/material/CircularProgress';
import {useEffect, useState} from "react";

export default function LoadingAnimation({isLoading}: { isLoading: boolean }) {
    const [open, setOpen] = useState(isLoading);
    useEffect(() => {
        setOpen(isLoading);
    }, [isLoading]);

    return (
        <div>
            <Backdrop
                sx={{color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1}}
                open={open}
                onClick={() => setOpen(false)}
            >
                <CircularProgress color="inherit"/>
            </Backdrop>
        </div>
    );
}
