import {
  API_RESPONSE_SUCCESS,
  API_RESPONSE_ERROR, 
  API_GET_LLM_MODELS
} from "./actionType";

const INIT_STATE = {
  isloading: true, 
  error: {}, 
  llmModels: {}
};

const LLM = (state = INIT_STATE, action) => {
  switch (action.type) {
    case API_GET_LLM_MODELS:
      return {
        ...state, 
        isloading: true,
        error: {}
      };
    case API_RESPONSE_SUCCESS:
      switch (action.payload.actionType) {
        case API_GET_LLM_MODELS:
          return {
            ...state, 
            isloading: false,
            llmModels: action.payload.data,
            error: {}
          };
        default:
          return state;
      }
    case API_RESPONSE_ERROR:
      switch (action.payload.actionType) {
        case API_GET_LLM_MODELS:
          return {
            ...state, 
            isloading: false, 
            error: action.payload.error,
          };
        default:
          return state;
      }
    default:
      return state;
  }
};
export default LLM;