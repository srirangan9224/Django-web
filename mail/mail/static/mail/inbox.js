document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector("#form-submit").addEventListener('click', create_mail);
  document.addEventListener('click',event =>{
    if (event.target.className === "solid"){
      const mail_id = event.target.dataset.mail_id;
      get_mail_page(mail_id);}
    else if (event.target.id === "reply"){
      console.log("reply");}
    else if (event.target.id === "archive"){
      console.log("archive")
      fetch(`/emails/${event.target.dataset.mail_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: true
        })
      })
    }
    })
  // By default, load the inbox
  load_mailbox('inbox');
});

function mail_page(email){
  document.querySelector("#compose-view").style.display = 'none';
  document.querySelector("#mail-view").style.display = 'block';
  document.querySelector("#emails-view").style.display = 'none';
  const rule = document.createElement('hr');
  const reply_button = document.createElement("button");
  reply_button.id = 'reply';
  reply_button.className = 'btn btn-primary';
  reply_button.dataset.mail_id = email['id'];
  reply_button.innerHTML = 'reply';
  const archive_button = document.createElement("button");
  archive_button.id = 'archive';
  archive_button.dataset.mail_id = email['id'];
  archive_button.innerHTML = 'archive';
  archive_button.className = 'btn btn-warning';
  const mail_page = document.querySelector("#mail-view");
  const para = document.createElement('p')
  para.innerHTML = email["body"]
  console.log(email)

  mail_page.innerHTML = `
  <strong> from: </strong> ${email["sender"]}
  <br>
  <strong> to: </strong> ${email["recipients"]}  
  <br>
  <strong> subject: </strong> ${email["subject"]}
  <br>
  <strong> timestamp: </strong> ${email["timestamp"]}
  <br>
  `
  mail_page.append(reply_button)
  if (email["archived"] ===  false){
  mail_page.append("    ")
  mail_page.append(archive_button)}
  else{
    console.log("in archive")
  }
  mail_page.append(rule)  
  mail_page.append(para)
  
  fetch(`/emails/${email["id"]}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })
}
function get_mail_page(mail_id){
  console.log("sending GET request...")
  fetch(`/emails/${mail_id}`)
  .then(response => response.json())
  .then(email => {mail_page(email)});
}



function display_mail(mail,mailbox){
  const new_line = document.createElement("br")
  const mail_container = document.createElement("div");
  mail_container.innerHTML = `<strong>${mail["sender"]}</strong> <br> <br><p> ${mail["subject"]}</p> 
                              <span class="timestamp">${mail["timestamp"]}</span>`;
  mail_container.className = "solid";
  if (mail["read"] === false & mailbox === 'inbox'){
    mail_container.style.backgroundColor = 'pink';
  }
  mail_container.dataset.mail_id = mail["id"]
  document.querySelector("#emails-view").append(mail_container)
  document.querySelector("#emails-view").append(new_line)
  document.querySelector("#emails-view").append(new_line)
}




function create_mail(){
  // create variables with the data
  recipients_data = document.querySelector("#compose-recipients").value
  subject_data = document.querySelector("#compose-subject").value
  body_data = document.querySelector("#compose-body").value


  // send the data
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients_data,
        subject: subject_data,
        body: body_data
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
  });
  return false;
}




function compose_email() {

  // Show compose view and hide other views
  document.querySelector("#mail-view").style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  


  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}



function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector("#mail-view").style.display = 'none';

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(result => result.forEach(mail =>{
    display_mail(mail,mailbox)
  }))
  .catch(error => 
    console.log("Error !",error)
  )
  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3 data-view=${mailbox}>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}
