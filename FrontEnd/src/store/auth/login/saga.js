import { call, put, takeEvery, takeLatest } from "redux-saga/effects";
import { Navigate, Route } from "react-router-dom";

// Login Redux States
import { LOGIN_USER, LOGOUT_USER, SOCIAL_LOGIN, VALIDATE_AUTHENTICATION } from "./actionTypes";
import { apiError, loginSuccess, logoutUserSuccess, logoutUser } from "./actions";

import { profileSuccess} from "../profile/actions";
//Include Both Helper File with needed methods
import { getFirebaseBackend } from "../../../helpers/firebase_helper";
import {
  checkLogin,
  postFakeLogin,
  postJwtLogin,
  postSocialLogin,
} from "../../../helpers/fakebackend_helper";
import {PathDashboard, PathLogin} from "../../../Routes/Paths"
import {setAuthorization} from "../../../helpers/api_helper"
 

function* loginUser({ payload: { user, history } }) {
  // history is the navigation object sent to this function. 
  try {
      const formDT = new FormData()
      formDT.append('username', user.email)
      formDT.append('password', user.password)
      // Our backend accepts the login info in Form format, because of backend functions.
      
      try{
        
        const response = yield call(postFakeLogin, formDT); 
        if (response.status === 200){
          yield put(loginSuccess(response.data.user));
          yield put(profileSuccess(response.data));
          localStorage.setItem("authUser", JSON.stringify(response.data));
          // the token will be set after the next call, so any automatic call between login and next page load will nt have token, so
          // the token should be set directly.
          setAuthorization(response.data.access_token)
          history(PathDashboard)
        }else{ 
          yield put(apiError({"status": "errors", "data": "Something went wrong"}));
        }
      }catch(error){ 
        yield put(apiError(error));
      }
  } catch (error) { 
    yield put(apiError(error));
  }
}

function* logoutUserSaga() {
  try {
    localStorage.removeItem("authUser");
    localStorage.clear();
    yield put(logoutUserSuccess(LOGOUT_USER, true)); 
  } catch (error) {
    yield put(apiError(LOGOUT_USER, error));
  }
}

function* socialLogin({ payload: { data, history, type } }) {
  
  try {
    if (process.env.REACT_APP_DEFAULTAUTH === "firebase") {
      const fireBaseBackend = getFirebaseBackend();
      const response = yield call(fireBaseBackend.socialLoginUser, type);
      if (response) {
        history(PathDashboard);
      } else {
        history(PathLogin);
      }
      localStorage.setItem("authUser", JSON.stringify(response));
      yield put(loginSuccess(response));
    } else {
      const response = yield call(postSocialLogin, data);
      localStorage.setItem("authUser", JSON.stringify(response));
      yield put(loginSuccess(response));
    }
    history(PathDashboard);
  } catch (error) {
    yield put(apiError(error));
  }
}


function* validateAuth() {
  
  try {
    const response = yield call(checkLogin);
    if(response.status!==200){
      yield put(logoutUser());
      return <Navigate to={{ pathname: PathLogin }} />
    }
  } catch (error) {
    // If it gets the error on authentication, then it should navigate to the login page
    yield put(logoutUser());
    // yield put(resetRegisterFlag());
    return <Navigate to={{ pathname: PathLogin }} />
  }
}


function* authSaga() {
  yield takeEvery(LOGIN_USER, loginUser); // Whenever an action with LOGIN_USER type is called, the loginUser function will be luanched automatically.
  // For example, in the login page, by pushing the submit button, the action loginUser (which LOGIN_USER is its type) is called. The moment it is called,
  // This will be launched.
  yield takeLatest(SOCIAL_LOGIN, socialLogin);
  yield takeEvery(LOGOUT_USER, logoutUserSaga);
  yield takeEvery(VALIDATE_AUTHENTICATION, validateAuth);
}

export default authSaga;
