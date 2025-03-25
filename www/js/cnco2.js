showing_temp = false;
showing_o2 = false;
showing_gantry = false;

function getComponents()
{
	var req = new XMLHttpRequest();
	req.open("POST", "cnco2_controller.php", true);

	req.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	req.onload = function() {
		document.getElementById('component_details').innerHTML = req.responseText;
	}
	var parms = "action=component_get_all";
	req.send(parms);

}

function getCommandStatus()
{
	var req = new XMLHttpRequest();
	req.open("POST", "cnco2_controller.php", true);

	req.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	req.onload = function() {
		output = JSON.parse(req.responseText);
		log_table = document.getElementById('log_table');
		log_table.innerHTML = '<tr><th>Started</th><th>Finished</th><th>Command</th><th>System Reponse</th></tr>';
		for(i = 0; i < output.length; i++) {
				log_row = document.createElement('tr');
				log_row_created = document.createElement('td');
				log_row_created.innerHTML = output[i].created;
				
				log_row_executed = document.createElement('td');
				log_row_executed.innerHTML = output[i].executed;
				
				log_row_command = document.createElement('td');
				log_row_command.innerHTML = output[i].command_text;
				
				log_row_response = document.createElement('td');
				log_row_response.innerHTML = output[i].system_response;
				
				
				log_row.appendChild(log_row_created);
				log_row.appendChild(log_row_executed);
				log_row.appendChild(log_row_command);
				log_row.appendChild(log_row_response);
				
				log_table.appendChild(log_row);
		}
		// document.getElementById('system_log_output').innerHTML = output;
	}
	var parms = "action=command_status";
	req.send(parms);
}

function addCloseButton()
{
	wscd = document.getElementById('ws_close');
	fname = 'func_close';
	
	cb = document.createElement('a');
	cb.innerHTML = 'X';
	
	 (function(fname){
		cb.addEventListener("click", function() {
			closeWorkspace();
		});
	})(fname);
	
	wscd.appendChild(cb);
}

function closeWorkspace()
{
	mo = document.getElementById('main_output');
	mo.innerHTML = '';
	
	wscd = document.getElementById('ws_close');
	wscd.innerHTML = '';
	
	showing_temp = false;
	showing_o2 = false;
	showing_gantry = false;

}

function updateStatus()
{
	getComponents();
	getCommandStatus();
	setTimeout(updateStatus, 1000);
}

function componentDiscover()
{
	var req = new XMLHttpRequest();
	req.open("POST", "cnco2_controller.php", true);

	req.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	req.onload = function() {
		document.getElementById('main_output').innerHTML = req.responseText;
	}
	var parms = "action=component_discover";
	req.send(parms);
}

function downloadBatchData(batch_access_key) 
{
	var req = new XMLHttpRequest();
	req.open("POST", "cnco2_controller.php", true);

	req.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	req.onload = function() {
		document.getElementById('work_area').innerHTML = req.responseText;
	}
	var parms = "action=view_data&batch_access_key="+batch_access_key;
	req.send(parms);
	
}
