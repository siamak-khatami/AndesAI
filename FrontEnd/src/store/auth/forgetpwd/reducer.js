import {
  FORGET_PASSWORD,
  API_SUCCESS_RESET_PASS,
  API_ERROR_RESET_PASS,
  RESET_PASSWORD,
} from "./actionTypes";

const initialState = {
  SuccessMsg: null,
  Error: null,
  requestingReset: false,
  resettingPassword: false,
  passChanged: false,
};

const forgetPassword = (state = initialState, action) => {  
  switch (action.type) {
    case RESET_PASSWORD:
      return {
        ...state,
        resettingPassword: true,
        passChanged: false,
        SuccessMsg: null,
        Error: null,
      };  
    case FORGET_PASSWORD:
      return {
        ...state,
        SuccessMsg: null,
        Error: null,
        requestingReset: true,
      };  
    case API_SUCCESS_RESET_PASS:  
      switch(action.payload.actionType){
        case RESET_PASSWORD: 
          return {
            ...state,
            resettingPassword: false,
            passChanged: true,
            SuccessMsg: action.payload.message,
            Error: null
          }; 
        case FORGET_PASSWORD: 
          return {
            ...state,
            SuccessMsg: action.payload.message,
            Error: null,
            requestingReset: false
          }; 
        default:
          return { ...state }; 
      }
    case API_ERROR_RESET_PASS: 
      switch(action.payload.actionType){
        case RESET_PASSWORD:
          return {
            ...state,
            resettingPassword: false,
            passChanged: false, 
            SuccessMsg: null,
            Error: action.payload.message
          }; 
        case FORGET_PASSWORD: 
          return {
            ...state, 
            SuccessMsg: null,
            Error: action.payload.message,
            requestingReset: false
          }; 
        default:
          return { ...state }; 
      } 
    default:
      return { ...state }; 
  } 
};

export default forgetPassword;
