import { takeEvery, fork, put, all, call } from "redux-saga/effects";

// Login Redux States
import { EDIT_PROFILE, UPDATE_PASSWORD } from "./actionTypes";
import { profileSuccess, profileError, ApiCallSuccess, ApiCallError } from "./actions";

//Include Both Helper File with needed methods
import { getFirebaseBackend } from "../../../helpers/firebase_helper";
import {
  postFakeProfile,
  postJwtProfile,
  postNewPassword
} from "../../../helpers/fakebackend_helper";

const fireBaseBackend = getFirebaseBackend();

function* editProfile({ payload: { user } }) {
  try {
    if (process.env.REACT_APP_DEFAULTAUTH === "firebase") {
      const response = yield call(
        fireBaseBackend.editProfileAPI,
        user.username,
        user.idx
      )
      yield put(profileSuccess(response))
    } else if (process.env.REACT_APP_DEFAULTAUTH === "jwt") {
      const response = yield call(postJwtProfile, "/post-jwt-profile", {
        username: user.username,
        idx: user.idx,
      })
      yield put(profileSuccess(response))
    } else if (process.env.REACT_APP_API_URL) {
      const response = yield call(postFakeProfile, user);
      yield put(profileSuccess(response));
    }
  } catch (error) {
    yield put(profileError(error));
  }
}

function* updatePass({ payload: {password}}) {
  try {
      const response = yield call(postNewPassword, password)
      if (response.status === 202) {
        console.log(response.data)
        yield put(ApiCallSuccess(UPDATE_PASSWORD, response.data));
      } else {
        yield put(ApiCallError(UPDATE_PASSWORD, "Error"));
      }
  } catch (error) {
    yield put(ApiCallError(UPDATE_PASSWORD, error));
  }
}
export function* watchProfile() {
  yield takeEvery(EDIT_PROFILE, editProfile);
  yield takeEvery(UPDATE_PASSWORD, updatePass);
}

function* ProfileSaga() {
  yield all([fork(watchProfile)]);
}

export default ProfileSaga;
