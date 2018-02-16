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
  constructor(x, y) {
    this.x = x;
    this.y = y;
    this.r = 10;
    this.colorID = ColorWheel.colorAssignment;
  }

  draw() {
    fill(ColorWheel.color(this.colorID));
    ellipseMode(CENTER);
    ellipse(this.x, this.y, this.r)
    noFill();
    if (distance(mouseX, mouseY, this.x, this.y) < 15) {
      ellipse(this.x, this.y, this.r*10);
    }
  }
};

let objects = [];
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

function setup() {
  createCanvas(720, 400);
  ws = new WebSocketClient();
  setupColors();
  for (let i=0; i<5; ++i) {
    c = new Agent(50 + 30*i, 100);
    objects.push(c);
  }

  objects.push(new Grid(20, 20));
    
}
function draw() {
  background(255);
  for (let instance of objects)
    instance.draw();
}

// reset board when mouse is pressed
function mousePressed() {
  
}