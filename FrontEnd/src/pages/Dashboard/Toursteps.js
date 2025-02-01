import { useDispatch, useSelector } from "react-redux";
import {deactivateUserTour} from "../../store/actions";
const Steps = (tour_id)=>{ 
  const dispatch = useDispatch()
  const deActivateTour = (tour_id)=>{ 
    dispatch(deactivateUserTour(tour_id))
  } 
  return [
  // id:1
    {
      id: "intro",
      attachTo: {  on: "bottom" },
      beforeShowPromise: function () {
        return new Promise(function (resolve) {
          setTimeout(function () {
            window.scrollTo(0, 0);
            resolve();
          }, 500);
        });
      },
      buttons: [
        {
          classes: "btn btn-success",
          text: "Next",
          action() {
            return this.next();
          },
        },
      ],
      title: "Welcome Back !",
      text:  "In order to use LLMs, you need to first create project profile. Then you can activate modules in project profile. To start, all free plans are activated.",
    },
  
    {
      id: "intro1",
      attachTo: { element: "#register-tour", on: "bottom" },
  
      buttons: [
        {
          text: "Back",
          classes: "btn btn-light",
          action() {
            return this.back();
          },
        },
        {
          text: "Next",
          classes: "btn btn-success",
          action() {
            return this.next();
          },
        },
      ],
      title: "Create project profile",
      text: "To create a new profile, you can use this button.",
    },
    // {
    //   id: "intro2",
    //   attachTo: { element: "#Softwares", on: "bottom" },
  
    //   buttons: [
    //     {
    //       text: "Back",
    //       classes: "btn btn-light",
    //       action() {
    //         return this.back();
    //       },
    //     },
    //     {
    //       text: "Next",
    //       classes: "btn btn-success",
    //       action() {
    //         return this.next();
    //       },
    //     },
    //   ],
    //   title: "More Profiles",
    //   text: "As a free plan, you have access to a project profile for a month. To be able to have more profiles, you need to purchase profiles from this tab.",
    // },
    {
      id: "intro3",
      attachTo: {   on: "bottom" },
      buttons: [
        {
          text: "Back",
          classes: "btn btn-light",
          action() {
            return this.back();
          },
        },
        {
          text: "Thank you and don't show this anymore!",
          classes: "btn btn-primary",
          action() {
            deActivateTour(tour_id) 
            return this.complete();
          },
        } 
      ],
      title: "Thank you !",
      text: "Then, you can find your projects here. By default you can have a free project profile for three months, from the time you make it.",
    },
  ]}
  
  export default Steps
  