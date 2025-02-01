import PropTypes from "prop-types";
import React, { useEffect } from "react";
import { Row, Col, Alert, Card, CardBody, Container, FormFeedback, Input, Label, Form, Button, Spinner } from "reactstrap";

//redux
import { useSelector, useDispatch } from "react-redux";

import { Link, useParams } from "react-router-dom";

import {AppPublicName} from "../../GlobalVars"

// Formik Validation
import * as Yup from "yup";
import { useFormik } from "formik";

// action
import { patchResetPassword, userForgetPassword } from "../../store/actions";

// import images
// import profile from "../../assets/images/bg.png";
import logoLight from "../../assets/images/logo-sm.png";
import ParticlesAuth from "../AuthenticationInner/ParticlesAuth";
import withRouter from "../../Components/Common/withRouter";
import {updatePassword } from "../../store/actions";

const ResetPasswordPage = props => {
  const dispatch = useDispatch();
  const params = useParams()
  const token = params.token

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
      dispatch(patchResetPassword(token, values.password));
    }
  });

  const { Error, SuccessMsg, resettingPassword } = useSelector(state => ({
    Error: state.ForgetPassword.Error,
    SuccessMsg: state.ForgetPassword.SuccessMsg,
    resettingPassword: state.ForgetPassword.resettingPassword
  })); 
document.title="Reset Password | " + AppPublicName;

  return (
    <ParticlesAuth>
      <div className="auth-page-content">
        <Container>
          <Row>
            <Col lg={12}>
              <div className="text-center mt-sm-5 mb-4 text-white-50">
                <div>
                  <Link to="/" className="d-inline-block auth-logo">
                    <img src={logoLight} alt="" height="20" />
                  </Link>
                </div>
                <p className="mt-3 fs-15 fw-medium">Simplifying Decision Making </p>
              </div>
            </Col>
          </Row>

          <Row className="justify-content-center">
            <Col md={8} lg={6} xl={5}>
              <Card className="mt-4">

                <CardBody className="p-4">
                {Error && Error ? (
                      <Alert color="danger" style={{ marginTop: "13px" }}>
                        {Error}
                      </Alert>
                    ) : null}
                    {SuccessMsg ? (
                      <Alert color="success" style={{ marginTop: "13px" }}>
                        {SuccessMsg}
                      </Alert>
                    ) : null}
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
                    <span>Update Password </span>
                    {
                      resettingPassword?<Spinner size="sm"></Spinner>:null
                    }
                  </Button>
                  <p>
                    or
                  </p>
                  <Link to="/forgot-password" className="fw-semibold text-primary text-decoration-underline"> Reset Again </Link>
                </div>
              </Form> 
                </CardBody>
              </Card>

              <div className="mt-4 text-center">
                <p className="mb-0">Wait, I remember my password... <Link to="/login" className="fw-semibold text-primary text-decoration-underline"> Click here </Link> </p>
              </div>

            </Col>
          </Row>
        </Container>
      </div>
    </ParticlesAuth>
  );
};
 

export default ResetPasswordPage;
