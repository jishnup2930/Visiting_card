import React, { useState, useEffect } from 'react';

function EmployeeDetails() {
  const [employeeData, setEmployeeData] = useState(null);
  const [currentEmployeeIndex, setCurrentEmployeeIndex] = useState(0);
  const employeeIds = []; // Assuming you have an array of employee ids

  useEffect(() => {
    if (currentEmployeeIndex >= 0 && currentEmployeeIndex < employeeIds.length) {
      const employeeId = employeeIds[currentEmployeeIndex];
      const employeeUrl = `/employees/${employeeId}`;
      
      fetch(employeeUrl)
        .then(response => response.json())
        .then(data => {
          setEmployeeData(data);
          $("span.info")[0].innerHTML = "Loaded";
        })
        .catch(error => {
          console.error('Error fetching employee data:', error);
        });
    }
  }, [currentEmployeeIndex, employeeIds]);

  const disableAddLeaveForm = () => {
  };

  const enableAddLeaveForm = () => {
  };

  const handleNextEmployee = () => {
    if (currentEmployeeIndex < employeeIds.length - 1) {
      setCurrentEmployeeIndex(prevIndex => prevIndex + 1);
    } else {
      alert("You've reached the last employee.");
    }
  };

  const handlePrevEmployee = () => {
    if (currentEmployeeIndex > 0) {
      setCurrentEmployeeIndex(prevIndex => prevIndex - 1);
    } else {
      alert("You're at the first employee.");
    }
  };

  const handleSubmitLeave = (ev) => {
    ev.preventDefault();
  };

  return (
    <div>
      
      <button id="prevEmployee" className="btn btn-primary btn-sm" onClick={handlePrevEmployee}>Prev</button>
      <button id="nextEmployee" className="btn btn-primary btn-sm" onClick={handleNextEmployee}>Next</button>
      
      <form onSubmit={handleSubmitLeave}>
        <input type="submit" value="Submit" />
      </form>
    </div>
  );
}

export default EmployeeDetails;

function gotEmployees(data) {
    console.log(data);
    $("span.info")[0].innerHTML = "Loaded";

    const userDetailsHTML = `
        <h1> Details for ${data.fname}  ${data.lname}</h1>
        <h2> ${data.title} </h2>
        <table>
            <tr>
                <th> First name </th>
                <td> ${data.fname}</td>
            </tr>
            <tr>
                <th> Last name </th>
                <td> ${data.lname}</td>
            </tr>
            <tr>
                <th> Email </th>
                <td> ${data.email}</td>
            </tr>
            <tr>
                <th> Phone </th>
                <td> ${data.phone}</td>
            </tr>
        </table>
        <div>
            <h1> Leave Details </h1>
            <table>
                <tr>
                    <th> Max leaves </th>
                    <td> ${data.max_leaves}</td>
                </tr>
                <tr>
                    <th> Leaves taken </th>
                    <td> ${data.leave}</td>
                </tr>
            </table>
        </div>
        <div>
            <h1> Add leave </h1>
            <form action="/leave/${data.id}" method="POST">
                <label for="leave_date">Leave Date:</label>
                <input type="date" id="leave_date" name="leave_date"><br><br>
                <label for="leave_reason">Reason:</label><br>
                <textarea id="leave_reason" name="leave_reason" rows="2" cols="50"></textarea><br><br>
                <input type="submit" value="Submit">
            </form>
        </div>
        <div>
            <br>
            <button id="prevEmployee" class="btn btn-primary btn-sm">Prev</button>
            <button id="nextEmployee" class="btn btn-primary btn-sm">Next</button>
            </br>
        </div>`;

    $("#userdetails")[0].innerHTML = userDetailsHTML;

}

$(function() {
    $("a.userlink").click(function(ev) {
        $("span.info")[0].innerHTML = "Loading...";
        $.get(ev.target.href, gotEmployees);
        ev.preventDefault();
    });

});