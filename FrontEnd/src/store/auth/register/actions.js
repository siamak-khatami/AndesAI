import {
  REGISTER_USER,
  REGISTER_USER_SUCCESSFUL,
  REGISTER_USER_FAILED,
  RESET_REGISTER_FLAG,
  REQUEST_USER_ACTIVATION,
  REQUEST_USER_REACTIVATION,
  API_RESPONSE_ERROR,
  API_RESPONSE_SUCCESS
} from "./actionTypes"

export const ApiSuccess = (actionType, data) => ({
  type: API_RESPONSE_SUCCESS,
  payload: { actionType, data },
});

// common error
export const ApiError = (actionType, error) => ({
  type: API_RESPONSE_ERROR,
  payload: { actionType, error },
});

export const requestUserActivation = (token) => {
  return {
    type: REQUEST_USER_ACTIVATION,
    payload: { token },
  }
}

export const requestUserReActivation = (email) => {
  return {
    type: REQUEST_USER_REACTIVATION,
    payload: { email },
  }
}

export const registerUser = user => {
  return {
    type: REGISTER_USER,
    payload: { user },
  }
}

export const registerUserSuccessful = user => {
  return {
    type: REGISTER_USER_SUCCESSFUL,
    payload: user,
  }
}

export const registerUserFailed = user => {
  return {
    type: REGISTER_USER_FAILED,
    payload: user,
  }
}

export const resetRegisterFlag = () => {
  return {
    type: RESET_REGISTER_FLAG,
  }
}
