import React from 'react';
import { Col, Container, Row } from 'reactstrap';
import LiveChat from './Hubspot';

const Footer = () => {
    return (
        <React.Fragment>
            <LiveChat />
            <footer className="footer">
                <Container fluid>
                    <Row>
                        <Col sm={6}>
                            {new Date().getFullYear()} © Example.
                        </Col>
                        <Col sm={6}>
                            <div className="text-sm-end d-none d-sm-block">
                                LLM Based Conversational AI
                            </div>
                        </Col>
                    </Row>
                </Container>
            </footer>
            
        </React.Fragment>
    );
};

export default Footer;