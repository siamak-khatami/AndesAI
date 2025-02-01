import { call, put, takeEvery, all, fork } from "redux-saga/effects";

// Crypto Redux States
import { GET_ALL_PROJECTS_DATA, API_DEL_PROJECT, DEACTIVATE_TOUR, GET_USER_TOURS } from "./actionType";
import { dashboardProjectApiSuccess, dashboardProjectApiError } from "./actions";
import { useNavigate } from 'react-router-dom';
import * as path from "../../Routes/Paths"

//Include Both Helper File with needed methods
import { 
  callDeactivateTour,
}
  from "../../helpers/fakebackend_helper";
  

function* deactivateTour({payload}) {
  // payload contains the project id.  
  try{ 
    // No Need to send Token, it is already attached to the axios token authentication.
    const response = yield call(callDeactivateTour, payload.tour_id);
    if (response.status === 200){
      yield put(dashboardProjectApiSuccess(DEACTIVATE_TOUR, response.data));
    }
  }catch(e){ 
    yield put(dashboardProjectApiError(DEACTIVATE_TOUR, e));
  }
}

function* getTours() {
  // payload contains the project id.   
  try{ 
    // No Need to send Token, it is already attached to the axios token authentication.
    const response = yield call(callDeactivateTour);
    if (response.status === 200){
      yield put(dashboardProjectApiSuccess(GET_USER_TOURS, response.data));
    }
  }catch(e){ 
    yield put(dashboardProjectApiError(GET_USER_TOURS, e));
  }
}

function* dashboardSaga() { 
  yield takeEvery(DEACTIVATE_TOUR, deactivateTour);
  yield takeEvery(GET_USER_TOURS, getTours);
}

export default dashboardSaga;
