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

			document.getElementById("connectbutton").addEventListener("click", onConnect);
			function onConnect(){
				var optionsMenu = document.getElementById("inputportselector");
				var portName = optionsMenu.options[optionsMenu.selectedIndex].text;
		
				initializeInputPort(portName);
			}
		}
	
	}
	
	function failure () {
		console.error('No access to your midi devices.')
	}

	// MIDI-Input Eventhandler
	function onMIDIMessage(event){
		let string = "";
		for (byte of event.data){
			// string += byte.toString(7) + " " + byte.toString(16);
			string += byte.toString(16) + " ";
		}
		// Darstellung der MIDI-Strings im Textfeld
		document.getElementById("label").innerHTML = string;
		
	}
}