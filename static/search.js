document.getElementById('search').addEventListener('input', function() {
    let input = this.value;
    fetch(`/search?query=${input}`)
        .then(response => response.json())
        .then(data => {
            let suggestions = document.getElementById('suggestions');
            suggestions.innerHTML = '';
            data.forEach(user => {
                let listItem = document.createElement('li');
                let link = document.createElement('a');
                link.href = `/employee_details/${user.id}`;
                link.textContent = `${user.fname} ${user.lname}`;
                listItem.appendChild(link);
                suggestions.appendChild(listItem);
            });
        });
});