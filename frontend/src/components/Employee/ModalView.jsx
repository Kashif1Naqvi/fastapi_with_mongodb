import React from 'react'
import { Modal, Button } from "react-bootstrap";
import AddForm from './AddForm';

function ModalView({show, handleClose, formData, setIsLoad, isLoad, setShow}) {
  return (
    <Modal className='full-screen-modal' fullscreen={true} show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Modal heading</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <AddForm  isLoad={isLoad} formData={formData} setIsLoad={setIsLoad} setShow={setShow} />
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>
  )
}

export default ModalView;