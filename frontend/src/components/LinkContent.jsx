import React from 'react'
import AddForm from './Employee/AddForm';
import ViewEmployee from './Employee/ViewEmployee';
import '../css/employee.css'
 function LinkContent({link, is_delete, is_edit}) {
  if(link){
    
    console.log("===========================link===================================", link.link_text);

    if(link.link_text === 'addEmployee') return <AddForm />
    if(link.link_text === 'Employee') return <ViewEmployee is_delete={is_delete} is_edit={is_edit} />
    
  
  return (
    
    <React.Fragment>
      {/* <Cards /> */}
      <div style={{marginTop: window.innerHeight/ 2 }} >{link.link_description}</div>
    </React.Fragment>
  )
}
}
export default LinkContent