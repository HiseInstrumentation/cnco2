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
