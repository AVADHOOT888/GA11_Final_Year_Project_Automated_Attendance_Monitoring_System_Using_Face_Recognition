import React from 'react'; 
const Table = ({ data }) => { 
  // Create an array of table rows from the JSON data 
  const rows = data.map((item, index) => ( 
    <tr key={index}> 
      <td>{index + 1}</td>   
      <td>{item.id}</td> 
      <td>{item.student_name}</td> 
      <td>{item.attend_status}</td> 
    </tr> 
  )); 
  // Render the table with headers and rows 
  return ( 
    // <table> 
    //   <thead> 
    //     <tr> 
    //       <th>Roll No</th> 
    //       <th>Student ID</th> 
    //       <th>Student Name</th> 
    //       <th>Attendance Status</th> 
    //     </tr> 
    //   </thead> 
    //   <tbody>{rows}</tbody> 
    // </table> 

         <table className="table table-light">
              <thead className="thead-dark">
                <tr>
                <th scope="col">Sr No.</th>
                  <th scope="col">Roll No</th>
                  <th scope="col">Student Name</th>
                  <th scope="col">Attendance Status</th>
                </tr>
              </thead>
              <tbody>{rows}</tbody>
            </table>


  ); 
}; 
export default Table;