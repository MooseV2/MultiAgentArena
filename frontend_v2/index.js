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
let iteration = 1
let pickup = false;

// Make sure Agents are 1 unit, Radius is 10 units, and Width/Height is 100 units
const scale_unit = 6

// Frame Rate
const frame_rate = 5

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
    pickup = true
  }

  background(255);

  stroke("#333")
  strokeWeight(2)
  rect(scale_unit*50, scale_unit*50, agent_reach, agent_reach)
  strokeWeight(1)
  noStroke()

  // if(pause){
  //   console.log(4)
  //   iteration = DOM_objects.Slider.value()
  //   DOM_objects.Iterations.html("Iteration: " + iteration)
  // } else {
    DOM_objects.Iterations.html("Iteration: " + iteration)
  //   DOM_objects.Slider.value(iteration)  
  // }

  for (let instance of objects) {
    if (instance)
      instance.draw()
  }

  if(iterations != 0 && !pause)
    iteration++
  
  if(iteration >= iterations.length)
    iteration = 1

  current_agent_info.display_info()

  if(pickup){
    agents.map((agent) => {
      agent.check_target(targets[agent.id])
    })
  }
}