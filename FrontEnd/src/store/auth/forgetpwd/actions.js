import {
  FORGET_PASSWORD,
  API_SUCCESS_RESET_PASS,
  API_ERROR_RESET_PASS,
  RESET_PASSWORD
} from "./actionTypes";


export const patchResetPassword = (token, password) => ({
    type: RESET_PASSWORD,
    payload: {token, password},
  } );

export const userForgetPassword = (email) => ({
    type: FORGET_PASSWORD,
    payload: {email},
})

export const apiSuccessResetPass = (actionType, message) => ({
    type: API_SUCCESS_RESET_PASS,
    payload: {actionType, message},
})

export const apiErrorResetPass = (actionType, message) => ({
    type: API_ERROR_RESET_PASS,
    payload: {actionType, message}
})
