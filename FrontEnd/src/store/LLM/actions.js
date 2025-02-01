import {
  API_RESPONSE_SUCCESS,
  API_RESPONSE_ERROR,  
  API_GET_LLM_MODELS
} from "./actionType";
 
// common success
export const LLMApiSuccess = (actionType, data) => ({
  type: API_RESPONSE_SUCCESS,
  payload: { actionType, data },
});

// common error
export const LLMApiError = (actionType, error) => ({
  type: API_RESPONSE_ERROR,
  payload: { actionType, error },
});

export const getLLMModels = () => (
{
  type: API_GET_LLM_MODELS,
})
 