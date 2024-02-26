const submitBtn=document.querySelector("#submit");
const errorBlock=document.querySelector(".errorBlock");
const emailEmt=document.querySelector("#email");
const passwordEmt=document.querySelector("#password");
const form=document.querySelector("form");
const flash=document.querySelector(".server-msg");
const loader=document.querySelector(".loader");

submitBtn.addEventListener("click",async(evt)=>{
  if (form.checkValidity()) {
    evt.preventDefault();
  } else{
    return;
  }
  console.log("submit button is clicked");
  loader.style.display= "block";
  console.log(loader);
  password=passwordEmt.value;
  email=emailEmt.value;
  if (password.length<3){
    errorBlock.innerText="Password must be at least 3 characters long";
  } else {
    if (form.getAttribute("id")=="login-form"){
      await loginCredential(password,email);
    } else{
      const nameEmt= document.querySelector("#name");
      await registerCredential(nameEmt.value,email,password);
    }
  }
  loader.style.display = "none";
  setTimeout(()=>{
    errorBlock.innerText="";
  },5000)
});

async function loginCredential(password,email){
  try{
    const response= await fetch("/login",{
      method: "POST",
      headers: {
        "Content-Type":"application/json"
      },
      body: JSON.stringify({email:email, password:password})
    });
    if (!response.ok){
      throw new Error("Network response was not ok");
    }
    const data=  await response.json();
    if (data.valid){
      window.location.href= data.redirectUrl;
    } else {
      errorBlock.innerText=`${data.error}`;
    }
  } catch(err){
    console.log("Error occured",err);
    errorBlock.innerText="Error occured while processing your request";
  }

}

async function registerCredential(name,email,password){
  try{
    const response= await fetch("/register",{
      method: "POST",
      headers: {
        "Content-Type":"application/json"
      },
      body: JSON.stringify({name:name, email:email, password:password})
    });
    if (!response.ok){
      throw new Error("Network response was not ok");
    }
    const data=  await response.json();
    if (data.valid){
      window.location.href= data.redirectUrl;
    } else {
      errorBlock.innerText=`${data.error}`;
    }
  } catch(err){
    console.log("Error occured",err);
    errorBlock.innerText="Error occured while processing your request";
  }
}


// event listener to disapper flash message
document.addEventListener("DOMContentLoaded",()=>{
  setTimeout(()=>{
    flash.remove();
  },5000);
});
