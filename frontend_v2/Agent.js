class Agent {
  constructor(id, x = 0, y = 0, r = 1) {
    this.x = x
    this.y = y
    this.r = r*scale_unit
    this.vision = this.r*10*2
    this.colour = colours[id]
    this.rgb = hexToRgb(this.colour)
    this.colour_alpha = color(this.rgb.r, this.rgb.g, this.rgb.b, 25)
    this.id = id
    this.targets_found = ["_", "_", "_", "_", "_"]
    this.xoff = random(100000)
    this.yoff = random(100000)
    this.vision_trail = createGraphics(scale_unit*100, scale_unit*100)
    this.frame_counter = 0
  }

  draw() {
    this.frame_counter++

    fill(this.colour)
    noStroke()
    ellipseMode(CENTER)
    ellipse(this.x, this.y, this.r)

    if(verbose) {
      stroke(this.colour)
      fill("#333")
      text(`ID: ${this.id}\n Colour: ${this.colour}`, this.x, this.y - 30)
      noFill()
      fill(this.colour_alpha)
      ellipse(this.x, this.y, this.vision);
    }

    if(this.frame_counter % frame_rate == 0 && trail){
      this.vision_trail.fill(this.colour_alpha)
      this.vision_trail.noStroke()
      this.vision_trail.ellipseMode(CENTER)
      this.vision_trail.ellipse(this.x/2, this.y/2, this.vision/2)
      tint(255, 25)
    }
    imageMode(CORNER)
    image(this.vision_trail, 0, 0, 600, 600)
    noTint()

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
