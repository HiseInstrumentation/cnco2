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
	</head>

	<body>
		<div id='app_content'>
			<div class='title_bar'>
				<div class='ip_section'>IP Address: <?= getIpAddress(); ?></div>&nbsp;
				<div class='menu_bar'>
					<input type='submit' value = 'Discover Components' onClick = 'componentDiscover()' />
				</div>
			</div>
			<div style='clear: both;'></div>
			<div id='work_area'>
				<div id='components'>
					<div class='section_title'>Components</div>
					<div id='component_details'></div>
				</div>
				<div id='main'>
					<div class='section_title'>Work Space</div>
					<div id='main_output'></div>
				</div>
			</div>
			<div style='clear: both;'></div>
			<div id='system_log'>
				<div class='section_title'>System Log</div>
				<div id='system_log_output'>
					<table id = 'log_table'></table>
				</div>
			</div>
        <script>
            setTimeout(updateStatus, 1000);
        </script>
	</body>
</html>
