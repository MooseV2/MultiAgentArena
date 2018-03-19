class Target {
  constructor(id, {x = 0, y = 0, r = 1, colorID = ColorWheel.colorAssignment}) {
    this.x = x;
    this.y = y;
    this.r = r*scale_unit;
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