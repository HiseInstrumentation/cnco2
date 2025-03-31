function show_o2_control()
{
	initializeWorkspace();
	mo = document.getElementById('main_output');

	device_name = 'o2_sensor';

	div_title = document.createElement('div');
	div_title.innerHTML = 'O2 Sensor';
	mo.appendChild(div_title);
	
	div_body = document.createElement('div');
	div_body.innerHTML = '';
	
	div_button = document.createElement('div');
	
	div_button_label = document.createElement('div');
	div_button_label.innerHTML = 'Get Sensor Reading';
	div_button_label.classList.add('ctl_left');

	div_button_button = document.createElement('div');
	div_button_button.classList.add('ctl_right');

	button_sensor_read = document.createElement('input');
	button_sensor_read.type = 'button';
	button_sensor_read.value = 'Get Sensor Reading';
	
	div_button_button.appendChild(button_sensor_read);

	div_button.appendChild(div_button_label);
	div_button.appendChild(div_button_button);
	
	div_body.appendChild(div_button);
		
	div_o2 = document.createElement('div');
		div_o2_label = document.createElement('div');
		div_o2_label.innerHTML = 'Oxygen';
		div_o2_label.classList.add('ctl_left');

		div_o2_value = document.createElement('div');
		div_o2_value.innerHTML = '';
		div_o2_value.classList.add('ctl_right');
		div_o2_value.classList.add('sensor_output');
		div_o2_value.innerHTML = '&nbsp;';
		div_o2_value.id = 'o2_reading';

		
	div_o2.appendChild(div_o2_label);
	div_o2.appendChild(div_o2_value);

	div_temp = document.createElement('div');
		div_temp_label = document.createElement('div');
		div_temp_label.innerHTML = 'Temperature';
		div_temp_label.classList.add('ctl_left');

		div_temp_value = document.createElement('div');
		div_temp_value.innerHTML = '';
		div_temp_value.classList.add('ctl_right');
		div_temp_value.id = 'temp_reading';
		div_temp_value.classList.add('sensor_output');
		div_temp_value.innerHTML = '&nbsp;';
		
	div_temp.appendChild(div_temp_label);
	div_temp.appendChild(div_temp_value);

	div_press = document.createElement('div');
		div_press_label = document.createElement('div');
		div_press_label.innerHTML = 'Pressure';
		div_press_label.classList.add('ctl_left');

		div_press_value = document.createElement('div');
		div_press_value.innerHTML = '';
		div_press_value.classList.add('ctl_right');
		div_press_value.id = 'press_reading';
		div_press_value.classList.add('sensor_output');
		div_press_value.innerHTML = '&nbsp;';
		
	div_press.appendChild(div_press_label);
	div_press.appendChild(div_press_value);
	
	div_o2.classList.add('float_clear');
	div_temp.classList.add('float_clear');
	div_press.classList.add('float_clear');
	div_body.classList.add('float_clear');

	mo.appendChild(div_o2);
	mo.appendChild(div_temp);
	mo.appendChild(div_press);
	mo.appendChild(div_body);
	
	
	sensor_reading = document.createElement('div');
	sensor_reading.id="sensor_reading";
	mo.appendChild(sensor_reading);

	 (function(device_name){
			button_sensor_read.addEventListener("click", function() {
				get_o2_reading();
			});
		})(device_name);
	
}

function get_o2_reading() {
	console.log("getting reading");
	var req = new XMLHttpRequest();
	req.open("POST", "cnco2_controller.php", true);

	req.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	req.onload = function() {
		response = req.responseText;
		console.log(response);
		sens = JSON.parse(response);
		document.getElementById('o2_reading').innerHTML = sens.current_o2 + ' %';
		document.getElementById('temp_reading').innerHTML = sens.current_temp + ' C';
		document.getElementById('press_reading').innerHTML = sens.current_pressure + ' mB';
	}
	var parms = "action=component_o2_read";
	req.send(parms);
}
