import "./SearchBar.sass";
import {useDispatch, useSelector} from "react-redux";
// import {updateFeatureGeographicalObject} from "../../../Store/Search.ts";
import {InputAdornment, TextField} from "@mui/material";
import {useState} from "react";
import SearchIcon from '@mui/icons-material/Search';
import IconButton from "@mui/material/IconButton";
import {RootState} from "../../../Store/store.ts";

export default function SearchBar() {
    const dispatch = useDispatch();
    const feature = useSelector((state: RootState) => state.search.feature);
    const [searchFeature, setSearchFeature] = useState<string>('' || feature)

    const handleChange = (value: string) => {
        setSearchFeature(value)
    };

    // Выполняем поиск при нажатии на клавише Enter (код клавиши 13)
    // const handleKeyDown = (e: React.KeyboardEvent<HTMLDivElement>) => {
    //     if (e.key === "Enter") {
    //         dispatch(updateFeatureGeographicalObject(searchFeature));
    //     }
    // };

    // Выполняем поиск при нажатии на кнопку поиска
    // const handleSearchClick = () => {
    //     dispatch(updateFeatureGeographicalObject(searchFeature));
    // };

    return (
        <TextField
            type="text"
            id="outlined-basic"
            label="Поиск..."
            variant="outlined"
            autoComplete="feature"
            value={searchFeature}
            onChange={(e) => handleChange(e.target.value)}
            // Добавляем обработчик события для клавиши Enter
            onKeyDown={handleKeyDown}
            // Добавляем InputAdornment с кнопкой поиска
            InputProps={{
                endAdornment: (
                    <InputAdornment position="end">
                        <IconButton
                            onClick={handleSearchClick}
                            edge="end"
                            sx={{color: 'white'}}
                        >
                            <SearchIcon/>
                        </IconButton>
                    </InputAdornment>
                ),
            }}
            sx={{
                '& input, & label, & .MuiIconButton-label': {color: 'white'},
                '& .MuiOutlinedInput-notchedOutline': {
                    borderColor: 'white',
                },
                '&:hover .MuiOutlinedInput-notchedOutline': {
                    borderColor: 'white',
                },
                '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                    borderColor: 'white',
                },
            }}
        />
    );
}