import {createSlice} from "@reduxjs/toolkit";

const initialState = {
    feature: "",
    full_name: "",
    status_task: [] as string[],
    date: {
        date_before: "",
        input_before: "",
        date_after: "",
        input_after: "",
    },
};

const feature_geographical_object = createSlice({
    name: "search",
    initialState: initialState,
    reducers: {
        updateFeatureGeographicalObject: (state, action) => {
            return {
                ...state,
                ...action.payload,
                feature: action.payload,
            }
        },
        updateFullNameEmployee: (state, action) => {
            return {
                ...state,
                ...action.payload,
                full_name: action.payload,
            }
        },
        updateStatusTask: (state, action) => {
            return {
                ...state,
                ...action.payload,
                status_task: action.payload,
            }
        },
        updateDateFormBefore: (state, action) => {
            return {
                ...state,
                date: {
                    ...state.date,
                    date_before: action.payload.date_before,
                    input_before: action.payload.input_before,
                },
            };
        },
        updateDateFormAfter: (state, action) => {
            return {
                ...state,
                date: {
                    ...state.date,
                    date_after: action.payload.date_after,
                    input_after: action.payload.input_after,
                },
            }
        },
    },
});

export const {
    updateFeatureGeographicalObject,
    updateFullNameEmployee,
    updateStatusTask,
    updateDateFormBefore,
    updateDateFormAfter,
} = feature_geographical_object.actions;

export default feature_geographical_object.reducer;