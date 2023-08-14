import React from 'react'
import { useState } from 'react';
import { useEffect } from 'react';
import {
  Link,
  useNavigate
} from "react-router-dom";



function Navigation({searchClick, handleSearch, setSearchClick}) {
  const navigate = useNavigate();
  const [isActive, setIsActive] = useState(false)
  const logout = () => {
    setIsActive(true)
    localStorage.removeItem('token')
    localStorage.removeItem('screens')
    localStorage.removeItem('username')
    // navigate('/login', {state:{"name": "kasjhoif"}})  

}

useEffect(()=>{
    if(isActive){
        navigate('/login', {state:{"name": "kasjhoif"}})
        setIsActive(false)
    }    
}, [isActive])



return (
          <nav class="navbar navbar-expand-lg navbar-light bg-light">
              <div class="container-fluid">
                    <Link to="" className="navbar-brand">
                      <img src="https://icons.veryicon.com/png/o/business/background-management-system/role-management-3.png" height="28" alt="CoolBrand" />
                    </Link>
                    <div className={`ZPSpanel ${searchClick? 'large-search': ''} `} onClick={handleSearch} id="zpeople_search">
                        <div className="ZPTbox ZPSrbox" id="searchdiv">
                            <span className="IC-lens S8" id="zpeople_search_pico"></span> 
                            <input type="search" className="ZPselect" id="zpeople_search_box" placeholder="Search Employee" value="" name="Search" />
                        </div>
                    </div>
                  <button type="button" className="navbar-toggler" data-bs-toggle="collapse" data-bs-target="#navbarCollapse">
                      <span className="navbar-toggler-icon"></span>
                  </button>
                  <div className="collapse navbar-collapse" id="navbarCollapse">
                      <div className="navbar-nav ms-auto">
                      <div class="navbar-nav">
                          <Link className="nav-item nav-link active" to="/">Home</Link>
                      </div>
                      <div class="navbar-nav">
                      {localStorage.token ? <Link className="nav-item nav-link active" to="/dashboard">Dashboard</Link> : '' }
                      </div>
                      {localStorage.token === undefined ? <Link className="nav-item nav-link active" to="/login">Login</Link> :<Link className="nav-item nav-link active" onClick={() => logout()} >Logout</Link>}
                          <Link className="nav-item nav-link active" to="/register">Register</Link>
                      </div>
                  </div>
              </div>
          </nav>    
  )
}
export default Navigation;