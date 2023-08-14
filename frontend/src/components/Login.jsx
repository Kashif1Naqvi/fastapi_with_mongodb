import React, {useState} from 'react'
import  { useNavigate } from 'react-router-dom'
import { IP } from '../constants'

function Login() {
    const [email,setEmail] = useState('')
    const [password,setPassword] = useState('')
    const [error, setError] = useState(null)
    const navigate = useNavigate();

   

    const handleSubmit = async (e) =>{
        e.preventDefault()
        let form = new FormData()
        form.append('username', email)
        form.append('password', password)
        
        try{
            let response = await fetch(`${IP}/login`,{
            method:'POST',
            mode:"cors",
            redirect: "follow",
            body: form
          })
        
        
        const data = await response.json()
        console.log(data);

        if(data.detail){
            setError(data.detail)
        }

        if(data.status === 'success'){
            alert(data.status)
            localStorage.setItem("token", data.access_token)
            localStorage.setItem("username", data.username)
            localStorage.setItem("screens", JSON.stringify(data.screens_list))
            navigate("/dashboard")
            
            
            
        }
        } catch(e){
            console.log("e", e);
        }
        

    
    
    }
  return (
    <section className="vh-100" style={{backgroundColor: "#eee"}}>
    
    <div className="container h-100">
        <div className="row d-flex justify-content-center align-items-center h-100">
        <div className="col-lg-12 col-xl-11">
            <div className="card text-black" style={{borderRadius: "border-radius: 25px"}} >
            <div className="card-body p-md-5">
                <div className="row justify-content-center">
                <div className="col-md-10 col-lg-6 col-xl-5 order-2 order-lg-1">
                    <p className="text-center h1 fw-bold mb-5 mx-1 mx-md-4 mt-4">Login</p>
                    <form className="mx-1 mx-md-4" onSubmit={handleSubmit}>
                       

                        <div className="d-flex flex-row align-items-center mb-4">
                            <i className="fas fa-envelope fa-lg me-3 fa-fw"></i>
                            <div className="form-outline flex-fill mb-0">
                            <label className="form-label" for="email">Your Email</label>
                            <input required type="email" id="email" className="form-control" value={email} onChange={(e)=> setEmail(e.target.value)} />
                            </div>
                        </div>

                        <div className="d-flex flex-row align-items-center mb-4">
                            <i className="fas fa-lock fa-lg me-3 fa-fw"></i>
                            <div className="form-outline flex-fill mb-0">
                            <label className="form-label" for="password">Password</label>
                            <input required type="password" id="password" className="form-control" value={password} onChange={(e)=> setPassword(e.target.value)}/>
                            </div>
                        </div>

                        
                        <div className="d-flex justify-content-center mx-4 mb-3 mb-lg-4">
                            <button type="submit" className="btn btn-primary btn-lg">Login</button>
                        </div>
                    </form>
                    {error && ( <div className="d-flex justify-content-center mx-4 mb-3 mb-lg-4"><span className='alert alert-danger'>{error}</span> </div> )}
                </div>
                <div className="col-md-10 col-lg-6 col-xl-7 d-flex align-items-center order-1 order-lg-2">
                    <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-registration/draw1.webp" className="img-fluid" alt="Sample show" />
                </div>
                </div>
            </div>
            </div>
        </div>
        </div>
    </div>
    </section>
  )
}
export default Login