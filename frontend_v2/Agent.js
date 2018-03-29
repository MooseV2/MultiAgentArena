class Agent {
  constructor(id, x = 0, y = 0, r = 1) {
    this.x = x
    this.y = y
    this.r = r*scale_unit
    this.vision = this.r*10*2
    this.colour = colours[id]
    this.rgb = hexToRgb(this.colour)
    this.colour_alpha = color(this.rgb.r, this.rgb.g, this.rgb.b, 50)
    this.id = id
    this.targets_found = ["_", "_", "_", "_", "_"]
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
      text(`ID: ${this.id}\n Colour: ${this.colour}`, this.x, this.y - 30);
      noFill()
      fill(this.colour_alpha)
      ellipse(this.x, this.y, this.vision);
    }

    // trail_canvas.noStroke()
    // trail_canvas.fill(this.colour_alpha)
    // trail_canvas.ellipseMode(CENTER)
    // trail_canvas.ellipse(this.x, this.y, this.vision)

    this.generate_noise()
  }

  display_info(){
    current_agent_info = this
    let title_span = DOM_objects.Agent.Title
    let x_pos_span = DOM_objects.Agent.X
    let y_pos_span = DOM_objects.Agent.Y
    let targets_found_span = DOM_objects.Agent.Targets_Found

    title_span.html(`Agent #${this.id + 1}`)
    x_pos_span.html(`x: ${int(this.x)}`)
    y_pos_span.html(`y: ${int(this.y)}`)
    targets_found_span.html(`Targets: [${this.targets_found.toString()}]`)
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
      if(dist(target.x, target.y, this.x, this.y) <= this.vision/2){
        target.bloom()
        this.target_found(target)
        remove_from_array(targets[this.id], target)
        remove_from_array(objects, target)
      }
    })
  }

  target_found(target){
    let index = this.targets_found.indexOf('_')
    this.targets_found[index] = target.target_id + 1
  }
}
