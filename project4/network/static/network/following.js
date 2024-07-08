document.addEventListener("DOMContentLoaded",()=>{
    document.querySelectorAll(".profile").forEach(profile=>{
        profile.style.display = 'block'
    })
    document.querySelectorAll("#posts").forEach(profile=>{
        profile.style.display = 'none'
    })
    document.addEventListener("click",(event)=>{
        if(event.target.dataset.funct === "profileButton"){
            document.querySelectorAll(".profile").forEach(profile=>{
                profile.style.display = 'block'
            })
            document.querySelectorAll("#posts").forEach(profile=>{
                profile.style.display = 'none'
            })
        }
        else if(event.target.dataset.funct === "postsButton"){
            document.querySelectorAll(".profile").forEach(profile=>{
                profile.style.display = 'none'
            })
            document.querySelectorAll("#posts").forEach(profile=>{
                profile.style.display = 'block'
            })
        }
    })
})