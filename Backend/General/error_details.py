from typing import Optional
from pydantic import BaseModel


class Msg(BaseModel):
    id: Optional[int]
    loc: Optional[list]
    msg: Optional[str]
    details: Optional[dict]


class ErrorDetails:
    PaymentNotFound = {"id": 80, "loc": ["body", "payment id"],
                       "msg": "No such a payment found."}
    CouldNotAddPayment = {"id": 79, "loc": ["body", "customer"],
                          "msg": "Could not add Stripe payment."}
    CouldNotAddStripeCustomer = {"id": 78, "loc": ["body", "customer"],
                                 "msg": "Could not add Stripe customer."}
    NoStripeCustomer = {"id": 77, "loc": ["body", "customer"],
                        "msg": "No Stripe customer found."}
    PaymentError = {"id": 76, "loc": ["body", "payment"],
                    "msg": "Payment intention failed."}
    CouldNotAddTeam = {"id": 75, "loc": ["body", "solutions"],
                       "msg": "Could not add the team."}
    TeamNotFound = {"id": 74, "loc": ["body", "solutions"],
                    "msg": "Could not find the team."}
    CouldNotAddSolution = {"id": 73, "loc": ["body", "solutions"],
                           "msg": "Could not add the solution."}
    SolutionExists = {"id": 72, "loc": ["body", "solutions"],
                      "msg": "Solution already added."}
    CouldNotDeleteAnalysis = {"id": 71, "loc": ["body", "solutions"],
                              "msg": "Couldn't delete analysis due to solution updates."}
    CouldNotEditSolution = {"id": 70, "loc": ["body", "solutions"],
                            "msg": "Couldn't edit the solution."}
    NoSuchSolution = {"id": 69, "loc": ["body", "solutions"],
                      "msg": "Couldn't find the solution."}
    CouldNotDisableTour = {"id": 68, "loc": ["body"],
                           "msg": "Could not disable the tour."}
    TourAlreadyDisabled = {"id": 67, "loc": ["body"],
                           "msg": "The tour already has been disabled."}
    Tour_Exists = {"id": 66, "loc": ["body", "email"], "msg": "Tour Exists!"}
    CouldNotActivateUser = {"id": 65, "loc": ["body"],
                            "msg": "Could Not activate the user."}
    ActivatedUser = {"id": 64, "loc": ["body"],
                     "msg": "User already has been activated."}
    CustomError = {"id": 63, "loc": ["body"],
                   "msg": ""}
    ActivateUser = {"id": 62, "loc": ["body"],
                    "msg": "Please first activate your user. Check your email for the link."}
    InValid_Token = {"id": 61, "loc": ["body"],
                     "msg": "The token is not valid."}
    CouldNotFindMarketAnalysisProgress = {"id": 60, "loc": ["body"],
                                          "msg": "Could not find the market size analysis progress."}
    WrongLogic = {"id": 59, "loc": ["body", "bp_project_id"],
                  "msg": "A wrong condition is happening."}
    ProgressProgressing = {"id": 58, "loc": ["body", "bp_project_id"],
                           "msg": "There is an ongoing progress for this project."}
    ProgressDone = {"id": 57, "loc": ["body", "bp_project_id"],
                    "msg": "Project progress is 100."}
    NLPImproperAnswer = {"id": 56, "loc": ["body", "project_name"],
                         "msg": "The AI System is overloaded."}
    NoAnalysisFound = {"id": 55, "loc": ["body", "bp_project_id"],
                       "msg": "Could not find an analysis."}
    CouldNotGetStats = {"id": 54, "loc": ["body"],
                        "msg": "Could not get stats."}
    CouldNotAddSts = {"id": 53, "loc": ["body"],
                      "msg": "Could not add {}."}
    CouldNotAddMarketAnalysisProgress = {"id": 52, "loc": ["body"],
                                         "msg": "Could not add a new market size analysis progress."}
    CouldNotAddMarketSizeAnalysis = {"id": 51, "loc": ["body"],
                                     "msg": "Could not add a new market size analysis ."}
    CouldNotDeleteActionZone = {"id": 50, "loc": ["body"],
                                "msg": "Could not delete the action zone."}
    ActionZoneExists = {"id": 49, "loc": ["body"],
                        "msg": "Action Zone Exists."}
    NoSuchCity = {"id": 48, "loc": ["body", "city_id"],
                  "msg": "Couldn't find the City. To add a city, country and province information is required."}
    NoSuchProvince = {"id": 47, "loc": ["body", "province_id"],
                      "msg": "Couldn't find the Province."}
    NoSuchCountry = {"id": 46, "loc": ["body", "solutions"],
                     "msg": "Couldn't find the country."}
    CouldNotAddBusinessCat = {"id": 45, "loc": ["body", "solutions"],
                              "msg": "Couldn't add the business category."}
    CouldNotAddComplementarySol = {"id": 45, "loc": ["body", "solutions"],
                                   "msg": "Couldn't add the complementary solution."}
    CouldNotAddCompetitor = {"id": 45, "loc": ["body", "solutions"],
                             "msg": "Couldn't add the competitor."}
    CouldNotAddTangibles = {"id": 45, "loc": ["body", "solutions"],
                            "msg": "Couldn't add the solutions."}
    NLPOutOfService = {"id": 44, "loc": ["body", "project_name"],
                       "msg": "The AI System is overloaded."}
    ProjectNameError = {"id": 43, "loc": ["body", "project_name"],
                        "msg": "Project name length error."}
    NoSuchATaskType = {"id": 42, "loc": ["body", "task_type"],
                       "msg": "Task type not implemented."}
    NoLocationInformation = {"id": 41, "loc": ["body", "location_ids"],
                             "msg": "Could not find any matched location."}
    CouldNotEditActionZone = {"id": 40, "loc": ["body"],
                              "msg": "Could not edit the Action Zone."}
    ActionZoneNotFound = {"id": 39, "loc": ["body"],
                          "msg": "Can not find the action zone."}
    CouldNotAddActionZone = {"id": 38, "loc": ["body"],
                             "msg": "Could not add the Action Zone."}
    CouldNotAddLocationInfo = {"id": 37, "loc": ["body", "google_location_info"],
                               "msg": "Could not add the location info."}
    CityNameRequired = {"id": 36, "loc": ["body", "city_name"],
                        "msg": "Please try to provide a country_name suggestion."}
    ProvinceInformationIsRequired = {"id": 35, "loc": ["body", "country_province_info"],
                                     "msg": "Please try to provide a country_name suggestion."}
    CountryRequired = {"id": 34, "loc": ["body", "country_id, alpha2"],
                       "msg": "If it is not a world wide action zone, a country is required."}
    ProblemStatementNotFound = {"id": 33, "loc": ["body", "problem_id"],
                                "msg": "Please try to provide a problem statement for us."}
    ProblemStatementCantDeleted = {"id": 32, "loc": ["body", "problem_id"],
                                   "msg": "A problem Statement Can Not be deleted. Only edit it."}
    ProjectCantDelete = {"id": 31, "loc": ["body", "project_id"],
                         "msg": "There are associations connected to the project."}
    NoSegmentProblemID = {"id": 30, "loc": ["body", "segment_id", "problem_id"],
                          "msg": "One of parameters should be provided."}
    SegmentNotFound = {"id": 29, "loc": ["body", "segment_id"],
                       "msg": "Segment Not Found."}
    CouldNotAddSeg = {"id": 28, "loc": ["body"],
                      "msg": "Could not be able to add segmentation."}
    zetaProductFeatureNotFound = {"id": 27, "loc": ["body", "feature_id"],
                                  "msg": "Feature not found, please make aa new one."}
    ProjectProbStatNotFound = {"id": 26, "loc": ["body", "project_id"], "msg": "There is no statement for this project."}
    CouldNotAddPS = {"id": 25, "loc": ["body"], "msg": "Something goes wrong."}
    ProjectHasProbStatement = {"id": 24, "loc": ["body", "project_id"],
                               "msg": "the project has a problem Statement. Try to edit that."}
    FeatureAccessDenied = {"id": 23, "loc": ["body", "feature_url"],
                           "msg": "Your active plan does not have access to this feature."}
    ZetaNoFeatureForPlan = {"id": 22, "loc": ["body", "plan_id"], "msg": "There is no features for the requested plan."}
    ZetaPlanFeatureBadRequest = {"id": 21, "loc": ["body", ""], "msg": "Bad relation request."}
    ZetaFeatureNotFound = {"id": 20, "loc": ["body", "feature_id"], "msg": "No feature found!"}
    ZetaPlanNotFound = {"id": 19, "loc": ["body", "plan_id"], "msg": "No plan found!"}
    FeaturePlanAttached = {"id": 18, "loc": ["body", "feature_id and plan_id"], "msg": "Plan already has the Feature."}
    ZetaProductFeatureNameExists = {"id": 17, "loc": ["body", "feature_name"], "msg": "Cannot create new feature. "
                                                                                      "feature name exists!"}
    CannotCreateNewBP = {"id": 16, "loc": ["body", "bp_project_id"], "msg": "Cannot create new business plan!"}
    BPProjectNotFound = {"id": 15, "loc": ["body", "bp_project_id"], "msg": "Project Not Found!"}
    PlanLimitationReached = {"id": 14, "msg": "Plan limitation has been reached! Try to either update the "
                                              "plan or delete other projects."}
    Email_Exists = {"id": 0, "loc": ["body", "email"], "msg": "Email Exists!"}
    Wrong_Credentials = {"id": 1, "loc": ["body", "email | password"],
                         "msg": "Invalid Credentials. Please check your email or password!"}
    Wrong_Email = {"id": 2, "loc": ["body", "email"], "msg": "Sorry, We couldn't find a user with this email!"}
    User_Not_Found = {"id": 3, "loc": ["body", "email"], "msg": "User not found!"}
    Token_access = {"id": 4, "loc": ["body", "email"], "msg": "Access expired!"}
    Admin_User_Done = {"id": 5, "loc": ["body", "admin"], "msg": "Done!"}
    ProductExists = {"id": 6, "loc": ["body", "product_name"], "msg": "Product exists!"}
    ProductNotExists = {"id": 7, "loc": ["body", "product_name"], "msg": "Product does not exists!"}
    PlanNotExists = {"id": 8, "loc": ["body", "plan_id"], "msg": "Plan does not exists!"}
    SubExists = {
        "id": 9,
        "loc": ["body", "product_id"],
        "msg": "A Subscription for the user and product exists!"
               "Please try to upgrade/downgrade the available one.",
        "details": {
            "active_product": 0,
            "active_plan": 0
        }}
    SubNotExists = {"id": 10, "loc": ["body", "plan_id"],
                    "msg": "There is no subscription for the requested user and plan!"}
    SubExistsActive = {"id": 11, "loc": ["body", "plan_id"],
                       "msg": "The plan for the user is already registered and activated!"}
    SubExistsDeactivated = {"id": 12, "loc": ["body", "plan_id"],
                            "msg": "There is a deactivated subscription for the requested user and  plan! "
                                   "Please try to activate it."}
    NoActiveSub = {"id": 13,
                   "msg": "There is no active subscription for the user and requested product!"
                          "Please activate/subscribe to a product."}
