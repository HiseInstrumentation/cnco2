function show_o2_control()
{
	device_name = 'o2_sensor';
	mo = document.getElementById('main_output');
	
	div_title = document.createElement('div');
	div_title.innerHTML = 'O2 Sensor';
	mo.appendChild(div_title);
	
	div_body = document.createElement('div');
	div_body.innerHTML = '';
	
	button_sensor_read = document.createElement('input');
	button_sensor_read.type = 'button';
	button_sensor_read.value = 'Get Sensor Reading';
	
	div_body.appendChild(button_sensor_read);
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
		document.getElementById('sensor_reading').innerHTML = "<br />Last Reading:<br /><b>O2: </b>" + sens.current_o2 + "<br /><b>Temp: </b>" + sens.current_temp + "<br /><b>Pressure: </b>" + sens.current_pressure;
	}
	var parms = "action=component_o2_read";
	req.send(parms);
}
