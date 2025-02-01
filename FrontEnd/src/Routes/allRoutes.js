import React from "react";

import { Navigate } from "react-router-dom";

//Dashboard
import Dashboard from "../pages/Dashboard"; 

//login
import Login from "../pages/Authentication/Login";
import ForgetPasswordPage from "../pages/Authentication/ForgetPassword";
import ResetPasswordPage from "../pages/Authentication/ResetPassword";
import Logout from "../pages/Authentication/Logout";
import Register from "../pages/Authentication/Register";
import UserActivationMsg from "../pages/Authentication/UserActivation" 

import * as paths from "./Paths" 

// User Profile
import UserProfile from "../pages/Authentication/user-profile"; 
import LLM from "../pages/LLmMocker";

const LandingPath = paths.PathDashboard

const authProtectedRoutes = [
  { path: paths.PathDashboard, component: <Dashboard /> },
  { path: paths.PathIndex, component: <Dashboard /> },

  //User Profile
  // { path: paths.PathProfile, component: <UserProfile /> }, 
  
  // this route should be at the end of all other routes
  // eslint-disable-next-line react/display-name
  {
    path: "/",
    exact: true,
    component: <Navigate to={LandingPath} />,
  },
  
  { path: "*", component: <Navigate to={LandingPath} /> },
  { path: paths.LLM, component: <LLM /> }, 
  
];

const publicRoutes = [
  
  // Authentication Page
  { path: paths.PathLogout, component: <Logout /> },
  { path: paths.PathLogin, component: <Login /> },
  { path: paths.UserActivation+"/:token", component: <UserActivationMsg /> },
  { path: paths.ResetPassword+"/:token", component: <ResetPasswordPage /> },
  { path: paths.PathForgetPass, component: <ForgetPasswordPage /> },
  { path: paths.PathRegister, component: <Register /> }, 
  
];

export { authProtectedRoutes, publicRoutes };
