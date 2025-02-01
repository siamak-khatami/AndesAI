import React, {useEffect, useState} from 'react';
import { Link, useParams } from 'react-router-dom';
import { useSelector, useDispatch,  } from "react-redux";
import { Card, CardBody, Col, Container, Row, SpinnerInput, Input, Label,Button, Form, FormFeedback, Alert, Spinner } from 'reactstrap';  
//import images
import logoLight from "../../assets/images/logo-sm.png";
import {requestUserActivation, requestUserReActivation} from "../../store/actions";
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
// Formik validation
import * as Yup from "yup";
import { AppPublicName } from '../../GlobalVars';
import { useFormik } from "formik";
// When they enter to the page
// 1. Send a activation request to the server with token in the header and put the loading on True.

// 2. If you get the status 200 then show the success.
// 3. If you get the error and not a 200 then show the failure.

const ParticlesAuth = ({ children }) => {
    
    return (
        <React.Fragment>
            <div className="auth-page-wrapper pt-5">
                <div className="auth-one-bg-position auth-one-bg" id="auth-particles">

                    <div className="bg-overlay"></div>

                    <div className="shape">
                        <svg xmlns="http://www.w3.org/2000/svg" version="1.1" xmlnsXlink="http://www.w3.org/1999/xlink" viewBox="0 0 1440 120">
                            <path d="M 0,36 C 144,53.6 432,123.2 720,124 C 1008,124.8 1296,56.8 1440,40L1440 140L0 140z"></path>
                        </svg>
                    </div>
                </div>

                {/* pass the children */}
                {children}

                <footer className="footer">
                    <div className="container">
                        <div className="row">
                            <div className="col-lg-12">
                                <div className="text-center">
                                    <p className="mb-0 text-muted"> © {new Date().getFullYear()} Zeta Resolution. </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </footer>
            </div>
        </React.Fragment>
    );
};

const loading = ()=>{
    return (
        <CardBody className="p-4 text-center"> 
            <Col lg={12} className="d-flex justify-content-center pt-5">
                <Spinner color="primary" className="align-self-center"></Spinner>
            </Col>
        </CardBody>
    
    )
}

const successRender = ()=>{
    return (
        <CardBody className="p-4 text-center">
            <div className="avatar-lg mx-auto mt-2">
                <div className="avatar-title bg-light text-success display-3 rounded-circle">
                    <i className="ri-checkbox-circle-fill"></i>
                </div>
            </div>
            <div className="mt-4 pt-2">
                <h4>Well done !</h4>
                <p className="text-muted mx-4">Your account has been activated successfully.</p>
                <div className="mt-4">
                    <Link to="/login" className="btn btn-success w-100">Go to Login</Link>
                </div>
            </div>
        </CardBody>
    )
}


const failureRender = (StateCaller, error)=>{ 
    const setResendEmailFunc = ()=>{ 
        return StateCaller(pre=>true)
    }
    return (
        <CardBody className="p-4 text-center">
            
            <div className="avatar-lg mx-auto mt-2">
                <div className="avatar-title bg-light text-danger display-3 rounded-circle">
                    <i className="ri-close-circle-fill"></i>
                </div>
            </div>
            <div className="mt-4 pt-2">
                <h4>Unfortunately we could not activate your account! </h4>
                <p className="text-muted mx-4">Please re-activate your account.</p>

                {error.error_id==64?(<div className="mt-4 text-center">
                                    <p className="mb-0">Already activated ? <Link to="/login" className="fw-semibold text-primary text-decoration-underline"> Signin </Link> </p>
                                </div>):(<div className="mt-4">
                    <Button onClick={setResendEmailFunc} className="btn btn-success w-100">Request New Activation!</Button>
                </div>)}
            </div>
        </CardBody>
    )
}   

const ResendEmailForm = (email, setEmail, setPatchEmail) => { 
    const dispatch = useDispatch()
    const changeEmail = (e)=>{ 
        setEmail(e.target.value)
    }
    const patchMail = (e)=>{
       //  setPatchEmail(true)
       dispatch(requestUserReActivation(email))
    }
    return ( 
            <CardBody className="p-4  text-center">
                <div className="text-center mt-2">
                    <h5 className="text-primary">Welcome!</h5>
                    <p className="text-muted">Please enter registered email to send another activation link.</p>
                </div> 
                <div className="p-2 mt-4">
                    <Form 
                    action='/#'
                    onSubmit={(e)=>{
                        e.preventDefault();
                        patchMail()
                    }}
                    >

                        <div className="mb-3">
                            <Label htmlFor="email" className="form-label">Email</Label>
                            <Input
                                name="email"
                                className="form-control"
                                placeholder="Enter email"
                                type="email" 
                                onChange={changeEmail}
                                required
                            /> 
                        </div>

                        <div className="mt-4">
                            <Button color="success" className="btn btn-success w-100" type="submit" > 
                                Resend Email
                            </Button>
                        </div>

                    </Form>
                </div>
                <div className="mt-4 text-center">
                                    <p className="mb-0">Already activated ? <Link to="/login" className="fw-semibold text-primary text-decoration-underline"> Signin </Link> </p>
                                </div>
            </CardBody> 
    );
}; 

const UserActivationMsg = (props) => {
    const params = useParams()
    const dispatch = useDispatch();
    const { userActivated, error, loadingActivation, userReActivation  } = useSelector(state => ({
        userActivated: state.Account.userActivated,
        error: state.Account.err,
        loadingActivation: state.Account.loadingActivation,
        userReActivation: state.Account.userReActivation
    }));
    const [resendEmail, setResendEmail] = useState(false)
    const [email, setEmail] = useState("")
    const [patchEmail, setPatchEmail] = useState(false)
    useEffect(()=>{ 
        dispatch(requestUserActivation(params.token))
    },[])   
document.title="User Activation | " + AppPublicName;
    return (
        <React.Fragment>
            <div className="auth-page-wrapper">
                <ParticlesAuth>
                    <div className="auth-page-content">
                        <Container>
                            <Row>
                                <Col lg={12}>
                                    <div className="text-center mt-sm-5 mb-4 text-white-50">
                                        <div>
                                            <Link to="/dashboard" className="d-inline-block auth-logo">
                                                <img src={logoLight} alt="" height="20" />
                                            </Link>
                                        </div>
                                        <p className="mt-3 fs-15 fw-medium">User Activation</p>
                                    </div>
                                </Col>
                            </Row>

                            <Row className="justify-content-center">
                                <Col md={8} lg={6} xl={5}>
                                    <Card className="mt-4">
                                    {userReActivation && userReActivation ? (
                                                    <>
                                                        <Alert color="success" className='text-center '>
                                                            A new activation email has been sent.
                                                        </Alert>
                                                    </>
                                                ) : Object.keys(error).length>0? (
                                                    <>
                                                        <Alert color="danger" className='text-center '>
                                                            {error.data}
                                                        </Alert>
                                                    </>
                                                ):null}
                                        {
                                            resendEmail?ResendEmailForm(email, setEmail, setPatchEmail):loadingActivation?loading():Object.keys(error).length>0?failureRender(setResendEmail, error):successRender()
                                        }
                                        
                                    </Card>
                                </Col>
                            </Row>
                        </Container>
                    </div>
                </ParticlesAuth>
            </div>
        </React.Fragment >
    );
};

export default UserActivationMsg;