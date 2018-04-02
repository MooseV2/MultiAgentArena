class Target {
  constructor(id, target_id, x = 0, y = 0, r = 1) {
    this.x = x
    this.y = y
    this.r = r*scale_unit
    this.id = id
    this.colour = colours[id]
    this.rgb = hexToRgb(this.colour)
    this.alpha = 75
    this.colour_alpha = color(this.rgb.r, this.rgb.g, this.rgb.b, alpha)
    this.target_id = target_id
  }

  draw() {
    fill(this.colour)
    stroke(this.colour)
    ellipseMode(CENTER)
    rectMode(CENTER)
    rect(this.x, this.y, this.r, this.r);
    text(this.target_id, this.x + 5, this.y)
    noFill()
  }

  bloom() {
    stroke(this.colour)
    fill(this.colour_alpha)
    ellipse(this.x, this.y, this.r*10)
    noFill()
  }
}