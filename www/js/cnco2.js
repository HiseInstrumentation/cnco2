function getComponents()
{
    console.log("Getting components");
	var req = new XMLHttpRequest();
	req.open("POST", "cnco2_controller.php", true);

	req.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	req.onload = function() {
		document.getElementById('components').innerHTML = req.responseText;
	}
	var parms = "action=component_get_all";
	req.send(parms);

    setTimeout(getComponents, 1000);

}

function componentDiscover()
{
	var req = new XMLHttpRequest();
	req.open("POST", "cnco2_controller.php", true);

	req.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
	req.onload = function() {
		document.getElementById('work_area').innerHTML = req.responseText;
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
