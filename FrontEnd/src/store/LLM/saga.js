import { call, put, takeEvery, all, fork } from "redux-saga/effects";

// Crypto Redux States
import {  API_GET_LLM_MODELS,} from "./actionType";
import {LLMApiError, LLMApiSuccess } from "./actions";
import { useNavigate } from 'react-router-dom';
import * as path from "../../Routes/Paths"

//Include Both Helper File with needed methods
import { 
  callGetLLMModels,
}
  from "../../helpers/fakebackend_helper";

function* getLLMModels() {
  // payload contains the project id.    
  try{ 
    // No Need to send Token, it is already attached to the axios token authentication.
    const response = yield call(callGetLLMModels);
    if (response.status === 200){
      yield put(LLMApiSuccess(API_GET_LLM_MODELS, response.data));
    }
  }catch(e){ 
    yield put(LLMApiError(API_GET_LLM_MODELS, e));
  }
}

function* llmSaga() {  
  yield takeEvery(API_GET_LLM_MODELS, getLLMModels);
}

export default llmSaga;
