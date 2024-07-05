document.addEventListener("DOMContentLoaded",()=>{
    document.querySelector(".profile").style.display = 'block';
    document.querySelector(".follow").style.display = 'block';
    document.querySelector(".posts").style.display = 'none';
    document.addEventListener("click",(event)=>{
        if(event.target.dataset.funct === "profileButton"){
            document.querySelector(".profile").style.display = 'block';
            document.querySelector(".follow").style.display = 'block';
            document.querySelector(".posts").style.display = 'none';
        }
        else if(event.target.dataset.funct === "postsButton"){
            document.querySelector(".profile").style.display = 'none';
            document.querySelector(".follow").style.display = 'none';
            document.querySelector(".posts").style.display = 'block';
        }
    })
})