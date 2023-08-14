import React,{useEffect, useState} from "react";
import {
  BrowserRouter as Router,
  Route,
  Routes
} from "react-router-dom";
import Dashboard from "./components/Dashboard";
import Login from "./components/Login";
import Footer from "./components/pages/Footer";
import Navigation from "./components/pages/Navigation";
import PageNotFound from "./components/pages/PageNotFound";
import Register from "./components/Register";
import Home from "./Home";
function App() {
  console.log("localStorage.token", localStorage.token);
  const [searchClick, setSearchClick] = useState(false)
  
  const handleSearch = () => {
    console.log("click me");
    setSearchClick(true)
  }

  return (
    <Router>
      <div className="container-fluid for_sub_menu" >
        <Navigation searchClick={searchClick} setSearchClick ={setSearchClick} handleSearch={handleSearch} />
        <div onClick={()=> setSearchClick(false)}>
        <Routes>
          <Route exact path="/register" element={<Register />} />
          <Route exact path="/login" element={<Login />} />
          <Route exact path="/" element={<Home />} />
          <Route exact path="/dashboard" element={<Dashboard />} />
          <Route exact path="/page_not_found" element={<PageNotFound />} />
        </Routes>
        </div>
      </div>
    </Router>
  );
}


export default App;