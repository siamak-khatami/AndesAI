import React from 'react';
import { Container, Row } from "reactstrap";
import BreadCrumb from "../../Components/Common/BreadCrumb";
import { AppPublicName } from '../../GlobalVars';

    const LLM = () => {
        document.title = "LLM | " + AppPublicName;   //for meta title
        return (
            <>
                <div className="page-content">
                    <Container fluid={true}>
                    <BreadCrumb title="LLM" pageTitle="LLM" />
                    </Container>
                    <Row>
                    </Row>
                </div>
            </>
        );
    }

export default LLM;