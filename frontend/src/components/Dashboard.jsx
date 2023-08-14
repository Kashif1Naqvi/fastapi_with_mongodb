import React, {useEffect} from 'react'
import { useState } from 'react'
import {USERNAME, IP} from '../constants'
import {useNavigate, Link} from 'react-router-dom'
import '../css/dashboard.css'
import PageNotFound from './pages/PageNotFound'
import Links from './Links'
function Dashboard() {
  const navigate = useNavigate()


  const [screen, setScreens] = useState([])
  const [links, setLinks] = useState(null)
  const [username, setUserName] = useState('')
  const [width, setWidth] = useState(20)
  const [height, setHeight] = useState(20)
  const [show, setShow] = useState(false)
  const [link, setLink] = useState(null)
  const [is_delete, setDelete] = useState(false)
  const [is_edit, setEdit] = useState(false)

    const get_links = async (obj, target) => {
        let data = {
            "screen_id": obj.screen_id,
            "link_id": obj._id,
        }
        console.log(data);
      
        let response = await fetch(`${IP}/api/link_for_screen`,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'Authorization':`Bearer ${localStorage.token}`
        },
        mode:'cors',
        referrer:'no-referrer',
        credentials:'same-origin',
        body:JSON.stringify(data)
        })
        
        
        const response_data = await response.json()
        console.log(response_data.link_content);
        if(response_data.detail){
            setLink(response_data.detail)
        } else {
            console.log("response_data.link_content", response_data.link_content);
            setLink(response_data.link_content)
        }
      
    }
    
  useEffect(()=>{
    if(localStorage.token === undefined){
        navigate('/page_not_found')
    }
    
  

    if(localStorage.screens !== undefined){
      let list = JSON.parse(localStorage.screens);
      setScreens(list)
    }
    
    setUserName(USERNAME)
  
  }, [])  


  const get_screen_links = async (screen_id) => {
    let data = {
      "screen_id": screen_id
    }

    let response = await fetch(`${IP}/api/screen_for_login_user`,{
      method:'POST',
      headers:{
        'Content-Type':'application/json',
        'Authorization':`Bearer ${localStorage.token}`
      },
      mode:'cors',
      referrer:'no-referrer',
      credentials:'same-origin',
      body:JSON.stringify(data)
    })

    const response_data = await response.json()
    console.log("response_data", response_data);
    if(response_data.screen_allowed_links){
      setDelete(false)
      setLink(null)
      setEdit(false)
      setLinks(response_data.screen_allowed_links)
      response_data.screen_allowed_links.map((item)=>{
        
        
        if(item.link_text === "editEmployee"){
            setEdit(true)
        }

        if(item.link_text === "deleteEmployee"){
            console.log("delete", item.link_text);
            setDelete(true)            
        }
        
      })

      setTimeout(()=>{
        setShow(true)
      }, 1000)
      
    } 

    if(response_data.detail){
      setLinks(response_data.detail)
    }
    
  }
  console.log("is_delete", is_delete);
  console.log("is_edit", is_edit);
  console.log("screen.length", screen.length);
  if(screen.length === 0){
    return (
      <div className="row">
        <div className="col-12">
          <PageNotFound message={`${username} no screens avaialble for you please contact with support`} />
        </div>
      </div>
    )
  } 
  

  return (
    <div className='row'>
      <div className="col-1 menu">
          <nav id="sidebarMenu" className="vh-100" style={{"width": () => setWidth(window.innerWidth/6)}} >
                <div className="list-group list-group-flush mx-3 mt-4 v-100">
                  {
                    screen && (screen.map((item)=>(
                      <div className='menu_content'>
                      <img class="ZPMic" src="https://js.zohostatic.com/people/01DEC2022_HF_1216/people3/images/svg/app.svg"></img>
                      <Link className="text-decoration-none"  onClick={() => get_screen_links(item._id)}>
                        <span>{item.name}</span>    
                      </Link>
                      </div>
                  )))
                  }
                </div>
            </nav>
            <main style={{marginTop: "58px"}}>
            <div className="container pt-4"></div>
          </main>
          
      </div>
      {
        show && (
          <div className="col-1   sub-menu" >
            <nav id="sidebarsubMenu"  className="vh-100" style={{"width": () => setWidth(window.innerWidth/8), "height": () => setHeight(window.innerHeight/8)}} >
                <div className="list-group list-group list-group-flush list-group-flush mx-3 mt-4 v-100 sub-nav-container">
                  {
                      typeof(links) !== 'string' && links && (links.map((item)=>(
                        <React.Fragment>
                          {
                            (item.link_text !== 'editEmployee' && item.link_text !== 'deleteEmployee') ? <Link className="text-decoration-none" key={item._id}  onClick={({target}) => get_links(item, target)}>
                              <span>{item.link_text}</span> 
                            
                              
                          </Link> : ""
                          }
                        </React.Fragment>
                        
                      )))
                    }
                </div>
            </nav>
            <main style={{marginTop: "58px"}}>
             <div className="container pt-4"></div>
            </main>
          </div>
        )
      }
      <div className={`submenu-data ${show ? "col-10": "col-11"}`}>
        {
          typeof(links) === 'string' ? <PageNotFound message={links} /> :   <Links link={link} is_delete={is_delete} is_edit={is_edit} />
        }
      </div>

    </div>
    
  )
}

export default  Dashboard