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
				<div class='menu_bar'>
                    <input type='submit' value = 'Discover Components' onClick = 'componentDiscover()' />
                </div>
			</div>
			<div>
			</div>
			<div id='work_area'></div>
            <div id='components'></div>
		</div>
        <script>
            setTimeout(getComponents, 1000);
        </script>
	</body>
</html>
