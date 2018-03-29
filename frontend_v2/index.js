let objects
let DOM_objects
let Agent_Buttons
let agents
let current_agent_info
let targets
let colours = ["#c56cf0", "#ff3838", "#ff9f1a", "#17c0eb", "#1dd1a1"]
let verbose = true

// Make sure Agents are 1 unit, Radius is 10 units, and Width/Height is 100 units
let scale_unit = 6

// Frame Rate
let frame_rate = 30

function objectSetup() {
  objects = []

  objects[0] = new Grid(scale_unit, scale_unit)

  agents = new Array()
  targets = new Array()

  for(let i = 0; i < 5; i++)
    agents[i] = new Agent(i, int(random(scale_unit*100)), int(random(scale_unit*100)))
  
  objects = objects.concat(agents)

  for(let i = 0; i < 5; i++){
    agent_targets = new Array()
    for(let j = 0; j < 5; j++)
      agent_targets[j] = new Target(i, j, int(random(scale_unit*100)), int(random(scale_unit*100)))
    targets = targets.concat([agent_targets])
    objects = objects.concat(agent_targets)
  }
}

function DOMSetup() {
  DOM_objects = {}

  // Reset Button
  let Reset_Button = createA("/Arena.html", "Reset")
  Reset_Button.parent('#reset').addClass("button is-danger is-medium")

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
    Agent_Buttons[i].parent(`#Agent${i + 1}`).addClass("button is-medium").style('background-color', agents[i].colour).mousePressed(agents[i].display_info.bind(agents[i]))
  }

  current_agent_info = agents[0]
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

  frameRate(frame_rate)
  // noLoop()
}

function draw() {
  background(255);
  stroke("#333")
  rect(42,42,558,558)
  noStroke()
  for (let instance of objects) {
    if (instance)
      instance.draw()
  }

  current_agent_info.display_info()

  agents.map((agent) => {
    agent.check_target(targets[agent.id])
  })
}