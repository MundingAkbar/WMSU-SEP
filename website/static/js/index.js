let id;

function setDelete(userId){
    id = userId
}

function deleteUser(){
    fetch('/delete-user', {
        method: 'POST',
        body: JSON.stringify({ id: id })
    }).then((_res) =>  {
        window.location.href = "/manage_students";
    })
}



