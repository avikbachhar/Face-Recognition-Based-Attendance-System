function onclickAddDepartment(){
    console.log("Add Department Clicked");
    var d_name = document.getElementById("dname").value;
    if(d_name !=''){
    console.log(d_name);
    var e = document.getElementById("year").value;
    console.log(e);
    addDeptApi(d_name,e);
    }
    else{
        document.getElementById('dlabel').innerHTML= "<label id='dlabel' style='color: red;' style='background-color=white';>Add Department Name</label>";
    }
}

function addDeptApi(dname,dyear){
    var url = "http://127.0.0.1:5000/adddepartments";
    $.post(url, {
        dname : dname,
        dyear : dyear
    },function(data, status) { 
        if(data.Ststatus==0){
            alert(data.message);
            onPageLoad();
        }
        else{
            alert(data.message);
        }
    }).fail(function(jqXHR, textStatus, errorThrown){
        alert("Error Occured");
    });
}

function onPageLoad1() {
    console.log( "document loaded" );
    var url = "http://127.0.0.1:5000/adddepartments";
    $.get(url,function(data, status) {
        console.log("got response for department request");
        if(data) {
            var Dept = data.Dept;
            var Year = data.Year;
            console.log(Dept);
            console.log(Year);
            $("#tbodyid").empty();
            for(var i in Dept) {
                markup = "<tr><td>"+Dept[i]+ "</td><td>"+ Year[i] + "</td></tr>";
                $('#tb > tbody:last-child').append(markup);
            }
        }
    });
    console.log("Added Departments")
  }


function onPageLoad() {
    console.log( "document loaded" );
    var url = "http://127.0.0.1:5000/getdepartments";
    $("#tbodyid").empty();
    $.get(url,function(data, status) {
        console.log("got response for department request");
        if(data) {
            var Dept = data.Dept;
            var Year = data.Year;
            console.log(Dept);
            console.log(Year);
            $("#tbodyid").empty();
            for(var i in Dept) {
                markup = "<tr><td>"+Dept[i]+ "</td><td>"+ Year[i] + "</td></tr>";
                $('#tb > tbody:last-child').append(markup);
            }
            console.log("Added Departments")
        }
        else{
            alert("Loading Failed Contact Admin");
        }

    }).fail(function(jqXHR, textStatus, errorThrown){
        $("#tbodyid").empty();
        alert("Error Occured");

    });
  }



window.onload = onPageLoad();

