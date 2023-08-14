
import React  from "react";
import Footer from "./components/pages/Footer";
function Home() {
    return (
        <React.Fragment>
            <div className="text-center m-5">
                <div className="row">
                    <div className="col-6">
                        <img  width={window.innerWidth/4} className="img-fluid" src="https://images.pexels.com/photos/416405/pexels-photo-416405.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"/>
                    </div>
                    <div className="col-6">
                        <h1>RBMS</h1>
                        <div>
                            Welcome Role Based Access Control Management
                        </div>
                    </div>
                </div>
            </div>
        <Footer />
    </React.Fragment>
    )
  }
  
export default Home  