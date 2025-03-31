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
	button_home.value = 'Send Home Commnad';
	
	 (function(d_name){
		button_home.addEventListener("click", function() {
			gantry_home();
			});
		})(d_name);
	
	div_home_button_button.appendChild(button_home);

	div_home_button.appendChild(div_home_button_label);
	div_home_button.appendChild(div_home_button_button);
	
	div_body.appendChild(div_home_button);
	
	mo.appendChild(div_body);
}

function gantry_home()
{	
	console.log("Homing Gantry");
	
	var req = new XMLHttpRequest();
	req.open("POST", "cnco2_controller.php", true);

	req.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	req.onload = function() {
		response = req.responseText;
		console.log(response);
		sens = JSON.parse(response);
		console.log(sens);
	}
	
	var parms = "action=component_gantry_home";
	req.send(parms);
	

}

