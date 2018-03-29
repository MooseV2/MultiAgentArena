class Target {
  constructor(id, target_id, x = 0, y = 0, r = 1) {
    this.x = x
    this.y = y
    this.r = r*scale_unit
    this.id = id
    this.colour = colours[id]
    this.target_id = target_id
  }

  draw() {
    fill(this.colour);
    stroke(this.colour)
    ellipseMode(CENTER);
    rect(this.x - this.r/2, this.y+this.r/2, this.r, this.r);
    text(this.target_id + 1, this.x, this.y)
    noFill();
    if (dist(mouseX, mouseY, this.x, this.y) < 15) {
      ellipse(this.x, this.y, this.r*10);
    }
  }

  display_info(){
    stroke(this.colour)
    text(`ID: ${this.id}\n Colour: ${this.colour}`, this.x, this.y - 30);
  }
}