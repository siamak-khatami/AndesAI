import {
  REGISTER_USER,
  REGISTER_USER_SUCCESSFUL,
  REGISTER_USER_FAILED,
  RESET_REGISTER_FLAG,
  REQUEST_USER_ACTIVATION,
  REQUEST_USER_REACTIVATION,
  API_RESPONSE_SUCCESS,
  API_RESPONSE_ERROR
} from "./actionTypes";

const initialState = {
  registrationError: null,
  message: null,
  loading: false,
  user: null,
  success: false,
  error: false,
  err: {},
  loadingActivation: false,
  userActivated: false,
  userReActivation: false,
  registering: false,
};

const Account = (state = initialState, action) => {
  switch (action.type) {
    case REQUEST_USER_REACTIVATION:
      state = {
        ...state,
      };
      break;
    case REQUEST_USER_ACTIVATION:
      state = {
        ...state,
        loadingActivation: true,
      };
      break;
    case REGISTER_USER:
      state = {
        ...state,
        registering: true,
        registrationError: null,
      };
      break;
    case REGISTER_USER_SUCCESSFUL:
      state = {
        ...state,
        registering: false,
        user: action.payload,
        success: true,
        registrationError: null,
      };
      break;
    case REGISTER_USER_FAILED:
      state = {
        ...state,
        user: null,
        registering: false,
        registrationError: action.payload,
        error: true
      };
      break;
    case RESET_REGISTER_FLAG:
      state = {
        ...state,
        success: false,
        error: false
      };
      break;
    case API_RESPONSE_SUCCESS:
      switch (action.payload.actionType){
        case REQUEST_USER_REACTIVATION:
          state = {
            ...state,
            userReActivation: true,
            err:{}
          };
          break;
        case REQUEST_USER_ACTIVATION:
          state = {
            ...state,
            loadingActivation: false,
            userActivated : true, 
            err:{}
          };
          break;
        default:
          state =  {
            ...state,
            err: {}
          }
      }
    break
    case API_RESPONSE_ERROR:
      switch (action.payload.actionType){
        case REQUEST_USER_REACTIVATION:
          state = {
            ...state,
            userReActivation: false,
            err: action.payload.error,
          };
          break;
        case REQUEST_USER_ACTIVATION:
          state = {
            ...state,
            loadingActivation: false,
            userActivated : false, 
            err: action.payload.error,
          };
          break;
        default:
          state = { ...state };
      }
    break
    default:
      state = { ...state };
      break;
  }
  return state;
};

export default Account;
