import React,{useState} from 'react';
import "./Login.css";
import { Link } from 'react-router-dom';
import {
  MDBBtn,
  MDBContainer,
  MDBRow,
  MDBCol,
  MDBCard,
  MDBCardBody,
  MDBInput,
  MDBIcon,
  MDBCheckbox
}
from 'mdb-react-ui-kit';

function App() {

    const [name,setName] = useState("");
    const [pass,setPass] = useState("");
    const [mail,setMail] = useState("");

    const nameChange = (event)=>{
        setName(event.target.value);
    }

    const mailChange = (event)=>{
        setMail(event.target.value);
    }

    const passChange = (event)=>{
        setPass(event.target.value);
    }

    const submitRegister = ()=>{
        console.log(name);
        console.log(mail);
        console.log(pass);
    }

  return (
    <div style={{background:"#508bfc"}}>
    <MDBContainer fluid>

      <MDBRow className='d-flex justify-content-center align-items-center h-100'>

            <p style={{color:"#c8b9b9",textShadow:"4px 3px 4px #000000",padding:"41px 0px 0px 0px",textDecoration:"underline", 
                fontSize:"60px", fontFamily:"Oswald"}}>Attendance Monitoring System</p>

        <MDBCol col='12' style={{margin : "17px 0px 0px 0px"}}>

          <MDBCard className='bg-white my-5 mx-auto' style={{borderRadius: '1rem', maxWidth: '500px'}}>
            <MDBCardBody className='p-5 w-100 d-flex flex-column'>

              <h2 className="fw-bold mb-2 text-center">Create Account</h2>
              <p className="text-white-50 mb-3">Please enter your login and password!</p>

              <MDBInput onChange={nameChange} wrapperClass='mb-4 w-100' label='Full Name' type='text' size="lg"/>
              <MDBInput onChange={mailChange} wrapperClass='mb-4 w-100' label='Email address' type='email' size="lg"/>
              <MDBInput onChange={passChange} wrapperClass='mb-4 w-100' label='Password' type='password' size="lg"/>

              
            <div className="container" style={{height:"12px"}}></div>
            <p>{"Already have an account?"}
                <Link to="/">
                    <span  className="f3 link dim black underline pa3 pointer" 
                    style={{padding:"0px 2px", fontSize:"16px" ,color:"#003d93"}}>Sign In</span>
                </Link>
            </p>
                    

              <MDBBtn onClick={submitRegister} size='lg'>
                Register
              </MDBBtn>

            </MDBCardBody>
          </MDBCard>

        </MDBCol>
      </MDBRow>

    </MDBContainer>
    </div>
  );
}

export default App;