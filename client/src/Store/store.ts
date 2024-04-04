import { configureStore } from "@reduxjs/toolkit";
import userReducer from "./User.ts";
import search from "./Search.ts";

export const store = configureStore({
	reducer: {
		user: userReducer,
		search: search,
	},
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;