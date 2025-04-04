function npad_push(u_value)
{
		ctl = document.getElementById('ctarget_temp_value');
		if(u_value == '<') {
			ctl.value = "";
		} else {
			ctl.value = ctl.value + u_value ;
		}
}

function show_temp_control(device_name)
{
	initializeWorkspace();
	showing_temp = true;
	mo = document.getElementById('main_output');

	div_title = document.createElement('div');
	div_title.innerHTML = 'Temperature Controller: ' + device_name;
	mo.appendChild(div_title);
	
	div_body = document.createElement('div');
	div_body.innerHTML = '';
	
	// Target
	div_target = document.createElement('div');
	
		div_target_label = document.createElement('div');
		div_target_label.innerHTML = 'Target Temperature';
		div_target_label.classList.add('ctl_left');
	
		div_target_input = document.createElement('div');
		div_target_input.classList.add('ctl_right');
		div_target_input.id='target_temp_value';
		
		div_target_input.classList.add('sensor_output');
		div_target_input.innerHTML = '&nbsp;';
				
	div_target.appendChild(div_target_label);
	div_target.appendChild(div_target_input);
	div_target.classList.add('float_clear');
	
	div_body.appendChild(div_target);
	
	
	
	// CURRENT
	div_current = document.createElement('div');
	div_current.classList.add('float_clear');
	
		div_current_label = document.createElement('div');
		div_current_label.innerHTML = 'Current Temperature';
		div_current_label.classList.add('ctl_left');
		
		div_current_input = document.createElement('div');
		div_current_input.classList.add('ctl_right');
		div_current_input.id='current_temp_value';
		
		div_current_input.classList.add('sensor_output');
		div_current_input.innerHTML = '&nbsp;';
		
					
		
	div_current.appendChild(div_current_label);
	div_current.appendChild(div_current_input);
	
	div_body.appendChild(div_current);
	
	// STATUS
	div_status = document.createElement('div');
	div_status.classList.add('float_clear');
	
		div_status_label = document.createElement('div');
		div_status_label.innerHTML = 'Current Status';
		div_status_label.classList.add('ctl_left');
		
		div_status_input = document.createElement('div');
		div_status_input.classList.add('ctl_right');
		div_status_input.id='current_status_value';
		
		div_status_input.classList.add('sensor_output');
		div_status_input.innerHTML = '&nbsp;';
		
	div_status.appendChild(div_status_label);
	div_status.appendChild(div_status_input);
	
	div_body.appendChild(div_status);
		
	// Power level
	div_power = document.createElement('div');
	div_power.classList.add('float_clear');
	
		div_power_label = document.createElement('div');
		div_power_label.innerHTML = 'Current Power Level';
		div_power_label.classList.add('ctl_left');
		
		div_power_input = document.createElement('div');
		div_power_input.classList.add('ctl_right');
		div_power_input.id='current_power_value';
		
		div_power_input.classList.add('sensor_output');
		div_power_input.innerHTML = '&nbsp;';
		
	div_power.appendChild(div_power_label);
	div_power.appendChild(div_power_input);
	
	div_body.appendChild(div_power);
	
	div_controls = document.createElement('div');
	div_controls.classList.add('float_clear');
	
// Target Change
	
	div_ctarget = document.createElement('div');
	
		div_ctarget_label = document.createElement('div');
		div_ctarget_label.innerHTML = 'Change Target Temperature';
		div_ctarget_label.classList.add('ctl_left');
	
		div_ctarget_input = document.createElement('div');
		div_ctarget_input.classList.add('ctl_right');
		
			text_ctarget_value = document.createElement('input');
			text_ctarget_value.type = 'text';
			text_ctarget_value.placeholder = 'Enter in C';
			text_ctarget_value.id='ctarget_temp_value';
				
			npad = document.createElement('div');
			
			npad.classList.add('npad');
			buttons = ["1","2","3","4","5","6","7","8","9","0",".","<"];
			
			for(i = 0; i < buttons.length; i++) {
				d_name = buttons[i];
				npad_butt = document.createElement('div');	
				npad_butt.innerHTML = buttons[i];
				
				 (function(d_name){
					npad_butt.addEventListener("click", function() {
					npad_push(d_name);
					});
				})(d_name);
				
				npad.appendChild(npad_butt);
			
			}

	
		div_ctarget_input.appendChild(text_ctarget_value);
		div_ctarget_input.appendChild(npad);
		
	div_ctarget.appendChild(div_ctarget_label);
	div_ctarget.appendChild(div_ctarget_input);
	div_ctarget.classList.add('float_clear');
	
	div_body.appendChild(div_ctarget);	
	
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
				start_temp(device_name,document.getElementById('ctarget_temp_value').value);
			});
		})(device_name);
		
	
	 (function(device_name){
			button_stop.addEventListener("click", function() {
				stop_temp(device_name);
			});
		})(device_name);
	
	get_stat(device_name);
}

function start_temp(device_name, target_temp) {
	
	console.log("Starting " + device_name + " at " + target_temp);
	
	var req = new XMLHttpRequest();
	req.open("POST", "cnco2_controller.php", true);

	req.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	req.onload = function() {
		response = req.responseText;
		sens = JSON.parse(response);
		

	}
	
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
		sens = JSON.parse(response);
		

	}
	target_temp = document.getElementById('target_temp_value').value;
	
	var parms = "action=component_temp_stop&controller_id="+encodeURIComponent(device_name);
	req.send(parms);
}

function get_stat(device_name) {
	
	if(showing_temp && system_running) {	
		
		var req = new XMLHttpRequest();
		req.open("POST", "cnco2_controller.php", true);

		req.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
		req.onload = function() {
			response = req.responseText;
			status = 'Off';
			sens = JSON.parse(response);
			
			if(sens.current_status == 'H') {
				status = 'On: Heating';
			} else if (sens.current_status == 'C') {
				status = 'On: Cooling';
			}
			
			power_pct = (sens.peltier_power_level / 255 * 100);
			if(status == 'Off') {
				power_pct = 0;
			}
			
			document.getElementById('current_temp_value').innerHTML = sens.current_temp + ' C';
			document.getElementById('current_power_value').innerHTML = Number((power_pct).toFixed(1)) + '%';
			document.getElementById('target_temp_value').innerHTML = sens.target_temp + ' C';
			
			document.getElementById('current_status_value').innerHTML = status;
		}
		var parms = "action=component_temp_stat&controller_id="+encodeURIComponent(device_name);
		req.send(parms);
	
		setTimeout(function() {
			get_stat(device_name);
		}, 5000);

	}
}
