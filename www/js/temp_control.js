function show_temp_control(device_name)
{
	addCloseButton();
	showing_temp = true;
	mo = document.getElementById('main_output');
	
	div_title = document.createElement('div');
	div_title.innerHTML = 'Temperature Controller: ' + device_name;
	mo.appendChild(div_title);
	
	div_body = document.createElement('div');
	div_body.innerHTML = '';
	
	div_target = document.createElement('div');
	
		div_target_label = document.createElement('div');
		div_target_label.innerHTML = 'Target Temperature';
		div_target_label.classList.add('ctl_left');
	
		div_target_input = document.createElement('div');
		div_target_input.classList.add('ctl_right');
		
			text_target_value = document.createElement('input');
			text_target_value.type = 'text';
			text_target_value.placeholder = 'Enter in C';
			text_target_value.id='target_temp_value';
	
		div_target_input.appendChild(text_target_value);
		
	div_target.appendChild(div_target_label);
	div_target.appendChild(div_target_input);
	div_target.classList.add('float_clear');
	
	div_body.appendChild(div_target);
	
	div_current = document.createElement('div');
	div_current.classList.add('float_clear');
	
		div_current_label = document.createElement('div');
		div_current_label.innerHTML = 'Current Temperature';
		div_current_label.classList.add('ctl_left');
		
		div_current_input = document.createElement('div');
		div_current_input.classList.add('ctl_right');
		
			text_current_value = document.createElement('input');
			text_current_value.type = 'text';
			text_current_value.value = '';
			text_current_value.id='current_temp_value';
			
		div_current_input.append(text_current_value);
		
	div_current.appendChild(div_current_label);
	div_current.appendChild(div_current_input);
	
	div_body.appendChild(div_current);
	
	div_controls = document.createElement('div');
	div_controls.classList.add('float_clear');
	
	div_button_start = document.createElement('id');

	
		button_start = document.createElement('input');
		button_start.type = 'button';
		button_start.value = 'Start';
	

	div_button_start.appendChild(button_start);
	div_button_start.classList.add('ctl_left');
	
	
	div_button_stop = document.createElement('div');
		
		button_stop = document.createElement('input');
		button_stop.type = 'button';
		button_stop.value = 'Stop';
		
	div_button_stop.appendChild(button_stop);	
	div_button_stop.classList.add('ctl_right');
		
	div_controls.appendChild(div_button_start);
	div_controls.appendChild(div_button_stop);
	
	div_body.appendChild(div_controls);
	
	mo.appendChild(div_body);
	
	 (function(device_name){
			button_start.addEventListener("click", function() {
				start_temp(device_name,document.getElementById('target_temp_value').value);
			});
		})(device_name);
		
	
	 (function(device_name){
			button_stop.addEventListener("click", function() {
				stop_temp(device_name);
			});
		})(device_name);
	console.log(device_name);
	
	get_stat(device_name);
}

function start_temp(device_name, target_temp) {
	
	console.log("Starting " + device_name + " at " + target_temp);
	
	var req = new XMLHttpRequest();
	req.open("POST", "cnco2_controller.php", true);

	req.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	req.onload = function() {
		response = req.responseText;
		console.log(response);
		sens = JSON.parse(response);
		

	}
	target_temp = document.getElementById('target_temp_value').value;
	
	var parms = "action=component_temp_set&controller_id="+encodeURIComponent(device_name)+"&target_temp="+target_temp;
	req.send(parms);
	
}

function stop_temp(device_name) {
	console.log("Stopping " + device_name);
	var req = new XMLHttpRequest();
	req.open("POST", "cnco2_controller.php", true);

	req.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	req.onload = function() {
		response = req.responseText;
		console.log(response);
		sens = JSON.parse(response);
		

	}
	target_temp = document.getElementById('target_temp_value').value;
	
	var parms = "action=component_temp_stop&controller_id="+encodeURIComponent(device_name);
	req.send(parms);
}

function get_stat(device_name) {
	
	if(showing_temp) {	
		console.log("getting temp stat for "+device_name);	
		
		var req = new XMLHttpRequest();
		req.open("POST", "cnco2_controller.php", true);

		req.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
		req.onload = function() {
			response = req.responseText;
			sens = JSON.parse(response);
			document.getElementById('current_temp_value').value = sens.current_temp;
		}
		var parms = "action=component_temp_stat&controller_id="+encodeURIComponent(device_name);
		req.send(parms);
	
		console.log("timout for stat");
		setTimeout(function() {
			get_stat(device_name);
		}, 10000);

	}
}
