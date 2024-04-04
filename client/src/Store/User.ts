import { createSlice } from "@reduxjs/toolkit";

const initialState = {
	id_user: -1,
	username: "",
	is_authenticated: false,
	is_moderator: false,
};

const user = createSlice({
	name: "user",
	initialState: initialState,
	reducers: {
		updateUser: (state, action) => {
			Object.assign(state, action.payload);
		},
		cleanUser: (state) => {
			Object.assign(state, initialState);
		},
	},
});

export const { updateUser, cleanUser } = user.actions;
export default user.reducer;