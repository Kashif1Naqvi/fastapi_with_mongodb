import React from 'react'
import { useState } from 'react'
import {Link} from 'react-router-dom'
import {IP} from '../constants'

import LinkContent from './LinkContent'
import PageNotFound from './pages/PageNotFound'

function Links({link, is_delete, is_edit}) {
    
    // debugger
  return (
    <React.Fragment>
           {/*  <div className='row'>
                <div className="col-12">
                    <div className=" list-group-flush mx-3 mt-4 d-flex">
                    {
                        links && (links.map((item)=>(
                        <Link className="list-group-item list-group-item-action py-2 ripple" key={item._id} onClick={() => get_links(item)}>
                            <i className="fas fa-tachometer-alt fa-fw me-3"  ></i><span>{item.link_text}</span>    
                        </Link>
                        )))
                    }
                    </div>
                </div>
            </div> */}

        {(typeof(link) === 'string') ? <PageNotFound message={"hello"} /> :  <LinkContent link={link}  is_delete={is_delete} is_edit={is_edit} />}
    </React.Fragment>
    )
}
export default Links