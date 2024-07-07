document.addEventListener("DOMContentLoaded",()=>{
    document.addEventListener("click",event=>{
        if (event.target.className == "likes"){
            let post_id = event.target.dataset.post
            console.log(post_id)
            fetch('/like', {
                method: 'POST',
                body: JSON.stringify({
                    "post_id": post_id
                })
              })
            .then(response => response.json())
            .then(result => console.log(result))
            .catch(error => error.message)
            location.reload()
        }
    })
})