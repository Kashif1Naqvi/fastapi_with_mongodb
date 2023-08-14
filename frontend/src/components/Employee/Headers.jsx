import React from 'react'

 function Headers({isCheck, handleChange, is_delete, is_edit}) {
    
  
  return (
    <thead>
        <tr>
            <th scope="col"><input type="checkbox" checked={isCheck} onChange={handleChange} /></th>
            <th scope="col">First Name <span><i className="fa-solid fa-chevron-down"></i></span></th>
            <th scope="col">Last Name <span><i className="fa-solid fa-chevron-down"></i></span></th>
            <th scope="col">Email <span><i className="fa-solid fa-chevron-down"></i></span></th>
            <th scope="col">Nick Name <span><i className="fa-solid fa-chevron-down"></i></span></th>
            <th scope="col">Department Name <span><i className="fa-solid fa-chevron-down"></i></span></th>
            <th scope="col">Location Name <span><i className="fa-solid fa-chevron-down"></i></span></th>
            <th scope="col">Designation <span><i className="fa-solid fa-chevron-down"></i></span></th>
            <th scope="col">Employment Type <span><i className="fa-solid fa-chevron-down"></i></span></th>
            <th scope="col">Employment Status <span><i className="fa-solid fa-chevron-down"></i></span></th>
            <th scope="col">Date Of Joining <span><i className="fa-solid fa-chevron-down"></i></span></th>
            {(is_delete || is_edit) ? <th scope="col">Operations</th>: ''} 
        </tr>
    </thead>
  )
}
export default Headers;