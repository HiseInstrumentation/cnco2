<?php
	ini_set('display_errors', 'on');
	require_once("cnco2_lib.php");
?>
<!DOCTYPE HTML>
<html>
	<head>
		<title>CNCO2 - Griffin Lab</title>
		<link rel="stylesheet" href='default.css'>
		<script type='text/javascript' src = 'js/cnco2.js'></script>
	</head>

	<body>
		<div id='app_content'>
			<div class='title_bar'>
				<div class='ip_section'>IP Address: <?= getIpAddress(); ?></div>&nbsp;
				<div class='menu_bar'><a href = 'help.php' target = '_INSTRUCTIONS'>Instructions</a></div>
			</div>
			<div id='batch_list'>
<?php
				$batches = getAllBatches();
				foreach($batches as $batch) {
					print("<div class='batch_entry' onClick='downloadBatchData(\"".$batch->accessKey."\");'><div class='batch_name'>".$batch->name."</div><div class='batch_created'>".$batch->created."</div><div class='batch_access_key' >".$batch->accessKey."</div></div>");
				}
?>
			</div>
			<div id='work_area'></div>
		</div>
	</body>
</html>
