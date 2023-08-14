import React, { useState } from 'react'
import '../../css/link.css'
import { IP } from '../../constants';
import { useForm } from 'react-hook-form';

function AddForm({formData, setIsLoad, isLoad, setShow}) {
    const { register, handleSubmit, formState: { errors } } = useForm();
    console.log("formData", formData === undefined);
    
    const [id, setId] = useState(formData === undefined ? '' : formData._id)
    const [firstName, setFirstName] = useState(formData === undefined ? '' : formData.first_name)
    const [lastName, setLastName] = useState(formData === undefined ? '' : formData.last_name)
    const [email, setEmail] = useState(formData === undefined ? '' : formData.email)
    const [nickName, setNickName] = useState(formData === undefined ? '' : formData.nick_name)
    const [departmentName, setDepartmentName] = useState(formData === undefined ? '' : formData.department_name)
    const [locationName, setLocationName] = useState(formData === undefined ? '' : formData.location_name)
    const [designation, setDesignation] = useState(formData === undefined ? '' : formData.designation)
    const [employmentType, setEmploymentType] = useState(formData === undefined ? '' : formData.employment_type)
    const [employmentStatus, setEmploymentStatus] = useState(formData === undefined ? '' : formData.employee_status)
    const [dateOfJoining, setDateOfJoining] = useState(formData === undefined ? '' : formData.date_of_joining)

    const onSubmit = async () => {
        let url = `${IP}/api/create_employee`
        let form = {
            first_name: firstName,
            last_name: lastName,
            email: email,
            nick_name: nickName,
            department_name: departmentName,
            location_name: locationName,
            designation: designation,
            employment_type: employmentType,
            employee_status: employmentStatus,
            date_of_joining: dateOfJoining
        }

        if(id){
            form['id'] = id
            url = `${IP}/api/edit_employee_by_id`
        }


        try{
            let response = await fetch(url,{
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
        console.log("data", data);
        
        if(data.detail){
            alert(data.detail  || "invalid request please check you params")
            
        }

        if(data.status === 'success'){
            if(id){
                alert(data.status)
                console.log(isLoad);
                setIsLoad()
                setShow(false)
            } else {
                alert(data.status)
            }
        }
        if(data.status === 'failed'){
            alert(data.message)
        }
        } catch(e){
            console.log("e", e);
        }
    }

    
    
  console.log("errors.Email", errors);
  return (
    <div className='link-form'>
        <div className='form-header' >
            <div className="ssp-profmin" id="zp_form_headerdisp">
                {id ? <span className="ssp-un" id="zp_form_header_name">Edit&nbsp;Employee</span>: <span className="ssp-un" id="zp_form_header_name">Add&nbsp;Employee</span>}
            </div>
        </div>
        <div className='form-container'>
            <form className='add-form' onSubmit={handleSubmit(onSubmit)}>
                {id ? <input type="hidden" name="id" value={id}  onChange={(e)=> setId(e.target.value)}/> : ''}
                <h3 issec="true" id="724531000000035993" className="zpcont-title"><span className="ZPbold">Basic information</span></h3>
                <div className="row">
                    <div className="col-sm-6">
                        <div className="form-input">
                            <label className="field-label zp_mdt"><font className="zp_mlne">First Name</font></label>
                            <div className='input-label'>
                            <input  id="emplooyee"  type="text" name="first_name" className=" form-control zptxt-edit "  {...register("first_name", {required: true, maxLength: 80})}  value={firstName}  onChange={(e)=> setFirstName(e.target.value)} />
                            {errors.first_name && <p className='alert alert-danger' >first name is required.</p>}
                            </div>
                        </div>
                        <div className="form-input">
                            <label className="field-label zp_mdt"><font className="zp_mlne">Last Name</font></label>
                            <div className='input-label'>
                            <input  type="text" name="last_name" className=" form-control zptxt-edit "   {...register("last_name", {required: true, maxLength: 100})} onChange={(e)=> setLastName(e.target.value)} id="emplooyee" value={lastName} />
                            {errors.last_name && <p className='alert alert-danger' >Last name is required.</p>}
                            </div>
                        </div>
                        <div className="form-input">
                            <label className="field-label zp_mdt"><font className="zp_mlne">Email</font></label>
                            <div className='input-label'>
                            <input  type="text" name="email" className=" form-control zptxt-edit "   {...register("email_address", {required: true, pattern: /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/i})} onChange={(e)=> setEmail(e.target.value)} id="emplooyee" value={email} />
                            {errors.email_address && <p className='alert alert-danger' >Invalid email please type correct email</p>}
                            </div>
                        </div>
                    </div>
                    <div className="col-sm-6">
                        <div className="form-input">
                            <label className="field-label zp_mdt"><font className="zp_mlne">Nick Name</font></label>
                            <div className='input-label'>
                                <input onChange={(e)=> setNickName(e.target.value)} id="emplooyee" value={nickName} type="text" name="nickName" className=" form-control zptxt-edit "  />
                            </div>
                        </div>
                    </div>
                </div>
                <h3 issec="true" id="724531000000035993" className="zpcont-title"><span className="ZPbold">Work information</span></h3>
                <div className="row">
                <div className="col-sm-6">
                        <div className="form-input">
                            <label className="field-label zp_mdt"><font className="zp_mlne">Department Name</font></label>
                            <div className='input-label'>
                            <input onChange={(e)=> setDepartmentName(e.target.value)} id="emplooyee" value={departmentName} type="text" name="department_name" className=" form-control zptxt-edit "  />
                            </div>
                        </div>
                        <div className="form-input">
                            <label className="field-label zp_mdt"><font className="zp_mlne">Location Name</font></label>
                            <div className='input-label'>
                            <input onChange={(e)=> setLocationName(e.target.value)} id="emplooyee" value={locationName} type="text" name="location" className=" form-control zptxt-edit "  />
                            </div>
                        </div>
                        <div className="form-input">
                            <label className="field-label zp_mdt"><font className="zp_mlne">Designation</font></label>
                            <div className='input-label'>
                            <input onChange={(e)=> setDesignation(e.target.value)} id="emplooyee" value={designation} type="text" name="designation" className=" form-control zptxt-edit "  />
                            </div>
                        </div>
                    </div>
                    <div className="col-sm-6">
                        <div className="form-input">
                            <label className="field-label zp_mdt"><font className="zp_mlne">Employment Type</font></label>
                            <div className='input-label'>
                            <input onChange={(e)=> setEmploymentType(e.target.value)} id="emplooyee" value={employmentType} type="text" name="employment_type" className=" form-control zptxt-edit "  />
                            </div>
                        </div>
                        <div className="form-input">
                            <label className="field-label zp_mdt"><font className="zp_mlne">Employee Status</font></label>
                            <div className='input-label'>
                            <input onChange={(e)=> setEmploymentStatus(e.target.value)} id="emplooyee" value={employmentStatus} type="text" name="employee_status" className=" form-control zptxt-edit "  />
                            </div>
                        </div>
                        <div className="form-input">
                            <label className="field-label zp_mdt"><font className="zp_mlne">Date of Joining</font></label>
                            <div className='input-label'>
                            <input onChange={(e)=> setDateOfJoining(e.target.value)} id="emplooyee" value={dateOfJoining} type="date" name="date_of_joining" className=" form-control zptxt-edit "  />
                            </div>
                        </div>
                    </div>
                </div>
                <div className="add-form-btn form-group">
                <input type="submit" value="submit" className='btn btn-danger' />
                </div>
            </form>
        </div>
    </div>
  )
}

export default AddForm;