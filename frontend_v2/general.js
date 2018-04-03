function remove_from_array(array, item){
  let index;

  index = array.indexOf(item)
  array.splice(index, 1)
}

function hexToRgb(hex) {
  var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result ? {
      r: parseInt(result[1], 16),
      g: parseInt(result[2], 16),
      b: parseInt(result[3], 16)
  } : null;
}

function objectSetup() {
  objects = []

  objects[0] = new Grid(scale_unit, scale_unit)

  agents = new Array()
  targets = new Array()

  for(let i = 0; i < 5; i++)
    agents[i] = new Agent(i, int(-(i+1)*10*scale_unit), int(-(i+1)*10*scale_unit))
  
  objects = objects.concat(agents)

  for(let i = 0; i < 5; i++){
    agent_targets = new Array()
    for(let j = 0; j < 5; j++)
      agent_targets[j] = new Target(i, j+1, int(-(i+1)*100*scale_unit), int(-(i+1)*100*scale_unit))
    targets = targets.concat([agent_targets])
    objects = objects.concat(agent_targets)
  }
}

function setup_positions(){
  objects = []

  objects[0] = new Grid(scale_unit, scale_unit)

  agents = new Array()
  targets = new Array()

  Agent_Buttons = DOM_objects.Agent_Buttons

  for(let i = 0; i < 5; i++){
    agents[i] = new Agent(i, int(starting_positions[i].X * scale_unit), int(starting_positions[i].Y * scale_unit))
    Agent_Buttons[i].mousePressed(agents[i].display_info.bind(agents[i]))
  }
  
  objects = objects.concat(agents)

  for(let i = 0; i < 5; i++){
    agent_targets = new Array()
    for(let j = 0; j < 5; j++)
      agent_targets[j] = new Target(i, j+1, int(starting_positions[i].Targets[j].X * scale_unit), int(starting_positions[i].Targets[j].Y * scale_unit))
    targets = targets.concat([agent_targets])
    objects = objects.concat(agent_targets)
  }

  starting_positions = []
  current_agent_info = agents[0]
}

function DOMSetup() {
  DOM_objects = {}

  // Reset Button
  let Reset_Button = createSpan("Reset")
  Reset_Button.parent('#reset').addClass("button is-danger is-medium").mousePressed(objectSetup)

  // // Reset Button
  // let Reset_Button = createA("/", "Reset")
  // Reset_Button.parent('#reset').addClass("button is-danger is-medium")

  // Pause Button
  let Pause_Button = createSpan("Pause")
  Pause_Button.parent('#pause').addClass("button is-info is-medium").mousePressed(toggle_pause)

  // // Test Button
  // let Test_Button = createSpan("Test")
  // Test_Button.parent('#server_test').addClass("button is-info is-medium").mousePressed(server_test)

  // Trail Button
  let Trail_Button = createSpan("Trail On")
  Trail_Button.parent('#trail').addClass("button is-link is-medium").mousePressed(toggle_trail)

  // Details Button
  let Detail_Button = createSpan("Details")
  Detail_Button.parent('#details').addClass("button is-primary is-medium").mousePressed(toggle_verbose)

  // Agent Info
  let Agent_Title = createP("Agent #1")
  Agent_Title.parent('#agent-info').addClass("is-size-5")

  let Agent_X_Position = createP("x: ")
  Agent_X_Position.parent('#agent-info').addClass("is-size-6")

  let Agent_Y_Position = createP("y: ")
  Agent_Y_Position.parent('#agent-info').addClass("is-size-6")

  let Agent_Targets_Found = createP("Targets Found: ")
  Agent_Targets_Found.parent('#agent-info').addClass("is-size-6")

  // Agent info buttons
  Agent_Buttons = []

  for(let i = 0; i < 5; i++){
    Agent_Buttons[i] = createSpan(`Agent #${i + 1}`)
    Agent_Buttons[i].parent(`#Agent${i + 1}`).addClass("button is-medium").style('background-color', agents[i].colour).style('color', '#fff').mousePressed(agents[i].display_info.bind(agents[i]))
  }

  // Iteration Number
  let Iterations_Span = createSpan("Iteration: " + iteration)
  Iterations_Span.parent('#iteration').addClass('is-size-4')

  // Iteration Slider
  let Iterations_Slider = createSlider(0, 100, 0, 1)
  Iterations_Slider.parent('#iteration-slider').id('slider')

  // Iteration Input
  let Iterations_Input = createInput('')
  Iterations_Input.parent('#iteration-input').addClass('input').value(0)
  // Reset Button
  let Iterations_Submit = createSpan("Submit")
  Iterations_Submit.parent('#iteration-submit').addClass("button is-danger is-medium").mousePressed(set_iteration)

  DOM_objects = Object.assign({
    "Reset" : Reset_Button,
    "Pause": Pause_Button,
    "Detail": Detail_Button, 
    "Trail": Trail_Button,
    "Agent": {
      "Title": Agent_Title,
      "X": Agent_X_Position,
      "Y": Agent_Y_Position,
      "Targets_Found": Agent_Targets_Found
    },
    "Agent_Buttons": Agent_Buttons,
    "Iterations": Iterations_Span,
    "Slider": Iterations_Slider,
    "Iterations_Input": Iterations_Input,
    "Iterations_Button": Iterations_Submit
  });

  current_agent_info = agents[0]
}

function toggle_verbose() {
  verbose = verbose ? false : true
}

function toggle_pause() {
  pause = pause ? false : true
  DOM_objects.Pause.html(`${pause ? "Resume" : "Pause"}`)
  if(pause)
    noLoop()
  else
    loop()
}

function toggle_trail() {
  trail = trail ? false : true
  DOM_objects.Trail.html(`Trail ${!trail ? "On" : "Off"}`)
}

function set_iteration(){
  value = int(DOM_objects.Iterations_Input.value())

  DOM_objects.Iterations.html("Iteration: " + value)
  DOM_objects.Slider.value(value)

  iteration = value
}