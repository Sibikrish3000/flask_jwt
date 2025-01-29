import React from "react";
import { Link, useNavigate } from "react-router-dom";

function NavBar() {
  const navigate = useNavigate();

  const handleLogout = () => {
  if (window.confirm("Are you sure you want to log out?")) {
    localStorage.removeItem("token");
    navigate("/login");
  }
};


  return (
    <nav style={{ display: "flex", justifyContent: "space-between", padding: "10px", borderBottom: "1px solid #ccc" }}>
      <div>
        <Link to="/dashboard" style={{ marginRight: "10px" }}>Dashboard</Link>
        <Link to="/other">Other Page</Link>
      </div>
      <button onClick={handleLogout} style={{ marginLeft: "auto" }}>
        Logout
      </button>
    </nav>
  );
}

export default NavBar;
