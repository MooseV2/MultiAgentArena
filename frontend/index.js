let distance = (x0, y0, x1, y1) => {
  return Math.sqrt(Math.pow(y1-y0, 2) + Math.pow(x1-x0, 2));
}

var objects;
let c;
// Make sure Agents are 1 unit, Radius is 10 units, and Width/Height is 100 units
let scale_unit = 8;
// Reset button
let reset_button;

let ColorWheel;
let setupColors = () => {
  ColorWheel = {
    index: 1,
    get colorAssignment() {
      return this.index++;
    },
    color: (id) => {
      colorMode(HSB, 255);
      return color(255-id/ColorWheel.index*255, 255, 255);
    }
  }  
}

function objectSetup() {
  objects = [];
  objects[0] = new Grid(scale_unit, scale_unit);
}

function setup() {
  document.querySelector('#conn-status').innerHTML = 'Disconnected';
  let canvas = createCanvas(scale_unit*100, scale_unit*100);
  canvas.parent("sketch_wrapper")
  objectSetup();
  ws = new WebSocketClient(parseCommand);
  setupColors();
  reset_button = createButton('Reset');
}

function draw() {
  background(255);
  for (let instance of objects) {
    if (instance)
      instance.draw();
  }

  reset_button.mousePressed(testButton);
}

function testButton() {
  createDiv("Reset made this");
}

// reset board when mouse is pressed
function mousePressed() {

}

function parseCommand(data) {
  switch (data['cmd']) {
    case 'create': commandCreate(data['type'], data['id'], data['args']); break;
    case 'reset': commandReset(); break;
    case 'move': commandMoveAgent(data['id'], data['args']); break;
    default: console.log(`Unknown command: ${data['cmd']}`); break;
  }
}

function commandCreate(item_type, id, args) {
  // TODO: Failsafe
  let objectTypes = {
    "Agent": Agent,
    "Target": Target
  }
  console.log(item_type);
  let obj = new objectTypes[item_type](id, args);
  objects[id] = obj;
}

function commandMoveAgent(id, {x = 0, y = 0}) {
  if (id == null) return;
  objects[id].x = x;
  objects[id].y = y;
}

function commandReset() {
  objectSetup();
}