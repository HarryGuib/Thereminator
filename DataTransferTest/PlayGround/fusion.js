let X = 0;
let Y = 0;
function initialize(){
	if (navigator.requestMIDIAccess) {
		navigator.requestMIDIAccess()
			.then(success, failure);
	}

	// Initialisiert WebMIDI
	function success (midi) {
		createUI(midi.inputs);

		// liefert Liste der MIDI-Input Ports
		function findInputPort(name){
			let selectedInput = null;
			midi.inputs.forEach(function(input, key){
				if (input.name == name){
					selectedInput = input;
				}
			});
			return selectedInput;
		}

		// initialisiert einen MIDI-Input Port 
		function initializeInputPort(name){
			const input = findInputPort(name);
			if (input){
				input.addEventListener('midimessage', onMIDIMessage);
			}
		}

		
		// erzeugt Dropdown-Menü mit MIDI-Input Ports
		function createUI(inputs){
			inputs.forEach(function(input, key){
				let opt = document.createElement("option");
				opt.text = input.name;
				document.getElementById("inputportselector").add(opt);
			});

			// document.getElementById("connectbutton").addEventListener("click", onConnect);
			// function onConnect(){
				var optionsMenu = document.getElementById("inputportselector");
				var portName = optionsMenu.options[optionsMenu.selectedIndex].text;		
				initializeInputPort(portName);
			//}
		}	
	}
	
	function failure () {
		console.error('No access to your midi devices.')
	}

	// MIDI-Input Eventhandler
	function onMIDIMessage(event){
		let string = "";
		let res;

		for (byte of event.data){
			// string += byte.toString(7) + " " + byte.toString(16);
			string += byte.toString(10) + " ";
			res = string.split(" ");
			X = res[1];
			Y = res[2];
		}
		//console.log("X: "+res[1]+" Y:"+res[2]);
		// Darstellung der MIDI-Strings im Textfeld
		document.getElementById("label").innerHTML = string;
		
	}
}
let maxFreq = 2000;
let mouseDown=false;

let context = new AudioContext();

let oscillatorNode = context.createOscillator();
let gainNode = context.createGain();

oscillatorNode.start();


let freq = function(mouseX){
    return((mouseX/127)*maxFreq);
}

let vol = function(mouseY){
    return((mouseY/127));
}
function onStart()
{
	oscillatorNode.connect(gainNode);
    gainNode.connect(context.destination);
}

function onStop()
{
	oscillatorNode.disconnect(gainNode);
    gainNode.disconnect(context.destination);
    //oscillatorNode.stop(context.currentTime+0.01);
}

document.getElementById("start").addEventListener("click", onStart);
document.getElementById("stop").addEventListener("click", onStop);

// document.addEventListener("mousemove", function (e) {
// if (mouseDown){
	setInterval(function(){ 
		console.log("X: "+X+ " Y: "+Y)
		marker(X,Y)
		oscillatorNode.frequency.setTargetAtTime(freq(X),context.currentTime,0.01);
		gainNode.gain.setTargetAtTime(vol(Y),context.currentTime,0.01);
	}, 20);

// }
// })
// document.addEventListener("mouseup",function(e){
//     mouseDown=false;
//     oscillatorNode.disconnect(gainNode);
//     gainNode.disconnect(context.destination);

//     //oscillatorNode.stop(context.currentTime+0.01);

// })

// document.addEventListener("mousedown", function(e){

//     mouseDown=true;
//     oscillatorNode.connect(gainNode);
//     gainNode.connect(context.destination);

// })

// ======== Marker =================
function marker (x,y)
{
	var canvas = document.getElementById("myCanvas");
	var ctx = canvas.getContext("2d");
	if (!document.getElementById("trail").checked)
	{
		ctx.clearRect(0,0,canvas.clientWidth,canvas.clientHeight);
	}
	ctx.beginPath();
	ctx.arc((x/128) * 500,(y/128)*500 ,10,0,2*Math.PI);
	ctx.fillStyle = "rgb(255,"+(x*2+1)+","+(y*2+1)+")";
	ctx.fill();
}

//====================================

