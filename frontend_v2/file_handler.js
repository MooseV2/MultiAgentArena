function handleFileSelect(evt) {
    evt.stopPropagation();
    evt.preventDefault();

    let files = evt.dataTransfer.files; // FileList object.
    // files is a FileList of File objects. List some properties.
    var output = [];
    if (!files.length > 0) // No actual file
        return;

    let file = files[0]; // Grab first file
    let reader = new FileReader();
    reader.onload = ((file) => {
        return (e) => {
            let contents = reader.result.split('\n');
            // Do whatever with contents (array of text lines)
            parseSimulation(contents);
        }
    })(file);
    reader.readAsText(file);
}

function parseSimulation(contents) {
    let simulation = [];
    for (let line of contents) {
        let splitLine = line.split(',');
        console.log(splitLine);
    }
}

function handleDragOver(evt) {
    evt.stopPropagation();
    evt.preventDefault();
    evt.dataTransfer.dropEffect = 'link'; // Explicitly show this is a copy.
}

// Setup the dnd listeners.
let dropZone = document.getElementById('thebody');
dropZone.addEventListener('dragover', handleDragOver, false);
dropZone.addEventListener('drop', handleFileSelect, false);