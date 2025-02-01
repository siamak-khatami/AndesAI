// gtm.js
import TagManager from "react-gtm-module";
import ReactGA from "react-ga4";
const gtmId = " "; // Replace with your GTM ID
const g4ID = " "; // Replace with your GTM ID

export const initializeTagManager = () => {
  TagManager.initialize({ gtmId });
};
 