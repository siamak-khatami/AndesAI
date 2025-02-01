const localBackEndPort = "8000"
const LocalServerBackend = "http://localhost:" + localBackEndPort
const TestServer = ""
const ProductionBackendServer = ""
const productionFrontEndHostName = "webapp.example.com"
const TestUserInTestServer  = ""
const TestUserPassInTestServer  = ""
const TestUserInProductionServer  = ""
const TestUserPassInProductionServer  = ""
// setup for the test api on local machines
const apiTest = ()=>{
  return {
    api: {
    API_URL: LocalServerBackend,
    TestUser: TestUserInTestServer,
    TestUserPass:TestUserPassInTestServer
    }
  }
}
// setup for the production api on the server
const apiProduction = ()=>{
  return {
    api: {
    API_URL: ProductionBackendServer,
    TestUser: "",
    TestUserPass:""
    }
  }
}

const isProduction = window.location.hostname == productionFrontEndHostName
// if the current running hostname is the production hostname, then connect to the backend server, else connect to the local server.
module.exports = isProduction?apiProduction():apiTest()
