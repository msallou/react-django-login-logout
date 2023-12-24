import axios from "axios";
import { REGISTER_SUCCESS, REGISTER_FAIL } from "./types";


export const register = (username, first_name, last_name, email, password, re_password) => async dispatch => {
    const config = {
        headers: {
            'Accept': 'application/json', // for passing in json responses
            'Content-Type': 'application/json'
        }
    }

    const body = JSON.stringify({username, first_name, last_name, email, password, re_password})

    try {
        const res = await axios.post(`${process.env.REACT_APP_API_URL}/accounts/register`, body, config)

        if (res.data.error) {
            dispatch({
                type: REGISTER_FAIL
            })
        } else {
            dispatch({
                type: REGISTER_SUCCESS
            })
        }
    } catch (err) {
        dispatch({
            type: REGISTER_FAIL
        })
    }
}