document.addEventListener("DOMContentLoaded",()=>{
    document.querySelectorAll(".profile").forEach(profile=>{
        profile.style.display = 'block'
    })
    document.querySelectorAll("#posts").forEach(profile=>{
        profile.style.display = 'none'
    })
    document.querySelector(".tb").style.display = 'none';
    document.querySelector(".heading").style.display = 'none';
    document.addEventListener("click",(event)=>{
        if(event.target.dataset.funct === "profileButton"){
            document.querySelectorAll(".profile").forEach(profile=>{
                profile.style.display = 'block'
            })
            document.querySelectorAll("#posts").forEach(profile=>{
                profile.style.display = 'none'
            })
            document.querySelector(".heading").style.display = 'none';
            document.querySelector(".tb").style.display = 'none';
        }
        else if(event.target.dataset.funct === "postsButton"){
            document.querySelectorAll(".profile").forEach(profile=>{
                profile.style.display = 'none'
            })
            document.querySelectorAll("#posts").forEach(profile=>{
                profile.style.display = 'block'
            })
            document.querySelector(".heading").style.display = 'block';
            document.querySelector(".tb").style.display = 'block';
        }
    })

    document.addEventListener("click",event=>{
        if (event.target.className === 'page-link'){
            console.log("hello")
            document.querySelectorAll(".solid").forEach(div=>{
                if(div.dataset.page === event.target.dataset.page){
                    div.style.display = 'block'
                }
                else{
                    div.style.display = 'none'
                }
            })
        }
    })
})