import React, { useState, useEffect } from "react";
import { ToastContainer, toast } from 'react-toastify';
import { isEmpty } from "lodash";

import {
  Container,
  Row,
  Col,
  Card,
  Alert,
  CardBody,
  Button,
  Label,
  Input,
  FormFeedback,
  Form,
} from "reactstrap";

// Formik Validation
import * as Yup from "yup";
import { useFormik } from "formik";
import {AppPublicName} from "../../GlobalVars"
//redux
import { useSelector, useDispatch } from "react-redux";

import avatar from "../../assets/images/users/user-dummy-img.jpg";
// actions
import { editProfile, resetProfileFlag, updatePassword } from "../../store/actions";

const UserProfile = () => {
  const dispatch = useDispatch();
  const us = JSON.parse(localStorage.getItem("authUser")).user 
  const [email, setemail] = useState(us.email); 

  const [firstName, setFirstName] = useState(us.first_name + " " + us.last_name);

  const { user, success, error, updatingPass, passUpdateSuccess} = useSelector(state => ({
    user: state.Profile.user,
    success: state.Profile.success,
    error: state.Profile.error,
    updatingPass: state.Profile.updatingPass,
    passUpdateSuccess: state.Profile.passUpdateSuccess, 
  })); 
  const PassUpdateMsg = ()=>{
    if(!updatingPass){
      let Msg = ""
      let colorCls = ""
      if(passUpdateSuccess){
        Msg = "Password has been updated"
        colorCls = "bg-success"
        return toast(Msg, { 
          position: "top-center",
          autoClose: 2000,
          // autoClose:true,
          hideProgressBar: false,
          closeOnClick: false,
          className: colorCls + ' text-white' });
      }
      if( Object.values(error).length !== 0){ 
        Msg = error.data
        colorCls = "bg-danger"
        return toast(Msg, { 
          position: "top-center",
          autoClose: 2000,
          // autoClose:true,
          hideProgressBar: false,
          closeOnClick: false,
          className: colorCls + ' text-white' });
      }
      
    }
  }
  const validation = useFormik({
    // enableReinitialize : use this flag when initial values needs to be changed
    enableReinitialize: true,

    initialValues: {
      password: '', 
      confirm_password: '', 
    },
    validationSchema: Yup.object({
      password: Yup.string().min(6, 'Password must be at least 6 characters').required('Please Enter Your Password'),
      confirm_password: Yup.string().oneOf([Yup.ref('password'), null], 'Passwords must match').required('Please re-enter your password.')
    }),
    onSubmit: (values) => {
      // When the profile is edited, the current version edits the SessionStorage,
      // we want to send it to the server and get it from there.  
      delete values["confirm_password"]
      dispatch(updatePassword(values));
    }
  });

  useEffect(()=>{
    PassUpdateMsg()
  }, [updatingPass, passUpdateSuccess])
  

  document.title = "Profile | " + AppPublicName;
  return (
    <React.Fragment>
      <ToastContainer />
      <div className="page-content">
        <Container fluid>
          <Row>
            <Col lg="12">
              {/* {error && error ? <Alert color="danger">{error}</Alert> : null} */}
              {/* {success ? <Alert color="success">Username Updated To {firstName}</Alert> : null} */}

              <Card>
                <CardBody>
                  <div className="d-flex">
                    <div className="mx-3">
                      <img
                        src={avatar}
                        alt=""
                        className="avatar-md rounded-circle img-thumbnail"
                      />
                    </div>
                    <div className="flex-grow-1 align-self-center">
                      <div className="text-muted">
                        <h5>{firstName  }</h5>
                        <p className="mb-1">Email: {email}</p>
                        {/* <p className="mb-0">Id No : #{idx}</p> */}
                      </div>
                    </div>
                  </div>
                </CardBody>
              </Card>
            </Col>
          </Row>

          <h4 className="card-title mb-4">Change Password</h4>

          <Card>
            <CardBody>
              <Form
                className="form-horizontal"
                onSubmit={(e) => { 
                  validation.handleSubmit(); 
                  e.preventDefault(); 
                  return false;
                }}
                action="#"
              >
                <div className="form-group">
                  <Label className="form-label">New Password</Label>
                  <Input
                    name="password"
                    // value={name}
                    className="form-control"
                    placeholder="Enter Password"
                    type="password"
                    onChange={validation.handleChange}
                    onBlur={validation.handleBlur}
                    value={validation.values.password || ""}
                    invalid={
                      validation.touched.password && validation.errors.password ? true : false
                    }
                  />
                  {validation.touched.password && validation.errors.password ? (
                    <FormFeedback type="invalid">{validation.errors.password}</FormFeedback>
                  ) : null} 
                </div>
                <div className="form-group mt-3">
                  <Label className="form-label">Confirm Password</Label>
                  <Input
                    name="confirm_password"
                    // value={name}
                    className="form-control"
                    placeholder="Re Enter Password"
                    type="password"
                    onChange={validation.handleChange}
                    onBlur={validation.handleBlur}
                    value={validation.values.confirm_password || ""}
                    invalid={
                      validation.touched.confirm_password && validation.errors.confirm_password ? true : false
                    }
                  />
                  {validation.touched.confirm_password && validation.errors.confirm_password ? (
                    <FormFeedback type="invalid">{validation.errors.confirm_password}</FormFeedback>
                  ) : null} 
                </div>
                <div className="text-center mt-4">
                  <Button type="submit" color="danger">
                    Update Password
                  </Button>
                </div>
              </Form>
            </CardBody>
          </Card>
        </Container>
      </div>
    </React.Fragment>
  );
};

export default UserProfile;
