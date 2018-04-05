let objects
let DOM_objects
let Agent_Buttons
let agents
let current_agent_info
let targets
const colours = ["#c56cf0", "#ff3838", "#ff9f1a", "#17c0eb", "#1dd1a1"]
let verbose = true
let pause = false
let trail = false
let iteration = 0
let pickup = false
let competition = false

// Make sure Agents are 1 unit, Radius is 10 units, and Width/Height is 100 units
const scale_unit = 6

// Frame Rate
const frame_rate = 30

// Agent vision properties
const agent_reach = 515

let starting_positions = []
let starting_positions_history = []
let iterations = []

function setup() {
  // document.querySelector('#conn-status').innerHTML = 'Disconnected';
  canvas = createCanvas(scale_unit*100, scale_unit*100)
  canvas.parent("sketch_wrapper")

  // Create all objects
  objectSetup()

  // Set DOM elements
  DOMSetup()

  frameRate(frame_rate)

}

function draw() {

  if(starting_positions != 0) {
    pickup = false
    setup_positions()
    iteration = 1
    if(pause)
    toggle_pause()
    pickup = true
  }

  background(255);

  stroke("#333")
  strokeWeight(2)
  rect(scale_unit*50, scale_unit*50, agent_reach, agent_reach)
  strokeWeight(1)
  noStroke()

  DOM_objects.Iterations.html("Iteration: " + iteration)

  for (let instance of objects) {
    if (instance)
      instance.draw()
  }
  
  if(iteration == 0){
    indicator_background(color(255, 159, 26, 75))
  }else if(iteration >= iterations.length - 1){
    if(!pause)
      toggle_pause()
    indicator_background(color(29, 209, 161, 75))
    iteration = iterations.length - 1
  } else if(iterations != 0 && !pause){
    iteration++
  }

  current_agent_info.display_info()

  if(pickup){
    agents.map((agent) => {
      agent.check_target(targets[agent.id])
    })
  }
}