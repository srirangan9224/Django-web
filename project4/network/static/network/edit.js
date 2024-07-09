document.addEventListener("DOMContentLoaded",()=>{
    
    document.querySelectorAll(".editForm").forEach(div=>{
        div.style.display = 'none';
    })
    document.querySelectorAll(".edit").forEach(para=>{
        para.style.display = 'block';
    })
    
    document.addEventListener("click",event=>{

        if(event.target.id == "edit"){
            document.querySelectorAll(".edit").forEach(para=>{
                if(para.dataset.poid === event.target.dataset.poid){
                    para.style.display = 'none';
                }
            })

            document.querySelectorAll(".editForm").forEach(div=>{
                if(div.dataset.poid === event.target.dataset.poid){
                    div.style.display = 'block';
                }
            })
        }


    })


    document.addEventListener("click",event=>{
        if(event.target.id == "saveButton"){
            let content='';
            document.querySelectorAll(".textarea").forEach(box=>{
                if(box.dataset.poid == event.target.dataset.poid ){
                    content = box.value;
                }
            })
            fetch('/edit', {
                method: 'POST',
                body: JSON.stringify({
                    "post_id": event.target.dataset.poid,
                    "content": content,
                })
              })
              .then(response => response.json())
              .then(result => console.log(result))
              .catch(error => error.message)
              location.reload()
        }
    })



})