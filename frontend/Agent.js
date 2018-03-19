class Agent {
  constructor(id, {x = 0, y = 0, r = 1, colorID = ColorWheel.colorAssignment}) {
    this.x = x;
    this.y = y;
    this.r = r*scale_unit;
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
