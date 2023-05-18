import React,{useState} from 'react';
import "./Login.css"
import Records from './users.json';
import {
  MDBBtn,
  MDBContainer,
  MDBRow,
  MDBCol,
  MDBCard,
  MDBCardBody,
  MDBInput,
  }
from 'mdb-react-ui-kit';
//import { Login } from './Register2';

const Login =(props) =>{

    const [name,setName] = useState("");
    const [pass,setPass] = useState("");
    

    const nameChange = (event)=>{
        setName(event.target.value);
    }

    const passChange = (event)=>{
        setPass(event.target.value);
    }


    const submitLogin = ()=>{
        console.log(name);
        console.log(pass);

        Records.map(user=>{
            if(user.username===name && user.password===pass){
                console.log("LoggedIn");
                props.setDirect(1);
                
            }
            return console.log("");

        })
        
    }

    

  return (
    <div style={{background:"rgb(55, 60, 61)"}}>
    <MDBContainer fluid>

      <MDBRow className='d-flex justify-content-center align-items-center h-100'>
      <p style={{color:"white",textShadow:"2px 2px 4px #000000",padding:"41px 0px 0px 0px", 
                fontSize:"60px", fontFamily:"Oswald"}}>Attendance Monitoring System</p>
        <MDBCol col='12' style={{margin : "-5px 0px 11px 0px"}}>
        {/* <form onSubmit={}> */}
          <MDBCard className='bg-white my-5 mx-auto' style={{borderRadius: '1rem', maxWidth: '500px'}}>
            <MDBCardBody className='p-5 w-100 d-flex flex-column'>

              <h2 className="fw-bold mb-2 text-center">Sign in</h2>
              <p className="text-white-50 mb-3">Please enter your login and password!</p>

              <MDBInput onChange={nameChange} wrapperClass='mb-4 w-100' label='Email address' type='email' size="lg"/>
              <MDBInput onChange={passChange} wrapperClass='mb-4 w-100' label='Password' type='password' size="lg"/>

              
            <div className="container" style={{height:"12px"}}></div>
            {/* <p>{"Don't have an account?"}
                <Link to="/register">
                    <span  className="f3 link dim black underline pa3 pointer" 
                    style={{padding:"0px 2px", fontSize:"16px" ,color:"#003d93"}}>Register</span>
                </Link>
            </p> */}

            <MDBBtn size='lg' onClick={submitLogin}>Login</MDBBtn>
                    
            {/* <Link to="/facerecognition">
              <MDBBtn size='lg' onClick={submitLogin}>Login</MDBBtn>
            </Link> */}

            </MDBCardBody>
          </MDBCard>
          {/* </form> */}

        </MDBCol>
      </MDBRow>

    </MDBContainer>
    </div>
  );
}

export default Login;