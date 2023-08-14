import React, {useState} from 'react'
import { useEffect } from 'react';
import { IP } from '../../constants';
import Headers from './Headers';
import List from './List';
import Paginate from './Paginate';

function ViewEmployee({is_delete, is_edit}) {
    const [list, setList] = useState([])
    const [isCheck, setIsCheck] = useState(false)
    const [isLoad, setIsLoad] = useState(1)
    const [size, setSize] = useState(null)    // comment for some reason working in progress


    


    const fetchData = async(url) => {
        let response = await fetch(url, {
            method: "GET",
            headers: {
                "Content-type": "application/json",
                "Authorization": `Bearer ${localStorage.token}`
            },
            mode: "cors",
            referrer:'no-referrer',
            credentials:'same-origin',
        })

        let data =  await response.json()
        console.log(data);
        if(data.detail){
            alert(data.detail)
        }

        setList(data.items) // work on it later for now reset to last


        if(data.items){

            setSize(Math.ceil(data.total/data.size))
            setList(data.items)
        

        }

        //setList(data.employees) // work on it later for now reset to last

    }


    useEffect(() => {
        setIsLoad(1)
        fetchData(`${IP}/api/view_employee`)

    }, [isLoad])

    const handleChange =() => {
        setIsCheck((prev)=>prev!==true)
    }
    // debugger
    console.log("list=============================><><><>", list);
    const dataList = list.map((item) => <List item={item} isCheck={isCheck} setIsLoad={setIsLoad} isLoad={isLoad} setIsCheck={setIsCheck} is_delete={is_delete} is_edit={is_edit}/>)
    

    const handlePageClick = async (event) => {
      
        let response = await fetch(`${IP}/api/view_employee?page=${event.selected+1}`, {
            method: "GET",
            headers: {
                "Content-type": "application/json",
                "Authorization": `Bearer ${localStorage.token}`
            },
            mode: "cors",
            referrer:'no-referrer',
            credentials:'same-origin',
        })

        let data =  await response.json()
        
        if(data.detail){
            alert(data.detail)
        }
        
        if(data.items){
            setList(data.items)
        }
    };
    

    return (
        <div className="section mt-4">
            <nav className="navbar navbar-expand-lg p-4 mb-5 navbar-light bg-light">
                <b className="navbar-brand">Employee View</b>
            </nav>
            <div className="table-responsive m-5" style={{backgroundColor: "#fff"}} >
                <table className="table mb-5 ms-5">
                    <Headers isCheck={isCheck} setIsCheck={setIsCheck} handleChange={handleChange}  is_delete={is_delete} is_edit={is_edit}/>
                    <tbody>
                        {dataList}    
                    </tbody>    
                </table>
                <Paginate list={list} handlePageClick={handlePageClick} size={size} />
            </div>
        </div>
    )
}

export default ViewEmployee;

