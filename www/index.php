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
		<script type='text/javascript' src = 'js/o2_control.js'></script>
		<script type='text/javascript' src = 'js/temp_control.js'></script>
		<script type='text/javascript' src = 'js/gantry_control.js'></script>
	</head>

	<body>
		<div id='app_content'>
			<div class='title_bar'>
				<div class='menu_bar'>
					<ul>
						<li>IP Address: <?= getIpAddress(); ?></li>
						<li><div class='system_status' id = 'system_status'></div></li>
					</ul>
				</div>
			</div>

			<div id='myModal' class='modal'>
				<div id = 'modal_content' class='modal-content'></div>
			</div>

			<div style='clear: both;'></div>
			<div id='work_area'>
				<div id='components'>
					<div class='section_title'>Components</div>
					<div id='component_details'></div>
					<div><input type='button' value = 'Discover Components' onClick = 'componentDiscover()' /></div>
				</div>
				<div id='main'>
					<div class='section_title'>
						<div class='section_title_caption'>Work Space</div>
						<div class='section_title_close' id='ws_close'></div>
						<div class='float_clear'></div>
					</div>
					<div id='main_output'></div>
				</div>
			</div>
			<div style='clear: both;'></div>
			<div id='system_log'>
				<div class='section_title'>Command Log</div>
				<div id='system_log_output'>
					<table id = 'log_table'></table>
				</div>
			</div>
        <script>
            setTimeout(updateStatus, 1000);
        </script>
	</body>
</html>
