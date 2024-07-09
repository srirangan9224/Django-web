document.addEventListener("DOMContentLoaded",()=>{
    // basic config 
    document.querySelectorAll(".solid").forEach(div=>{
        if(div.dataset.page == 1){
            div.style.display = 'block';
        }
        else{
            div.style.display = 'none';
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