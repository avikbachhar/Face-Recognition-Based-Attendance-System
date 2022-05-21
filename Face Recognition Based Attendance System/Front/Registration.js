const rollBtn1 = document.querySelector(".rolbut1 button");
const rollBtn2 = document.querySelector(".rolbut2 button");
console.log(rollBtn1)
var i = 0;

function checkDetails1(){
    console.log("Check Details Clicked");
    var roll = document.getElementById("rollinput").value;
    console.log(roll);
    var first_name = document.getElementById("fname");
    var last_name = document.getElementById("lname");
    first_name.value = "Avik";
    last_name.value = "Bachhar";
    document.getElementById("profileImage").src="Photo Original.jpg";
    document.getElementById("fname").disabled = true;
    document.getElementById("lname").disabled = true;
    rollBtn1.classList.add("deactive");
    rollBtn2.classList.add("active");

}

function checkDetails() {
  console.log("Check Details Clicked");
  if(i==0){
    
  
    var roll = document.getElementById("rollinput").value;
  var url = "http://127.0.0.1:5000/checkdetails"; 
  $.post(url, {
      id : roll,
  },function(data, status) {
    var first_name = document.getElementById("fname");
    var last_name = document.getElementById("lname");
    first_name.value = data.fname;
    last_name.value = data.lname;
      console.log(status);
    document.getElementById("fname").disabled = true;
    document.getElementById("lname").disabled = true;
    console.log("Calling Imgae Function");
    var imgdata="http://127.0.0.1:5000/getImage/roll";
    document.getElementById("profileImage").src = imgdata;
    document.getElementById("check-btn").innerHTML="Reload";
    i+=1;
  });
}
else{
  Reload();
}
}

function Reload(){
  location.reload();
}

function checkDetails3() {
  console.log("Check Details Clicked");
  var roll = document.getElementById("rollinput").value;
  var url = "http://127.0.0.1:5000/checkdetails"; 
  $.post(url, {id : roll,},function(data, status) {
    if(data.Ststatus==1){
      var first_name = document.getElementById("fname");
      var last_name = document.getElementById("lname");
      var d_name = document.getElementById("dname");
      first_name.value = data.fname;
      last_name.value = data.lname;
      d_name.value=data.dname
      var img_base = data.img;
      var final = ('data:image/jpg;base64,'+img_base);
      document.getElementById("profileImage").src =final;  
    }
    else{
      alert("Error Found");
      location.reload();
    }
     }).fail(function(jqXHR, textStatus, errorThrown){
      alert("Error Found");
});

}



