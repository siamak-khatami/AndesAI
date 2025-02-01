import { PROFILE_ERROR, PROFILE_SUCCESS, EDIT_PROFILE, RESET_PROFILE_FLAG, API_CALL_SUCCESS, API_CALL_FAILURE, UPDATE_PASSWORD } from "./actionTypes";

const initialState = {
  error: {},
  success: "",
  updatingPass: false,
  passUpdateSuccess: false,  
  user: {}
};

const profile = (state = initialState, action) => {
  switch (action.type) {
    case UPDATE_PASSWORD:
      state = {
        ...state,
        updatingPass: true, 
      }
      break
    case EDIT_PROFILE:
      state = { ...state };
      break;
    case PROFILE_SUCCESS:
      state = {
        ...state,
        success: action.payload.status,
        user: action.payload.user
      };
      break;
    case PROFILE_ERROR:
      state = {
        ...state,
        error: action.payload
      };
      break;
    case RESET_PROFILE_FLAG:
      state = {
        ...state,
        success: null
      };
      break;
    case API_CALL_SUCCESS:
      switch (action.payload.actionType){
        case UPDATE_PASSWORD:
          state = {
            ...state,
            updatingPass: false, 
            passUpdateSuccess: true, 
          }
          break
      }
      break
    case API_CALL_FAILURE:
        switch (action.payload.actionType){
          case UPDATE_PASSWORD: 
            state = {
              ...state,
              updatingPass: false,
              passUpdateSuccess: false, 
              error: action.payload.error
            }
            break
        }
        break
    default:
      state = { ...state };
      break;
  }
  return state;
};

export default profile;
