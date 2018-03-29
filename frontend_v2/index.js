let objects
let DOM_objects
let Agent_Buttons
let agents
let targets
let colours = ["#ff9ff3", "#feca57", "#ff6b6b", "#48dbfb", "#1dd1a1"]
let verbose = false

// Make sure Agents are 1 unit, Radius is 10 units, and Width/Height is 100 units
let scale_unit = 6;

function objectSetup() {
  objects = []

  agents = new Array(5)
  targets = new Array(5)

  for(let i = 0; i < 5; i++)
    agents[i] = new Agent(i, int(random(scale_unit*100)), int(random(scale_unit*100)))
  
  for(let i = 0; i < 5; i++){
    agent_targets = new Array(5)
    for(let j = 0; j < 5; j++)
      agent_targets[j] = new Target(i, int(random(scale_unit*100)), int(random(scale_unit*100)))
    
    targets = targets.concat(agent_targets)
  }

  objects[0] = new Grid(scale_unit, scale_unit)
  objects = objects.concat(agents, targets)
}

function DOMSetup() {
  DOM_objects = {}

  // Details Button
  let Detail_Button = createSpan("Details")
  Detail_Button.parent('#details').addClass("button is-danger is-medium").mousePressed(toggle_verbose)

  // Agent Info
  let Agent_Title = createP("Agent #1")
  Agent_Title.parent('#agent-info').addClass("is-size-5")

  let Agent_X_Position = createP("x: ")
  Agent_X_Position.parent('#agent-info').addClass("is-size-6")

  let Agent_Y_Position = createP("y: ")
  Agent_Y_Position.parent('#agent-info').addClass("is-size-6")

  let Agent_Targets_Found = createP("Targets Found: ")
  Agent_Targets_Found.parent('#agent-info').addClass("is-size-6")

  DOM_objects = Object.assign({
    "Detail": Detail_Button, 
    "Agent": {
      "Title": Agent_Title,
      "X": Agent_X_Position,
      "Y": Agent_Y_Position,
      "Targets_Found": Agent_Targets_Found
    }
  });

  // Agent info buttons
  Agent_Buttons = []

  for(let i = 0; i < 5; i++){
    Agent_Buttons[i] = createSpan(`Agent #${i + 1}`)
    Agent_Buttons[i].parent(`#Agent${i + 1}`).addClass("button is-info is-medium").mousePressed(agents[i].display_info.bind(agents[i]))
  }
}

function toggle_verbose() {
  verbose = verbose ? false : true
}

function setup() {
  // document.querySelector('#conn-status').innerHTML = 'Disconnected';
  let canvas = createCanvas(scale_unit*100, scale_unit*100)
  canvas.parent("sketch_wrapper")
  canvas.background("#333")

  // Create all objects
  objectSetup()

  // Set DOM elements
  DOMSetup()
}

function draw() {
  background(255);
  for (let instance of objects) {
    if (instance)
      instance.draw()
  }
}