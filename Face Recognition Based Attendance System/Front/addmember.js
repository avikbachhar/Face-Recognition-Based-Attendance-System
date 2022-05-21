var url1 = '';

function previewFile() {
    var preview = document.querySelector('img');
    var file    = document.querySelector('input[type=file]').files[0];
    var reader  = new FileReader();
  
    reader.onloadend = function () {
      preview.src = reader.result;
      url1 = reader.result;
    }
  
    if (file) {
      reader.readAsDataURL(file);
    } else {
      preview.src = "";
    }
  }

  function buttonpressed(){
      console.log("Test Done");

      var fname = document.getElementById('fname').value;
      var rollno = document.getElementById('rollno').value;  
      var lname = document.getElementById('lname').value;
      var depID = document.getElementById('flight').value;
      if(fname!='' && lname!='' &&rollno!='' && url1!=''){
      console.log(url1);
      console.log(fname);
      console.log(lname);
      console.log(rollno);
      console.log(depID);
      addStudentApi(fname,lname,rollno,depID,url1)
      }
      else{
        alert("Enter Details Please");
      }
  }



















  function addStudentApi(fname,lname,rollno,depID,img){
    var url = "http://127.0.0.1:5000/addstudentdetails";
    $.post(url, {
        fname : fname,
        lname : lname,
        rollno : rollno,
        depID : depID,
        img : img
    },function(data, status) { 
        if(data.Ststatus==0){
            alert(data.message);
        }
        else{
            alert(data.message);
        }
    }).fail(function(jqXHR, textStatus, errorThrown){
        alert("Error Occured");
    });
}



  function onPageLoad() {
    console.log( "document loaded" );
    var url = "http://127.0.0.1:5000/getdepartmentnames";
    $.get(url,function(data, status) {
        console.log("got response for department request");
        if(data) {
            var Department = data.Dept;
            var DeptID = data.DYear_ID;
            var flight = document.getElementById("flight");
            $('#flight').empty();
            var opt = new Option("-- Select --",0);
            $('#flight').append(opt);
            for(var i in Department) {
                var opt = new Option(Department[i],DeptID[i]);
                $('#flight').append(opt);
            }
        }
    });
  }

  
window.onload = onPageLoad;