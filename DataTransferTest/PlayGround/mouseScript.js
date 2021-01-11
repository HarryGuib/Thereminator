
let maxFreq = 2000;
let mouseDown=false;

let context = new AudioContext();

let oscillatorNode = context.createOscillator();
let gainNode = context.createGain();

oscillatorNode.start();


let freq = function(mouseX){
    return((mouseX/innerWidth)*maxFreq);
}

let vol = function(mouseY){
    return((mouseY/innerHeight));
}




document.addEventListener("mousemove", function (e) {
if (mouseDown){
    oscillatorNode.frequency.setTargetAtTime(freq(e.clientX),context.currentTime,0.01);
    gainNode.gain.setTargetAtTime(vol(e.clientY),context.currentTime,0.01);
}
})



document.addEventListener("mouseup",function(e){
    mouseDown=false;
    oscillatorNode.disconnect(gainNode);
    gainNode.disconnect(context.destination);

    //oscillatorNode.stop(context.currentTime+0.01);

})


document.addEventListener("mousedown", function(e){

    mouseDown=true;

    oscillatorNode.connect(gainNode);
    gainNode.connect(context.destination);

    

})

