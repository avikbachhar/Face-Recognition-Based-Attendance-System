let newLiTag = "";
let i = 0;
const students = [];
function onClickedEstimatePrice1() {
    removeAll()
    console.log("Estimate price button clicked");
    element="Student" + i; 
    students.push(element); 
    let fLen = students.length; 
    for (let i = 0; i < fLen; i++) {
    newLiTag += `<li> Attendance Marked for ${students[i]}</li>`;
    todoList.innerHTML = newLiTag;
    }
    i++;
}
function removeAll(){
    console.log("Remove button clicked");
    document.getElementById("todoList").innerHTML = "";
    $("#todoList").html("");
}


function cameraOff(){
  var url = "http://127.0.0.1:5000/video-terminate";
  $.get(url,function(data, status) {
      console.log("got response for department request");
  });
  document.getElementById("myImg").src = "compman.gif";
  stopTimer();
}
function cameraOn(){
  document.getElementById("myImg").src = "http://127.0.0.1:5000/video";
  startTimer();
}

function imgError(){
  stopTimer();
}

function loadImage(){
  console.log("Streaming..");
}


function onClickedEstimatePrice2() { //when user click on plus icon button
    element="Student" + i; 
    i++;
    let userEnteredValue = element; //getting input field value
    let getLocalStorageData = localStorage.getItem("New Todo"); //getting localstorage
    if(getLocalStorageData == null){ //if localstorage has no data
      listArray = []; //create a blank array
    }else{
      listArray = JSON.parse(getLocalStorageData);  //transforming json string into a js object
    }
    listArray.push(userEnteredValue); //pushing or adding new value in array
    localStorage.setItem("New Todo", JSON.stringify(listArray)); //transforming js object into a json string
    showTasks(); //calling showTask function
    
  }

  

  function onClickedEstimatePrice3(element) { //when user click on plus icon button
    let userEnteredValue = element; //getting input field value
    let getLocalStorageData = localStorage.getItem("New Todo"); //getting localstorage
    if(getLocalStorageData == null){ //if localstorage has no data
      listArray = []; //create a blank array
    }else{
      listArray = JSON.parse(getLocalStorageData);  //transforming json string into a js object
    }
    listArray.push(userEnteredValue); //pushing or adding new value in array
    localStorage.setItem("New Todo", JSON.stringify(listArray)); //transforming js object into a json string
    showTasks(); //calling showTask function
    
  }


  function showTasks(){
    let getLocalStorageData = localStorage.getItem("New Todo");
    if(getLocalStorageData == null){
      listArray = [];
    }else{
      listArray = JSON.parse(getLocalStorageData); 
    }
    let newLiTag = "";
    listArray.forEach((element, index) => {
      newLiTag += `<li>${element}<span class="icon" onclick="deleteTask(${index})"><i class="fas fa-trash"></i></span></li>`;
    });
    todoList.innerHTML = newLiTag; //adding new li tag inside ul tag
  }
  function deleteTask(index){
    let getLocalStorageData = localStorage.getItem("New Todo");
    listArray = JSON.parse(getLocalStorageData);
    listArray.splice(index, 1); //delete or remove the li
    localStorage.setItem("New Todo", JSON.stringify(listArray));
    showTasks(); //call the showTasks function
  }
  // delete all tasks function
  function emptyStudentList2(){
    listArray = []; //empty the array
    localStorage.setItem("New Todo", JSON.stringify(listArray)); //set the item in localstorage
    showTasks(); //call the showTasks function
  }
  function emptyStudentList1(){
    students = [];
    showTasks(); //call the showTasks function
  }

  function IterateList(){
    const students2=['Utsab Roy', 'Souvik Das', 'Sayantan Banerjee', 'Sayak Basu', 'SOUVIK PAUL', 'SUBHORUP SARKAR', 'Abhay Anand', 'Abu Faishal', 'AVINANDAN BOSE', 'Debasish Ghosh', 'Mahboob Alam', 'AVIK BACHHAR', 'SAYAK ADITYA', 'SOUVIK BERA', 'DEBJYOTI MONDAL', 'RAKESH DEY', 'Suman Maity', 'Biman Hazra', 'ESHITA CHAKRABORTY', 'ROHAN SARKAR', 'SUBHAJIT DEY', 'DEEPTARAGH ROY', 'UPAMANNYU SAIN', 'Arnab Ojha', 'AVIJIT SINGH', 'PANKAJ JANA', 'Suman Dey', 'SUBHAJIT DAS', 'Adarsh Ram', 'Nuruddin Ahmed', 'Usop Ali', 'Atanu Mondal', 'Bitan Mandal', 'Sanskar Shaw', 'ANANT YADAV', 'ANINDITA SARKAR', 'DEBOPRIYA KARMAKAR', 'DEBOLINA KUNDU', 'Priyanka Malakar', 'SUDIPA BHOWMIK', 'OLIVIA MONDAL', 'TIASA CHAKRABORTY', 'B Deepika', 'SUJATA SHAW', 'Bratati Roy', 'Amrita Mandal', 'Saswati Sinha', 'PRIYANGANA ROY', 'BANDITA LENKA', 'SOHINI BISWAS', 'Payel Mondal', 'SANJUKTA SINHA', 'MOMITA MUKHERJEE', 'KRITI SHARMA', 'Alina Kashyap', 'Shreya Mondal', 'Shrabana Sengupta', 'Sumana Santra', 'PRITHA DAS']
    let fLen = students2.length; 
    for (let i = 0; i < fLen; i++) {
        onClickedEstimatePrice3(students2[i]);
    }
  }
  

var namelen = 0;
  function studentlist(){
 
      var url = "http://127.0.0.1:5000/attendes";
      $.get(url,function(data, status) {
        console.log("got response for names");
        if(data) {
            var name = data.studentnames;
            let length = name.length;
            if(namelen != length){
              for(var i in name) {
                console.log(name[i]);
            }
            emptyStudentList2();
            namelen=length;
            for (let i = 0; i < length; i++) {
                onClickedEstimatePrice3(name[i]);
            }
            }
            else{
              console.log("NO NEW STUDENT")
            }
    
        }
    });
    }

    var timer;
  function startTimer() {
      timer = setInterval(function() {
        studentlist();
      }, 3000);
  }
   
  function stopTimer() {
      clearInterval(timer);
  }
window.onload=startTimer();

function myFunction() {
  return "Write something clever here...";
}