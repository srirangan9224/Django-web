document.addEventListener("DOMContentLoaded",()=>{
    document.querySelectorAll(".comments").forEach(button=>{
        button.style.display = 'none'
    })
    document.addEventListener("click",event=>{
        if(event.target.className == "comment_button"){
            if(event.target.dataset.mode == "view"){
                event.target.dataset.mode = "hide"
                event.target.innerHTML = "hide comments"
                document.querySelectorAll(".comments").forEach(link=>{
                    if (link.dataset.post == event.target.dataset.post){
                        link.style.display = 'block'
                    }
                })
            }
            else{
                event.target.innerHTML = "view comments"
                event.target.dataset.mode = "view"
                document.querySelectorAll(".comments").forEach(link=>{
                    if (link.dataset.post == event.target.dataset.post){
                        link.style.display = 'none'
                    }
                })
            }
        }
    })
})