import { PROFILE_ERROR, PROFILE_SUCCESS, EDIT_PROFILE, RESET_PROFILE_FLAG, UPDATE_PASSWORD,
  API_CALL_SUCCESS, API_CALL_FAILURE } from "./actionTypes"



export const ApiCallSuccess = (actionType, data) => ({
  type: API_CALL_SUCCESS,
  payload: { actionType, data },
});

  // common error
export const ApiCallError = (actionType, error) => ({
  type: API_CALL_FAILURE,
  payload: { actionType, error },
});


export const updatePassword = (password) =>{
  return {
    type: UPDATE_PASSWORD,
    payload: {password}
  }
}

export const editProfile = user => {
  return {
    type: EDIT_PROFILE,
    payload: { user },
  }
}

export const profileSuccess = msg => {
  return {
    type: PROFILE_SUCCESS,
    payload: msg,
  }
}

export const profileError = error => {
  return {
    type: PROFILE_ERROR,
    payload: error,
  }
}

export const resetProfileFlag = error => {
  return {
    type: RESET_PROFILE_FLAG,
  }
}
