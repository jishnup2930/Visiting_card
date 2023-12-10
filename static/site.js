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
            <form action="/add_leave/${data.id}" method="POST">
                <label for="leave_date">Leave Date:</label>
                <input type="date" id="leave_date" name="leave_date"><br><br>
                <label for="leave_reason">Reason:</label><br>
                <textarea id="leave_reason" name="leave_reason" rows="4" cols="50"></textarea><br><br>
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

    currentEmployeeIndex = employeeIds.indexOf(data.id);
}

function disableAddLeaveForm() {
    $('#leave_date, #leave_reason, input[type="submit"]').prop('disabled', true);
}

function enableAddLeaveForm() {
    $('#leave_date, #leave_reason, input[type="submit"]').prop('disabled', false);
}

$(function() {
    $("a.userlink").click(function(ev) {
        $("span.info")[0].innerHTML = "Loading...";
        $.get(ev.target.href, gotEmployees);
        ev.preventDefault();
    });

    $("#nextEmployee").click(function() {
        if (currentEmployeeIndex < employeeIds.length - 1) {
            currentEmployeeIndex++;
            const nextEmployeeId = employeeIds[currentEmployeeIndex];
            const nextEmployeeUrl = `/employees/${nextEmployeeId}`;
            $("span.info")[0].innerHTML = ``;
            $.get(nextEmployeeUrl, gotEmployees);
        } else {
            alert("You've reached the last employee.");
        }
    });

    $("#prevEmployee").click(function() {
        if (currentEmployeeIndex > 0) {
            currentEmployeeIndex--;
            const prevEmployeeId = employeeIds[currentEmployeeIndex];
            const prevEmployeeUrl = `/employees/${prevEmployeeId}`;
            $("span.info")[0].innerHTML = "Loading previous employee...";
            $.get(prevEmployeeUrl, gotEmployees);
        } else {
            alert("You're at the first employee.");
        }
    });

    $("form").submit(function(ev) {
        ev.preventDefault();
        const formData = $(this).serializeArray();
        const leaveTaken = parseInt($("#leave_details td:nth-child(2)").text().trim());
        const maxLeaves = parseInt($("#leave_details td:nth-child(2)").text().trim());

        if (leaveTaken >= maxLeaves) {
            alert('Cannot take more leave. Maximum leaves taken.');
            return;
        }
        $.ajax({
            type: "POST",
            url: $(this).attr('action'),
            data: formData,
            success: function(response) {
            },
            error: function(error) {
            }
        });
    });
});
