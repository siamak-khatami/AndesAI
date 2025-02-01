import { takeEvery, fork, put, all, call } from "redux-saga/effects";

// Login Redux States
import { FORGET_PASSWORD, RESET_PASSWORD } from "./actionTypes";
import { apiErrorResetPass, apiSuccessResetPass } from "./actions";

//Include Both Helper File with needed methods
import { patchResetPassword, postResetPassword } from "../../../helpers/fakebackend_helper" 
//If user is send successfully send mail link then dispatch redux action's are directly from here.
function* forgetPass({ payload }) {   
  try {
    const response = yield call(postResetPassword, payload) 
    if (response.status==200) {
      yield put( 
        apiSuccessResetPass(FORGET_PASSWORD, "A reset link is sent to your email address.")
      )
    } 
  } catch (error) {  
    yield put(apiErrorResetPass(FORGET_PASSWORD, error.data));
  }
}

function* resetPassword({ payload }) { 
  try {
    const response = yield call(patchResetPassword, payload)
    
    if (response.status==200) {
      yield put(
        apiSuccessResetPass(RESET_PASSWORD, "Password is changed.")
      )
    } 
  } catch (error) { 
    const e = error.error_id == 1? "Link is expired. Please re-apply for password resetting.":error.data
    yield put(apiErrorResetPass(RESET_PASSWORD, e));
  }
}

export function* watchUserPasswordForget() {
  yield takeEvery(FORGET_PASSWORD, forgetPass);
  yield takeEvery(RESET_PASSWORD, resetPassword);
}

function* forgetPasswordSaga() {
  yield all([fork(watchUserPasswordForget)]);
}

export default forgetPasswordSaga;
