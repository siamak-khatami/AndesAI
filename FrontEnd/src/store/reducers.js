import { combineReducers } from "redux";


/// Zeta 


import Dashboard from "./dashboard/reducer"; 

// Front
import Layout from "./layouts/reducer";

// Authentication
import Login from "./auth/login/reducer";
import Account from "./auth/register/reducer";
import ForgetPassword from "./auth/forgetpwd/reducer";
import Profile from "./auth/profile/reducer";

//Calendar
import Calendar from "./calendar/reducer";
//Chat
import chat from "./chat/reducer";
//Ecommerce
import Ecommerce from "./ecommerce/reducer";
 

// Tasks
import Tasks from "./tasks/reducer";
//Form advanced
import changeNumber from "./formAdvanced/reducer";

//Crypto
import Crypto from "./crypto/reducer";

//TicketsList
import Tickets from "./tickets/reducer";
//Crm
import Crm from "./crm/reducer";
 

//Mailbox
import Mailbox from "./mailbox/reducer";

// Dashboard Analytics
import DashboardAnalytics from "./dashboardAnalytics/reducer";



// Pages > Team
import Team from "./team/reducer";

// File Manager
import FileManager from "./fileManager/reducer";

// To do
import Todos from "./todos/reducer";
//Jobs
import Jobs from "./job/reducer";
//API Key
import APIKey from "./apikey/reducer";
import LLM from "./LLM/reducer";
const rootReducer = combineReducers({
  // public 
  Layout,
  Login,
  Account,
  ForgetPassword,
  Profile,
  Calendar,
  chat, 
  Ecommerce,
  Tasks,
  changeNumber,
  Crypto,
  Tickets,
  Crm, 
  Mailbox,
  Dashboard,
  DashboardAnalytics,
  Team,
  FileManager,
  Todos,
  Jobs,
  APIKey,
  LLM
});

export default rootReducer;
