function gotEmployees(data) {
    console.log(data);
    $("span.info")[0].innerHTML = "Loaded";
    $("#userdetails")[0].innerHTML=`<h1> Details for ${data.fname}  ${data.lname}</h1>
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
    <form action="/add_leave/${data.id}" method="POST">
    
    <label for="leave_date">Leave Date:</label>
        <input type="date" id="leave_date" name="leave_date"><br><br>
        
        <label for="leave_reason">Reason:</label><br>
        <textarea id="leave_reason" name="leave_reason" rows="4" cols="50"></textarea><br><br>

        <input type="submit" value="Submit">
    </form>
</div>
    
`  

}

$(function() {
    $("a.userlink").click(function (ev) {
        $("span.info")[0].innerHTML = "Loading...";
        $.get(ev.target.href, gotEmployees);
        ev.preventDefault();
        });
});