import {
  API_RESPONSE_SUCCESS,
  API_RESPONSE_ERROR,
  GET_ALL_PROJECTS_DATA,
  DEL_A_PROJECT,
  API_DEL_PROJECT,
  DEACTIVATE_TOUR,
  GET_USER_TOURS
} from "./actionType";


// get user deactivated tours
export const getUserDeactivatedTours = () => ({
  type: GET_USER_TOURS,
  payload: {},
});


// deactivate user tour
export const deactivateUserTour = (tour_id) => ({
  type: DEACTIVATE_TOUR,
  payload: { tour_id },
});

// common success
export const dashboardProjectApiSuccess = (actionType, data) => ({
  type: API_RESPONSE_SUCCESS,
  payload: { actionType, data },
});

// common error
export const dashboardProjectApiError = (actionType, error) => ({
  type: API_RESPONSE_ERROR,
  payload: { actionType, error },
});

// Project Lists
export const getAllProjectsData = (AllprojectsData) => ({
  type: GET_ALL_PROJECTS_DATA,
  payload: AllprojectsData
});


// Delete a project
export const deleteABPProject = (projectId, delConfPass) => ({
  type: DEL_A_PROJECT,
  payload: {projectId, delConfPass}
});

// Delete a project
export const apiDeleteTheABPProject = (projectId) => ({
  type: API_DEL_PROJECT,
  payload: {projectId}
});