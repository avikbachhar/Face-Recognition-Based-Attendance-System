function onloadtest(){
    $("#tbodyid").empty();




    markup = "<tr><td>This is row </td><td>"+ lineNo + "</td></tr>";
    $('#tb > tbody:last-child').append(markup);
  
}
function incrementDate(dateInput,increment) {
    var dateFormatTotime = new Date(dateInput);
    var increasedDate = new Date(dateFormatTotime.getTime() +(increment *86400000));
    return increasedDate;
}


function buttonpressed2(){
    console.log("Check Button 2 Clicked")
    var fdate = document.getElementById("From_Time").value;
    var tdate = document.getElementById("to_Time").value;
    var dept = document.getElementById("flight").value;
    var rollno = document.getElementById("rollno").value;
    var dateWith31 = new Date(tdate);
    dateWith31=incrementDate(dateWith31,1);
    tdate = dateWith31.getFullYear()+'-0'+(dateWith31.getMonth()+1)+'-'+dateWith31.getDate();
    console.log("From date : "+fdate);
    console.log("To date : "+tdate);
    console.log("Roll No : "+rollno);
    console.log(dept);
    var url = "http://127.0.0.1:5000/checkattendance";
    
    $.post(url,{
        fdate : fdate,
        tdate : tdate,
        dept : dept,
        rollno : rollno

    },function(data, status) {

        console.log("got response for department request");
        if(data) {
            var roll = data.db_rolls;
            var name = data.db_name;
            var count = data.db_count;
            var dep = data.db_dept;
            $('#tbodyid').empty();
            if (roll !=0){
                
            for (var i in roll){
                markup = "<tr><td>" +roll[i]+ "</td><td>"+ name[i] + "</td><td>" +count[i]+ "</td><td>"+ dep[i] + "</td></tr>";
                $('#tb > tbody:last-child').append(markup);
            }

            }
            else{
                markup = "<tr><td>" +"No"+ "</td><td>"+ "Student" + "</td><td>" +" Found"+ "</td><td>"+ " " + "</td></tr>";
                $('#tb > tbody:last-child').append(markup);
            }
        }
    });
}

function buttonpressed(){
    console.log("Check Button Clicked")
    var url = "http://127.0.0.1:5000/checkattendance";
    
    $.get(url,function(data, status) {
        console.log("got response for department request");
        if(data) {
            var roll = data.db_rolls;
            var name = data.db_name;
            var count = data.db_count;
            var dep = data.db_dept;
            $('#tbodyid').empty();
            for (var i in roll){
                markup = "<tr><td>" +roll[i]+ "</td><td>"+ name[i] + "</td><td>" +count[i]+ "</td><td>"+ dep[i] + "</td></tr>";
                $('#tb > tbody:last-child').append(markup);
            }
        }
    });
}


function onPageLoad() {
    $('#tbodyid').empty();
    var today = new Date();
    value = today.toISOString().substring(0, 10);
    console.log(value);
    document.getElementById("From_Time").value=value;
    document.getElementsByName("Book_Time")[0].max = value;
    document.getElementById("to_Time").value=value;
    document.getElementsByName("to_Time")[0].max = value;
    console.log( "document loaded" );
    var url = "http://127.0.0.1:5000/getdepartmentnames";
    $.get(url,function(data, status) {
        console.log("got response for department request");
        if(data) {
            var Department = data.Dept;
            var DeptID = data.DYear_ID;
            var flight = document.getElementById("flight");
            $('#flight').empty();
            var opt = new Option("Choose Department",0);
            $('#flight').append(opt);
            for(var i in Department) {
                var opt = new Option(Department[i],DeptID[i]);
                $('#flight').append(opt);
            }
        }
    });

  }

  
window.onload = onPageLoad;