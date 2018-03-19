let distance = (x0, y0, x1, y1) => {
  return Math.sqrt(Math.pow(y1-y0, 2) + Math.pow(x1-x0, 2));
}


class Grid {
  constructor(w, h) {
    this.w = w;
    this.h = h;
  }
  
  draw() {
    for (let x=0; x<displayWidth; x+=this.w)
      line(x, 0, x, displayHeight);
    
    for (let y=0; y<displayHeight; y+=this.h)
      line(0, y, displayWidth, y);
  }
}

class Agent {
  constructor(id, {x = 0, y = 0, r = 10, colorID = ColorWheel.colorAssignment}) {
    this.x = x;
    this.y = y;
    this.r = r;
    this.colorID = colorID;
    this.id = id;
  }

  draw() {
    fill(ColorWheel.color(this.colorID));
    ellipseMode(CENTER);
    ellipse(this.x, this.y, this.r)
    noFill();
    if (distance(mouseX, mouseY, this.x, this.y) < 15) {
      ellipse(this.x, this.y, this.r*10);
      fill(0, 0, 0);
      text(`ID: ${this.id}\nX: ${this.x}\nY: ${this.y}`, this.x, this.y - 30);
    }
  }
};

class Target {
  constructor(id, {x = 0, y = 0, r = 10, colorID = ColorWheel.colorAssignment}) {
    this.x = x;
    this.y = y;
    this.r = r;
    this.id = id;
    this.colorID = colorID;
  }

  draw() {
    fill(ColorWheel.color(this.colorID));
    ellipseMode(CENTER);
    rect(this.x - this.r/2, this.y+this.r/2, this.r, this.r);
    noFill();
    if (distance(mouseX, mouseY, this.x, this.y) < 15) {
      ellipse(this.x, this.y, this.r*10);
    }
  }
};

var objects;
let c;

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
  objects[0] = new Grid(20, 20);
}

function setup() {
  document.querySelector('#conn-status').innerHTML = 'Disconnected';
  createCanvas(720, 400);
  objectSetup();
  ws = new WebSocketClient(parseCommand);
  setupColors();
  
}
function draw() {
  background(255);
  for (let instance of objects) {
    if (instance)
      instance.draw();
  }
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