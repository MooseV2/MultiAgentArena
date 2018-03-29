class Agent {
  constructor(id, x = 0, y = 0, r = 1) {
    this.x = x
    this.y = y
    this.r = r*scale_unit
    this.vision = this.r*10
    this.colour = colours[id]
    this.id = id
    this.targets_found = []
    this.xoff = random(100000)
    this.yoff = random(100000)
  }

  draw() {
    fill(this.colour)
    noStroke()
    ellipseMode(CENTER)
    ellipse(this.x, this.y, this.r)

    if(verbose) {
      stroke(this.colour)
      noFill()
      ellipse(this.x, this.y, this.vision);
      text(`ID: ${this.id}\n Colour: ${this.colour}`, this.x, this.y - 30);
    }
    this.generate_noise()
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

  // Agent movement range is from (42, 42) => (558, 558)
  // Make sure all movement is within that range
  generate_noise(){
      this.x = int(map(noise(this.xoff), 0, 1, 42, 558))
      this.y = int(map(noise(this.yoff), 0, 1, 42, 558))
      this.xoff += 0.005
      this.yoff += 0.005
  }

  check_target(agent_targets){
    agent_targets.map((target) => {
      if(dist(target.x, target.y, this.x, this.y) <= this.vision){
        console.log(dist(target.x, target.y, this.x, this.y))
        noLoop()
        remove_from_array(targets[this.id], target)
        remove_from_array(objects, target)
      }
    })
  }
}
