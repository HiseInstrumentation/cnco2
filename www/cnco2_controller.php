<?php
	ini_set('display_errors', 'on');
	
	$method = $_SERVER['REQUEST_METHOD'];
	
	if($method == 'POST') {
		$action = $_POST['action'];
        $db = new SQLite3("../src/cnco2.db");

		switch($action) {
            case 'component_discover':
               $sql = "insert into sys_command values ('', CURRENT_TIMESTAMP, 'COMP_DISCOVERY', '', '', '')";
               $db->query($sql);
               print("Comp Discovery Requested");                  
            break;
            case 'component_get_all':
                $sql = "select * from gantry";
                $res = $db->query($sql);
                $row = $res->fetchArray();
                print("Gantry: ".$row['serial']."<br />");

                $sql = "select * from o2_sensor";
                $res = $db->query($sql);
                $row = $res->fetchArray();
                print("O2 Sensor: ".$row['serial']."<br />");

                $sql = "select * from temp_controller";
                $res = $db->query($sql);
                while($row = $res->fetchArray()) {
                    print("Temp Controller: ".$row['device_id']."<br />");
                }

            break;
            case 'component_gantry_home':
            break;
            case 'component_gantry_adjust':
            break;
            case 'component_temp_set':
            break;
            case 'component_temp_stop':
            break;
            case 'component_temp_stat':
            break;
            case 'component_o2_read':
            break;
          
			case "view_data":
				$key = substr(trim($_POST['batch_access_key']), 0, 32);
				$db = new SQLite3("../src/cnco2_data.db");
				$res = $db->query("select * from sample_store where batch_access_key = '".$key."' order by collected");
				print("<a href = 'download_data.php?batch_access_key=".$key."'>Download as CSV</a>");
				print("<table>
						<tr>
						<th>Collected</th>
						<th>Type</th>
						<th>X Pos</th>
						<th>Y Pos</th>
						<th>O2 %</th>
						<th>Temp C</th>
						<th>Pressure Mb</th>
						</tr>");
				while($row = $res->fetchArray()) {
					$sample_type = ($row['sample_type'] == 0) ? 'Sample' : (($row['sample_type'] == 1) ? 'Control' : 'Blank');
					print("<tr>
								<td>".$row['collected']."</td>
								<td>".$sample_type ."</td>
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
