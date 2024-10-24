<?php
	ini_set('display_errors', 'on');
	
	$method = $_SERVER['REQUEST_METHOD'];
	
	if($method == 'POST') {
		$action = $_POST['action'];
		switch($action) {
			case "view_data":
				$key = substr(trim($_POST['batch_access_key']), 0, 32);
				$db = new SQLite3("../src/cnco2.db");
				$res = $db->query("select * from sample_store where batch_access_key = '".$key."' order by collected");
				print("<a href = 'download_data.php?batch_access_key=".$key."'>Download as CSV</a>");
				print("<table>
						<tr>
						<th>Collected</th>
						<th>X Pos</th>
						<th>Y Pos</th>
						<th>O2 %</th>
						<th>Temp C</th>
						<th>Pressure Mb</th>
						</tr>");
				while($row = $res->fetchArray()) {
					print("<tr>
								<td>".$row['collected']."</td>
								<td>".$row['x_pos'] ."</td>
								<td>".$row['y_pos'] ."</td>
								<td>".$row['o2_value'] ."</td>
								<td>".$row['temp_value'] ."</td>
								<td>".$row['pressure_value'] ."</td>
							</tr>");
				}
				$db->close();
				print("</table>");
			break;
				
		}
		
		
		
	}
