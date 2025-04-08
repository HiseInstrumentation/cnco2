gantry_homed = false;
controls_shown = false;
device_name = 'gantry'
x_changed = false;
y_changed = false;

function get_current_status()
{
	if(showing_gantry) {			
		var req = new XMLHttpRequest();
		req.open("POST", "cnco2_controller.php", true);

		req.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
		req.onload = function() {
			response = req.responseText;
			stat = JSON.parse(response);
			gantry_homed = stat.was_homed;
			if((gantry_homed == true) && (controls_shown == false)) {
				show_move_controls();
			}
			if(controls_shown) {
				if(!x_changed) {
					document.getElementById('x_pos_offset').value = stat.current_x;
				}
				if(!y_changed) {
					document.getElementById('y_pos_offset').value = stat.current_y;
				}
			}
		}
		
		var parms = "action=component_gantry_status";
		req.send(parms);
		
		setTimeout(function() {
			get_current_status();
		}, 5000);
	}
}

function show_move_controls()
{
	controls_shown = true;
	show_gantry_control(device_name);
}

function show_gantry_control(device_name)
{
	initializeWorkspace();
	showing_gantry = true;
	d_name = 'gantry';
	
	mo = document.getElementById('main_output');
	div_body = document.createElement('div');
	div_body.innerHTML = '';
	
	div_title = document.createElement('div');
	div_title.innerHTML = 'Gantry Controller ';
	mo.appendChild(div_title);
	
	div_home_button = document.createElement('div');
	
	div_home_button_label = document.createElement('div');
	div_home_button_label.innerHTML = 'Home Gantry';
	div_home_button_label.classList.add('ctl_left');

	div_home_button_button = document.createElement('div');
	div_home_button_button.classList.add('ctl_right');

	button_home = document.createElement('input');
	button_home.type = 'button';
	button_home.value = 'Home Gantry';
	
	 (function(d_name){
		button_home.addEventListener("click", function() {
			gantry_home();
			});
		})(d_name);
	
	div_home_button_button.appendChild(button_home);

	div_home_button.appendChild(div_home_button_label);
	div_home_button.appendChild(div_home_button_button);
	
	div_body.appendChild(div_home_button);
	
	if(controls_shown) {
	
		div_controls = document.createElement('div');
		
		div_x_row = document.createElement('div');
		
		div_x_label = document.createElement('div');
			div_x_label.innerHTML = 'X Postion';
			div_x_label.classList.add('ctl_left');

			
		div_x_input = document.createElement('div');
		div_x_input.classList.add('ctl_right');

			input_x = document.createElement('input');
			input_x.type = 'text';
			input_x.placeholder = 'Enter X Position';
			input_x.id = 'x_pos_offset';
			
		(function(device_name){
			input_x.addEventListener("focus", function() {
				x_changed = true;
				console.log("CHANGED");
			});
		})(device_name);
		
		
		div_x_row.classList.add('float_clear');

		
		div_y_row = document.createElement('div');
		
		div_y_label = document.createElement('div');
			div_y_label.innerHTML = 'Y Postion';
			div_y_label.classList.add('ctl_left');

			
		div_y_input = document.createElement('div');
		div_y_input.classList.add('ctl_right');

			input_y = document.createElement('input');
			input_y.type = 'text';
			input_y.placeholder = 'Enter Y Position';
			input_y.id = 'y_pos_offset';
		
		(function(device_name){
			input_y.addEventListener("focus", function() {
				y_changed = true;
			});
		})(device_name);
			
		div_y_row.classList.add('float_clear');

		
		div_repos_row = document.createElement('div');

			div_repos_label = document.createElement('div');
			div_repos_label.classList.add('ctl_left');
			div_repos_label.innerHMTL = '&nbsp';

			div_repos_butt = document.createElement('div');
			div_repos_butt.classList.add('ctl_right');
		
			button_repos = document.createElement('input');
				button_repos.type = 'button';
				button_repos.value = 'Move';
				
		div_repos_row.classList.add('float_clear');

			
		(function(device_name){
			button_repos.addEventListener("click", function() {
				gantry_move();
			});
		})(device_name);
		
		div_x_input.appendChild(input_x);
		div_y_input.appendChild(input_y);
		div_x_row.appendChild(div_x_label);
		div_x_row.appendChild(div_x_input);
		
		div_repos_butt.appendChild(button_repos);
		
		div_y_row.appendChild(div_y_label);
		div_y_row.appendChild(div_y_input);
		
		div_repos_row.appendChild(div_repos_label);
		div_repos_row.appendChild(div_repos_butt);
		
		div_controls.appendChild(div_x_row);
		div_controls.appendChild(div_y_row);
		div_controls.appendChild(div_repos_row);
		
		div_body.appendChild(div_controls);
	}
	
	mo.appendChild(div_body);
	
	get_current_status();
	
	

}

function gantry_move()
{
	x = Number(document.getElementById('x_pos_offset').value);
	y = Number(document.getElementById('y_pos_offset').value);

	if((x >= 0 && x <=200) && (y >= 0 && y <= 200)) {
		
		console.log("Moving Gantry to: x="+x+" y="+y);
		var req = new XMLHttpRequest();
		req.open("POST", "cnco2_controller.php", true);

		req.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
		req.onload = function() {
			response = req.responseText;
			sens = JSON.parse(response);
			x_changed = false;
			y_changed = false;
		}
		
		var parms = "action=component_gantry_move&x="+x+"&y="+y;
		req.send(parms);
		
	} else {
		console.log("Out of Range x="+x+" y="+y);
	}
}


function gantry_home()
{	
	console.log("Homing Gantry");
	
	var req = new XMLHttpRequest();
	req.open("POST", "cnco2_controller.php", true);

	req.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	req.onload = function() {
		response = req.responseText;
		sens = JSON.parse(response);
	}
	
	var parms = "action=component_gantry_home";
	req.send(parms);
	
}

