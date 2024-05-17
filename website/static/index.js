function deleteTodo(todoId){
    fetch(`/delete-todo`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({todoId: todoId})
    }).then((_res) => {
        window.location.href = "/";
    })
}