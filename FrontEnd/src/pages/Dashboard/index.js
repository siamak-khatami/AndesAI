import React, {useContext, useEffect, useRef, useState} from "react";
import { Container, Row, Col, Button, FormGroup, Input, Label } from "reactstrap";
import BreadCrumb from "../../Components/Common/BreadCrumb"; 
import { Link, useNavigate } from 'react-router-dom';
import * as path from "../../Routes/Paths"
import { useDispatch, useSelector } from "react-redux";

import { ShepherdTour, ShepherdTourContext } from 'react-shepherd';
import {deactivateUserTour, getUserDeactivatedTours, getLLMModels} from "../../store/actions";
import NewSteps from './Toursteps'; 
import { AppPublicName } from "../../GlobalVars";

// When they enter the page, they can make upto 3 projects with alpha access. 
// then if they update others they can get more

// to update a project profile they need to go and select a payment option for their project profile. 
// Then when they activate it, their project activated_till will be updated as well.
const tourOptions = {
    defaultStepOptions: {
        cancelIcon: {
            enabled: true
        },
        classes: 'shadow-md bg-purple-dark',
        scrollTo: { behavior: "smooth", block: "center" },
    },
    useModalOverlay: true
};

function Autton() {
    const tour = useContext(ShepherdTourContext);
    useEffect(() => {
        tour.start();
    }, [tour]);
    return (<> </>);
  }
  
const Dashboard = () => {
  const dispatch = useDispatch()
  useEffect(()=>{
    dispatch(getUserDeactivatedTours())
    dispatch(getLLMModels())
  },[]) 
  const { error, userTours, toursLoaded, llmModels } = useSelector(state => ({
    error: state.Dashboard.error, 
    userTours: state.Dashboard.userTours,
    toursLoaded: state.Dashboard.toursLoaded,
    llmModels: state.LLM.llmModels
  }));
  document.title =" Dashboard | " + AppPublicName;
  const navigate = useNavigate() 
  
  const renderLLMList =(llmList)=>{
    return llmList.map((v, i)=>{ 
      return <option key={i} defaultValue={v}>{v}</option>
    })
  }
  const [llmOptions, setLLMOptions] = useState({})
  const tour_id = 1
  const [selectedLLM, setSelectedLLM] = useState(null)
  useEffect(()=>{
    if(llmModels!=undefined && Object.keys(llmModels).length>0){
      setLLMOptions(pre=>renderLLMList(llmModels)) 
    }
  }, [llmModels])
  
  const changeLLM = (e)=>{
    setSelectedLLM(pre=>e.target.value)
    setChatHistory(pre=>[])
  }
  const SelectLLM = ()=>{

  }

  const [chatHistory, setChatHistory] = useState([])

  const renderChatHistory = ()=>{
    if(chatHistory.length>0){
      return chatHistory.map((v, i)=>{
        return <>
          <div key={i}>
            {v}
          </div>
        </>
      })
    }else{
      return "No Chat History"
    }
  }
  const [chatInputText, setChatInputText] = useState()
  const ChatInput = (e) =>{
    setChatInputText(e.target.value)
  }
  const doChat = (e)=>{
    if(chatInputText!=""&& chatInputText!=undefined&& chatInputText!=null){
      // dispatch(postChat(chatInputText))
      if(selectedLLM!=undefined&&selectedLLM!=null && selectedLLM!="Choose..."){
        console.log(chatInputText, selectedLLM, chatHistory)
      }else{
        console.log("No LLM detected")
      }
      
    }
  }
  const s = useRef(NewSteps(tour_id)) // It is called every time state var is updated, so to prevent this, we hold it in a ref
  const renderTour = ()=>{
    return (
      <ShepherdTour steps={s.current} tourOptions={tourOptions} >
          <Autton />
      </ShepherdTour>
    )
  }
  
  return (
    <React.Fragment>  
      <div className="page-content">
        <Container fluid>
          {/* {toursLoaded?userTours.includes(tour_id)?null:renderTour():null}  */}
            {/* <BreadCrumb title="LLM Usage" breadcrumbItem="Projects" /> */}
            <Row id="logo-tour">
            <Col lg={12}>
              <div className="mb-3 d-flex justify-content-center text-center" >  
                <Col xxl={5} md={5} className="align-self-center">
                  <div className="input-group">
                      <Label className="input-group-text" htmlFor="inputGroupSelect01">Select an LLM</Label>
                      <select className="form-select" id="inputGroupSelect01" onChange={changeLLM}>
                          <option key={100} >Choose...</option>
                          {
                            Object.keys(llmOptions).length>0?llmOptions:null
                          }
                      </select>
                      <Button onClick={SelectLLM}>Click to select</Button>
                  </div>
                </Col>
                </div>
              </Col>
              <Col lg={12}>
                <div className="mb-3 d-flex justify-content-center" >  
                  <Col xxl={8} md={8} className="">
                   {renderChatHistory()}
                  </Col>
                </div>
              </Col>
              <Col lg={12} className="">
                <div className="mb-3 d-flex justify-content-center text-center" >  
                  <Col xxl={5} md={5} className="align-self-center">
                      <div>
                          <FormGroup floating>
                              <Input
                                  id="ChatBox"
                                  name="ChatBox"
                                  placeholder="Chat Here"
                                  type="textarea" 
                                  onChange={ChatInput}
                                  style={{height:"100px", resize:"none"}}
                              /> 
                              <Button
                              color="primary"
                              className="btn-icon"
                              style={{position:"absolute", right:"5px", bottom:"5px"}}
                              onClick={doChat}
                              >
                                <i className="ri-send-plane-2-fill"/> 
                              </Button>
                              <Label for="Chat">
                                  Chat Here
                              </Label>
                          </FormGroup>
                      </div>
                  </Col>
                </div>
              </Col>
            </Row>
            <Row> 
            </Row> 
        </Container>
      </div>
    </React.Fragment>
  );
};

export default Dashboard;
