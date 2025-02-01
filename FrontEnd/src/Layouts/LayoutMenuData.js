import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import * as path from "../Routes/Paths"

const Navdata = () => {
  const history = useNavigate();
  //state data
  const [isDashboard, setIsDashboard] = useState(false);
  const [isSoftware, setIsSoftware] = useState(false);
  const [isBPProjectMetaData, setisBPProjectMetaData] = useState(false);

  const [iscurrentState, setIscurrentState] = useState("Dashboard");

  function updateIconSidebar(e) {
    if (e && e.target && e.target.getAttribute("subitems")) {
      const ul = document.getElementById("two-column-menu");
      const iconItems = ul.querySelectorAll(".nav-icon.active");
      let activeIconItems = [...iconItems];
      activeIconItems.forEach((item) => {
        item.classList.remove("active");
        var id = item.getAttribute("subitems");
        if (document.getElementById(id))
          document.getElementById(id).classList.remove("show");
      });
    }
  }

  useEffect(() => {
    document.body.classList.remove("twocolumn-panel");
    if (iscurrentState !== "Dashboard") {
      history(path.PathDashboard);
      setIsDashboard(false);
    }
    if (iscurrentState === "Softwares") {
      // history(path.Pathsoftwares);
      document.body.classList.add("twocolumn-panel");
    }
  }, [
    history,
    iscurrentState,
    isDashboard,
    isSoftware
  ]);

  const menuItems = [
    {
      label: "Menu",
      isHeader: true,
    },
    {
      id: "dashboard",
      label: "Dashboard",
      icon: "bx bxs-dashboard",
      link: path.PathDashboard,
      stateVariables: isDashboard,
      click: function (e) {
        e.preventDefault();
        setIscurrentState("Dashboard");
      }
    },
    // {
    //   id: "dashboard",
    //   label: "Dashboard",
    //   icon: "bx bxs-dashboard",
    //   link: path.PathDashboard,
    //   stateVariables: isDashboard,
    //   click: function (e) {
    //     e.preventDefault();
    //     setIscurrentState("Dashboard");
    //   }
    // },
    // {
    //   id: "Softwares",
    //   label: "Products and Modules",
    //   icon: "bx bxs-layer",
    //   link: path.Pathsoftwares,
    //   stateVariables: isSoftware,
    //   click: function (e) {
    //     e.preventDefault();
    //     //setIsSoftware(!isSoftware)
    //     setIscurrentState("Softwares");
    //     //updateIconSidebar(e)
    //   }
    // }
  ];
  return <React.Fragment>{menuItems}</React.Fragment>;
};
export default Navdata;
