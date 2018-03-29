class Agent {
  constructor(id, x = 0, y = 0, r = 1) {
    this.x = x;
    this.y = y;
    this.r = r*scale_unit;
    this.colour = colours[id];
    this.id = id;
    this.targets_found = []
  }

  draw() {
    fill(this.colour)
    noStroke()
    ellipseMode(CENTER)
    ellipse(this.x, this.y, this.r)

    if(verbose) {
      stroke(this.colour)
      noFill()
      ellipse(this.x, this.y, this.r*10);
      // text(`ID: ${this.id}\nX: ${this.x}\nY: ${this.y}`, this.x, this.y - 30);
    }
  }

  display_info(){
    let title_span = DOM_objects.Agent.Title
    let x_pos_span = DOM_objects.Agent.X
    let y_pos_span = DOM_objects.Agent.Y
    let targets_found_span = DOM_objects.Agent.Targets_Found

    title_span.html(`Agent #${this.id + 1}`)
    x_pos_span.html(`x: ${this.x}`)
    y_pos_span.html(`y: ${this.y}`)
    targets_found_span.html(`Targets: [_,_,_,_,_]`)
  }
}
