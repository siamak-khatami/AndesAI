import {
  API_RESPONSE_SUCCESS,
  API_RESPONSE_ERROR,
  GET_ALL_PROJECTS_DATA,
  DEL_A_PROJECT,
  API_DEL_PROJECT,
  DEACTIVATE_TOUR,
  GET_USER_TOURS
} from "./actionType";

const INIT_STATE = {
  isloading: true,
  AllProjectsMetaData: [],
  error: {},
  delProjectId: null,
  delConfPass: null,
  deActivatingTour: false,
  gettingTours: false,
  toursLoaded: false,
  userTours: {}
};

const Dashboard = (state = INIT_STATE, action) => {
  switch (action.type) {
    case GET_USER_TOURS:
      return {
        ...state,
        gettingTours: true, // we put the project Id inside the payload 
        toursLoaded: false
      }
    case DEACTIVATE_TOUR:
      return {
        ...state,
        deActivatingTour: true, // we put the project Id inside the payload
        error: {}
      }
    case DEL_A_PROJECT:
      return {
        ...state,
        delProjectId: action.payload.projectId, // we put the project Id inside the payload
        delConfPass: action.payload.delConfPass
      }
    case API_DEL_PROJECT:
      return {
        ...state,
        isloading: true,
        delProjectId: action.payload.projectId, // we put the project Id inside the payload
      }
    case GET_ALL_PROJECTS_DATA:
      return {
        ...state,
        isloading: true,
      };
    case API_RESPONSE_SUCCESS:
      switch (action.payload.actionType) {
        case GET_USER_TOURS:
          return {
            ...state,
            gettingTours: false, // we put the project Id inside the payload
            toursLoaded: true,
            userTours: action.payload.data, 
          }
        case DEACTIVATE_TOUR:
          return {
            ...state,
            deActivatingTour: false, // we put the project Id inside the payload
            error: {}
          }
        case GET_ALL_PROJECTS_DATA:
          return {
            ...state,
            isloading: false,
            AllProjectsMetaData: action.payload.data
          };
        case API_DEL_PROJECT:
          return {
            ...state,
            isloading: false,
            delProjectId: action.payload.projectId
          };
        default:
          return state;
      }
    case API_RESPONSE_ERROR:
      switch (action.payload.actionType) {
        case GET_USER_TOURS:
          return {
            ...state,
            gettingTours: false, // we put the project Id inside the payload 
            toursLoaded: false,
            error: action.payload.error
          }
        case DEACTIVATE_TOUR: 
          return {
            ...state,
            deActivatingTour: false, // we put the project Id inside the payload
            error: action.payload.error
          }
        case GET_ALL_PROJECTS_DATA:
          return {
            ...state,
            isloading: false,
            error: action.payload.error
          };
        case API_DEL_PROJECT:
          return {
            ...state,
            isloading: false,
            error: action.payload.error,
            delProjectId: action.payload.projectId
          };
        default:
          return state;
      }
    default:
      return state;
  }
};
export default Dashboard;