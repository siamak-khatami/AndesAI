import { all, fork } from "redux-saga/effects";
/// Zeta

// Dashboard
import dashboardSaga from "./dashboard/saga"; 

//layout
import LayoutSaga from "./layouts/saga";
//Auth
import AccountSaga from "./auth/register/saga";
import AuthSaga from "./auth/login/saga";
import ForgetSaga from "./auth/forgetpwd/saga";
import ProfileSaga from "./auth/profile/saga";

//calendar
import calendarSaga from "./calendar/saga";
//chat
import chatSaga from "./chat/saga";
//ecommerce
import ecommerceSaga from "./ecommerce/saga";
 
// Task
import taskSaga from "./tasks/saga";
// Crypto
import cryptoSaga from "./crypto/saga";
//TicketsList
import ticketsSaga from "./tickets/saga";

//crm
import crmSaga from "./crm/saga"; 
//mailbox
import mailboxSaga from "./mailbox/saga";

// Dashboard Analytics
import dashboardAnalyticsSaga from "./dashboardAnalytics/saga";

// Pages > Team
import teamSaga from "./team/saga";

// File Manager
import fileManager from "./fileManager/saga";

// To do
import todos from "./todos/saga";
//Jobs
import ApplicationSaga from "./job/saga";
//API Key
import APIKeysaga from "./apikey/saga";
import llmSaga from "./LLM/saga";
export default function* rootSaga() {
  yield all([
    //public
    fork(LayoutSaga), 
    fork(AccountSaga),
    fork(AuthSaga),
    fork(ForgetSaga),
    fork(ProfileSaga),
    fork(chatSaga), 
    fork(taskSaga),
    fork(cryptoSaga),
    fork(ticketsSaga),
    fork(calendarSaga),
    fork(ecommerceSaga),
    fork(crmSaga), 
    fork(mailboxSaga),
    fork(dashboardAnalyticsSaga),
    fork(teamSaga),
    fork(fileManager),
    fork(todos),
    fork(ApplicationSaga),
    fork(APIKeysaga),
    fork(dashboardSaga),
    fork(llmSaga),
  ]);
}
