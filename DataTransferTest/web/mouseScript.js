
            eel.expose(fromJsToPY);
            function fromJsToPY(x){
                console.log("hello from " + x)
            }
            
            eel.fromPyToJS("JS");