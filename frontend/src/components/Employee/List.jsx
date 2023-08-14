import React, {useState} from 'react'
import { IP } from '../../constants';
import ModalView from './ModalView'

function List({item, isCheck, is_delete, is_edit, setIsLoad, isLoad}) {
    const [show, setShow] = useState(false);
    const [formData, setFormData] = useState({})
    console.log("item", item);
    
    const get_data = async (id) => {
        // debugger
        let form = {
            id:id
        }

        try{
            let response = await fetch(`${IP}/api/view_employee_by_id`,{
                method:'POST',
                headers:{
                    'Content-Type':'application/json',
                    'Authorization':`Bearer ${localStorage.token}`
                },
                mode:'cors',
                referrer:'no-referrer',
                credentials:'same-origin',
                body:JSON.stringify(form)
            })
            
            const data = await response.json()
            console.log("data??????????????????? by id", data);
            
        
        

            if(data.status === 'success'){
                setFormData(data.employees)
            }
            
        } catch(e){
            console.log("e", e);
        }
    
    
    }


    const handleShow = async (id) => { 
        console.log("handle show", id);
        await get_data(id)
        await setShow(true)
        
    }
    const handleClose = () => setShow(false);
    
    const handleDelete = async (id) => {
        // debugger
        let form = {
            id:id
        }

        try{
            let response = await fetch(`${IP}/api/delete_employee_by_id`,{
                method:'DELETE',
                headers:{
                    'Content-Type':'application/json',
                    'Authorization':`Bearer ${localStorage.token}`
                },
                mode:'cors',
                referrer:'no-referrer',
                credentials:'same-origin',
                body:JSON.stringify(form)
            })
            
            const data = await response.json()
            console.log("data", data);
            
        
        

            if(data.status === 'success'){
                alert(data.status)
                setIsLoad()
            }
            
        } catch(e){
            console.log("e", e);
        }
    
    
    }
    console.log("item._id", item._id);
  
    // debugger
    return (
        <React.Fragment>
            <ModalView handleClose={handleClose} isLoad={isLoad} setShow={setShow} formData={formData} show={show} setIsLoad={setIsLoad} />
            <tr>
                <td><input type="checkbox" checked={isCheck} /></td>
                <td>{item.first_name}</td>
                <td>{item.last_name}</td>
                <td>{item.email}</td>
                <td>{item.nick_name}</td>
                <td>{item.department_name}</td>
                <td>{item.location_name}</td>
                <td>{item.designation}</td>
                <td>{item.employment_type}</td>
                <td>{item.employee_status}</td>
                <td>{item.date_of_joining}</td>
                <td>
                    <span>
                        {is_edit ? <button className='btn btn-sm btn-info' onClick={() => handleShow(item._id)} >Edit</button>: "" }
                        {is_delete ? <button className='btn btn-sm btn-danger' onClick={() => handleDelete(item._id)}>Delete</button> : ""} 
                        
                    </span>
                    
                </td>
            </tr>
        </React.Fragment>
    )
}
export default List

