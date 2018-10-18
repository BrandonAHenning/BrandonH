//////////////Define Objects and see if it working////////////////
console.log("It works!");

Input1 = document.querySelector("#Input1");
console.log("Input1 ", Input1);

Input2 = document.querySelector("#Input2");
console.log("Input2 ", Input2);

Input3 = document.querySelector("#Input3");
console.log("Input3 ", Input3);

Input4 = document.querySelector("#Input4");
console.log("Input4 ", Input4);

Input5 = document.querySelector("#Input5");
console.log("Input5 ", Input5);



var opsList = document.querySelector('#opsList');


var list_of_ops;

var opsClientInfo;

//////////////Create the Operartors Display Box////////////////





//////////////Create the Operartors Display Box////////////////

var pinOpsPaper = function(opsClientInfo) { //(Must be done through GET) <- SHOULD NOT BE DONE THROUGH GET
	
	var displayContainer = document.querySelector("#displayContainer")

	var opsContainer = document.createElement("div");

	var OpsHeaderContainer = document.createElement("div");
	var icon = document.createElement("div"); //UNQUIE
	var name = document.createElement("h3"); //UNQUIE

	var info1 = document.createElement("div");
	var info2 = document.createElement("div");
	var info3 = document.createElement("div");

	var country = document.createElement("span"); //UNQUIE
	var gadget = document.createElement("span"); //UNQUIE
	var weapon = document.createElement("span"); //UNQUIE

	var smallerIcon1 = document.createElement("div"); //UNQUIE
	var smallerIcon2 = document.createElement("div"); //UNQUIE
	var smallerIcon3 = document.createElement("div"); //UNQUIE

	var deleteButton = document.createElement("button")
	var editButton = document.createElement("button")

	//IMPORTANT YOU MUST APPEND A ID WHICH HAS THE UNQUIE ID OF
	//THE OPERATORS
	//SO YOU KEEP THE CLASS, BUT THEN MAKE THE ID
	//CHANGE THE BACKGROUND ID OF THE ICON
	//YOU ALSO NEED ID FOR THE TEXT SO THAT YOU
	//CAN USE THE INNER HTML
	//LASTLY YOU SHOULD THEN MAKE SCRIPT THAT AUTO GENERATE THE CSS FOR ALL
	//BACKGROUND ID PICTURES INTOT THE CSS. ACTUALLY
	//SCRATCH THAT. INSTEAD JUST USE THE URL BUT PUT INTO THE HTML
	//THAT THE MOST PROPER WAY TO DO IT. PUT THE PICTURE SRC INTOT THE
	//HTML OF EACH DIV

	opsContainer.className = "opsContainer";
	OpsHeaderContainer.className = "OpsHeaderContainer";
	icon.className = "icon"
	name.className = "name"

	info1.className = "info"
	info2.className = "info"
	info3.className = "info"

	country.className = "country"
	gadget.className = "gadget"
	weapon.className = "weapon"

	smallerIcon1.className = "smallerIcon"
	smallerIcon2.className = "smallerIcon"
	smallerIcon3.className = "smallerIcon"

	displayContainer.appendChild(opsContainer)

	opsContainer.appendChild(OpsHeaderContainer)
	OpsHeaderContainer.appendChild(icon)

	OpsHeaderContainer.appendChild(name)
	name.innerHTML = opsClientInfo['name'] //opsClientInfo is information submit by the 'form'

	opsContainer.appendChild(info1)
	info1.appendChild(country)
	country.innerHTML = opsClientInfo['country']
	info1.appendChild(smallerIcon1)

	opsContainer.appendChild(info2)
	info2.appendChild(gadget)
	gadget.innerHTML = opsClientInfo['gadget']
	info2.appendChild(smallerIcon2)

	opsContainer.appendChild(info3)
	info3.appendChild(weapon)
	weapon.innerHTML = opsClientInfo['weapon']
	info3.appendChild(smallerIcon3)

	opsContainer.appendChild(editButton)
	editButton.innerHTML = "EDIT"

	opsContainer.appendChild(deleteButton)
	deleteButton.innerHTML = "DELETE"

};

//////////////Read the Inputs and Modify////////////////

//////////////Read the Inputs and Creates////////////////


getInput = function(){
	opsClientInfo = {
	"name": Input1.value,
	"country": Input2.value,
	"gadget": Input3.value,
	"weapon": Input4.value,
	"age": Input5.value
	}
	console.log("All the Ops Info: ", opsClientInfo)
}

Create.onclick = function(){
	getInput()
	createOps(opsClientInfo)
	pinOpsPaper(opsClientInfo)
}

//////////////FETCH GET//////////////////

var getOps = function(opsClientInfo){
fetch("http://localhost:8080/operators").then(function (response) {
	response.json().then(function(theData){
	  	list_of_ops = theData;

		//UPDATE THE PAGE
		refreshPage(list_of_ops)
  	});
});
};

//////////////Create the Operartors Display Box////////////////

var createOps = function(opsClientInfo) {

	var Data = 'name=' + encodeURIComponent(opsClientInfo['name']) +
		'&country=' + encodeURIComponent(opsClientInfo['country']) +
		'&gadget=' + encodeURIComponent(opsClientInfo['gadget']) +
		'&weapon=' + encodeURIComponent(opsClientInfo['weapon']) +
		'&age=' + encodeURIComponent(opsClientInfo['age']);

	fetch("http://localhost:8080/operators",{
		method: "POST",
		body: Data,
		headers: {"content-type":"application/x-www-form-urlencoded"}
	}).then(function (response) {
		console.log("Cool, you were able create something:", Data)
		//YOU SENDING THE DATA IS CREATING IT. AS LONG YOU HAVE FUNCTION THAT CREATE ELEMENTS 
		//THIS WILL BE GOOD. YOU DON'T NEED PUT MUCH HERE, I THINK.
		//
		//UPDATE/REFRESH THE PAGE
  		});
};

/////////////////REFRESH THE PAGE//////////////////////////////
var refreshPage = function(list_of_ops){
	deleteDisplay()
	createDisplay(list_of_ops)
}

var createDisplay = function(list_of_ops){
	//Create the entire list
	
	for (i=0; i < list_of_ops.length; i++){
		console.log(list_of_ops[i])
		pinOpsPaper(list_of_ops[i])
		console.log("building ", i)
	}
	
	console.log('All the entrys has been created')
}

var deleteDisplay = function(){
	//Empty the entire list
	var opsList = document.querySelector("#displayContainer")
	while (opsList.firstChild){
		opsList.removeChild(opsList.firstChild)
	}
	console.log('All the entrys has been deleted')
}



////////RUN ON PAGE LOAD////////////

getOps()

