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
    this.targets_found = []
    this.targets_found_id = new Array(5).fill('_')
    this.xoff = random(100000)
    this.yoff = random(100000)
    this.vision_trail = createGraphics(scale_unit*100, scale_unit*100)
    this.frame_counter = 0
    this.last_x = null
    this.last_y = null
    this.destination = null
    this.stage = 0
  }

  draw() {
    this.frame_counter++

    if(iterations != 0){
      this.x = int(iterations[iteration][this.id].X * scale_unit)
      this.y = int(iterations[iteration][this.id].Y * scale_unit)
    }

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

    if(this.frame_counter % 5 == 0 && trail){
      this.vision_trail.fill(this.colour_alpha)
      this.vision_trail.noStroke()
      this.vision_trail.ellipseMode(CENTER)
      this.vision_trail.ellipse(this.x/2, this.y/2, this.vision/2)
      tint(255, 25)

      this.vision_trail.stroke(this.colour)
      this.vision_trail.fill(this.colour)
      if(this.last_x == null){
        this.last_x = this.x/2
        this.last_y = this.y/2
        this.vision_trail.point(this.last_x, this.last_y, this.r)
      } else {
        this.vision_trail.line(this.x/2, this.y/2, this.last_x, this.last_y)
        // this.vision_trail.point(this.last_x, this.last_y, this.r)
        this.last_x = this.x/2
        this.last_y = this.y/2
      }
    }
    imageMode(CORNER)
    image(this.vision_trail, 0, 0, 600, 600)
    noTint()

    // this.decision()

    // this.generate_noise()
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
    targets_found_span.html(`Targets: [${this.targets_found_id.toString()}]`)
  }

  // Agent movement range is from (42, 42) => (558, 558)
  // Make sure all movement is within that range
  generate_noise(){
      this.x = int(map(noise(this.xoff), 0, 1, 42, 558))
      this.y = int(map(noise(this.yoff), 0, 1, 42, 558))
      this.xoff += 0.005
      this.yoff += 0.005
  }

  decision() {
    switch(this.stage){
      case 0:
        if(this.destination == null){
          this.destination = {x: int((scale_unit*100-agent_reach)/2), y: int((scale_unit*100-agent_reach)/2)}
        }
        this.move_towards(this.destination.x, this.destination.y)
        break
      default:
        break
    }
  }

  move_towards(destx, desty){
    this.x += this.direction(this.x, destx)
    this.y += this.direction(this.y, desty)
  }

  direction(startpoint, endpoint){
    if(endpoint == startpoint)
      return 0

    if(endpoint < startpoint){
      return -1
    } else {
      return 1
    }
  }

  check_target(agent_targets){
    agent_targets.map((target) => {
      if(target.visible && (dist(target.x, target.y, this.x, this.y) <= this.vision/2)){
        target.bloom()
        this.target_found(target)
        // remove_from_array(targets[this.id], target)
        // remove_from_array(objects, target)
        target.visible = false
      }
    })
  }

  target_found(target){
    let index = this.targets_found_id.indexOf('_')
    this.targets_found[index] = target
    this.targets_found_id[index] = target.target_id
  }
}
