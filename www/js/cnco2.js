showing_temp = false;
showing_o2 = false;
showing_gantry = false;
system_running = false;
ui_blocked = false;


function blockUI()
{
	if(ui_blocked == false) {
		console.log("Blocking");
		sr = document.getElementById('modal_content');
		sr.innerHTML = '[ Please wait for task to finish. ]';
		ui_blocked = true;

		m = document.getElementById('myModal');
		m.style.display = "block";
	}
}

function freeUI()
{
	if(ui_blocked == true) {
		console.log("Freed");
		ui_blocked = false;

		m = document.getElementById('myModal');
		m.style.display = "none";
	}
}


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
		unfinished_found = false;

		output = JSON.parse(req.responseText);
		log_table = document.getElementById('log_table');
		log_table.innerHTML = '<tr><th>Started</th><th>Finished</th><th>Command</th><th>Parameters</th><th>System Reponse</th></tr>';
		for(i = 0; i < output.length; i++) {
			log_row = document.createElement('tr');
			log_row_created = document.createElement('td');
			log_row_created.innerHTML = output[i].created;

			log_row_executed = document.createElement('td');
			log_row_executed.innerHTML = output[i].executed;

			log_row_command = document.createElement('td');
			log_row_command.innerHTML = output[i].command_text;

			log_row_parms = document.createElement('td');
			log_row_parms.innerHTML = output[i].parameters;

			log_row_response = document.createElement('td');
			log_row_response.innerHTML = output[i].system_response;


			log_row.appendChild(log_row_created);
			log_row.appendChild(log_row_executed);
			log_row.appendChild(log_row_command);
			log_row.appendChild(log_row_parms);
			log_row.appendChild(log_row_response);

			log_table.appendChild(log_row);
			if((output[i].executed == "") && (output[i].ui_block == 1)) {
				unfinished_found = true;
			}
		}

		if(unfinished_found) {
			blockUI();
		} else {
			freeUI();
		}
	}
	var parms = "action=command_status";
	req.send(parms);
}

function initializeWorkspace()
{
	addCloseButton();
	mo = document.getElementById('main_output');
	mo.innerHTML = '';
}

function addCloseButton()
{
	wscd = document.getElementById('ws_close');
	wscd.innerHTML = '';
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
	getSystemStatus();
	setTimeout(updateStatus, 1000);
}

function getSystemStatus() 
{
	var req = new XMLHttpRequest();
	req.open("POST", "cnco2_controller.php", true);

	req.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	req.onload = function() {
		response = JSON.parse(req.responseText);
		div_status = document.getElementById('system_status');
		if(response.running == false) {
			div_status.innerHTML = '[ <b>SYSTEM NOT RUNNING</b> ]';
			system_running = false;
		} else {
			div_status.innerHTML = '[ System Running ]';
			system_running = true;
		}
		
	}
	var parms = "action=system_check";
	req.send(parms);
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
