import { takeEvery, fork, put, all, call } from "redux-saga/effects";

//Account Redux states
import { REGISTER_USER, REQUEST_USER_ACTIVATION, REQUEST_USER_REACTIVATION } from "./actionTypes";
import { registerUserSuccessful, registerUserFailed, ApiSuccess, ApiError } from "./actions";

//Include Both Helper File with needed methods
import { getFirebaseBackend } from "../../../helpers/firebase_helper";
import {
  postRegister,
  postJwtRegister,
  postUserActivation,
  postResendUserActivation
} from "../../../helpers/fakebackend_helper";

// initialize relavant method of both Auth
const fireBaseBackend = getFirebaseBackend();

// Is user register successfull then direct plot user in redux.
function* registerUser({ payload: { user } }) {
  try { 
      const response = yield call(postRegister, user);
      console.log(response)
      if (response.status === 201) {
        yield put(registerUserSuccessful(response.data));
      } else {
        yield put(registerUserFailed(response.data));
      } 
  } catch (error) {
    console.log(error)
    yield put(registerUserFailed(error));
  }
}


function* activateUser({ payload: { token } }) {
  try {
    
      const response = yield call(postUserActivation, token); 
      if (response.status === 200) {
        yield put(ApiSuccess(REQUEST_USER_ACTIVATION, ""));
      } else {
        yield put(ApiError(REQUEST_USER_ACTIVATION, "Error"));
      }
      
  } catch (error) { 
    yield put(ApiError(REQUEST_USER_ACTIVATION, error));
  }
}

function* reActivateUser({ payload: { email } }) {
  try {
      const data = {
        email: email
      }
      const response = yield call(postResendUserActivation, data); 
      if (response.status === 200) {
        yield put(ApiSuccess(REQUEST_USER_REACTIVATION, response.data));
      } else {
        yield put(ApiError(REQUEST_USER_REACTIVATION, "Error"));
      }
      
  } catch (error) {
    yield put(ApiError(REQUEST_USER_REACTIVATION, error));
  }
}


export function* watchUserRegister() {
  yield takeEvery(REGISTER_USER, registerUser);
}

function* accountSaga() {
  yield all([fork(watchUserRegister)]);
  yield takeEvery(REQUEST_USER_ACTIVATION, activateUser);
  yield takeEvery(REQUEST_USER_REACTIVATION, reActivateUser);
}

export default accountSaga;
