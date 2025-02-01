import React, { useEffect } from "react";
import { Navigate, Route, useNavigate } from "react-router-dom";
import {setAuthorization} from "../helpers/api_helper";
import { useDispatch, useSelector } from "react-redux";

import { useProfile } from "../Components/Hooks/UserHooks";

import { logoutUser, validateAuthentication, profileSuccess } from "../store/actions";

import {PathLogin} from "../Routes/Paths"

const AuthProtected = (props) => {
  const dispatch = useDispatch();
  const { userProfile, loading, token } = useProfile();
  const navigate = useNavigate();
  // console.log(userProfile, loading, token)
  
  const { isUserLogout } = useSelector((state) => ({
        isUserLogout: state.Login.isUserLogout,
    }));
  useEffect(()=>{
      dispatch(validateAuthentication()) // There are many reasons in which a token might be not valid
      // After validating, if it is valid, then user info should be set
    },[])
  useEffect(() => {
    if (userProfile && !loading && token) {
      setAuthorization(token);
      // dispatch(validateAuthentication()) // There are many reasons in which a token might be not valid
      // TODO: we need to clear localstoragte at every chrome closing attempt.
    } else if (!userProfile && loading && !token) {
      dispatch(logoutUser());
      // navigate('/login')
    }
  }, [token, userProfile, loading, dispatch]);
  
  useEffect(()=>{
    if(isUserLogout){
      navigate(PathLogin)
    }
  },[isUserLogout])
  /*
    Navigate is un-auth access protected routes via url
    */

  if (!userProfile && loading && !token) {
    return (
      <Navigate to={{ pathname: PathLogin, state: { from: props.location } }} />
    );
  }

  return <>{props.children}</>;
};

const AccessRoute = ({ component: Component, ...rest }) => {
  return (
    <Route
      {...rest}
      render={props => {
        return (<> <Component {...props} /> </>);
      }}
    />
  );
};

export { AuthProtected, AccessRoute };