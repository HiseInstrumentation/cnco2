<?php
	ini_set('display_errors', 'on');
	
	$method = $_SERVER['REQUEST_METHOD'];
	
	if($method == 'POST') {
	    $action = $_POST['action'];
	    $db = new SQLite3("../src/cnco2.db");
	    $db->busyTimeout(10000);


	    switch($action) {
		case 'command_status':
		    $sql = "select * from sys_command order by created desc limit 5";
		    $res = $db->query($sql);
		    $output = array();
		    while($row = $res->fetchArray()) {
			$command_line = array();
			
			$command_line['created'] = $row['created'];
			$command_line['executed'] = $row['executed'];
			$command_line['command_text'] = $row['command_text'];
			$command_line['parameters'] = $row['parameters'];
			$command_line['system_response'] = $row['system_response'];
			$command_line['ui_block'] = $row['ui_block'];
			
			$output[] = $command_line;
		    }
		    print(json_encode($output));
		break;
		case 'component_discover':
		   $sql = "insert into sys_command values ('', CURRENT_TIMESTAMP, 'COMP_DISCOVERY', '', '', '', 1)";
		   $db->query($sql);
		   print("");                  
		break;
		case 'component_get_all':
		    $gantry_found = 
		    $o2_found = false;
		    $temp_count = 0;
		    
		    $sql = "select * from gantry";
		    $res = $db->query($sql);
		    $row = $res->fetchArray();
		    
		    if($row['serial'] != "") {
			$gantry_found = true;
			print("<div class = 'component_button' onClick = 'show_gantry_control();'>Gantry</div>");
		    }
		    
		    $sql = "select * from o2_sensor";
		    $res = $db->query($sql);
		    $row = $res->fetchArray();
		    
		    if($row['serial'] != "") {
			$o2_found = true;
			print("<div class = 'component_button' onClick = 'show_o2_control();'>Sendot O2 Sensor</div>");
		    }
		    
		    $sql = "select * from temp_controller";
		    $res = $db->query($sql);
		    while($row = $res->fetchArray()) {
			$temp_count++;
			print("<div class = 'component_button' onClick = 'show_temp_control(\"".$row['device_id']."\");'>".$row['device_id']."</div>");
		    }
		    
		    if( (($temp_count == 4) && $o2_found && $gantry_found)) {
			print("All Components Found");
		    }
		    

		break;
		case 'system_check':
		    $sys_status = array();
		    
		    $res = shell_exec("ps ax | grep main");
		    
		    if(!stristr($res, 'cnco2_main')) {
			$sys_status['running'] = false;
		    } else {
			$sys_status['running'] = true;
		    } 
		    
		    print(json_encode($sys_status));
		break;
		case 'component_gantry_status':
		    $res = array();
		    
		    $sql = "select * from gantry";
		    $res = $db->query($sql);
		    $row = $res->fetchArray();
		    
		    print(json_encode($row));
		break;
		case 'component_gantry_home':
		    $sql = "insert into sys_command values ('', CURRENT_TIMESTAMP, 'COMP_COMMAND', '', '', 'command_type=GANTRY_HOME', 1)";
		    $db->query($sql);
		    $res = array();
		    $res['response'] = 'Gantry Homed';
		    print(json_encode($res));
		break;
		case 'component_gantry_move':
		    $move_x = floatval(substr(trim($_POST['x']),0,10));
		    $move_y = floatval(substr(trim($_POST['y']),0,10));
		    
		    if(($move_x >= 0 && $move_x <= 200) && ($move_y >= 0 && $move_y <= 200)) {
			$sql = "insert into sys_command values ('', CURRENT_TIMESTAMP, 'COMP_COMMAND', '', '', 'command_type=ADJUST_GANTRY&x=".$move_x."&y=".$move_y."', 1)";
			$db->query($sql);
			$res = array();
			$res['response'] = 'Gantry Moving To x:'.$move_x.' y:'.$move_y;
			print(json_encode($res));
		    }
		    
		    
		break;
		
		case 'component_gantry_adjust':
		break;
		case 'component_temp_set':
		    $controller_id = substr(trim($_POST['controller_id']), 0, 40);
		    $target_temp = floatval(substr(trim($_POST['target_temp']), 0, 10));
		    $sql = "insert into sys_command values ('', CURRENT_TIMESTAMP, 'COMP_COMMAND', '', '', 'command_type=TEMP_SET&controller_id=".$controller_id."&target_temp=".$target_temp."', 0)";
		    $db->query($sql);
		    sleep(5);
		    $sql = "select * from temp_controller where device_id='".$controller_id."'";
		    $res = $db->query($sql);
		    $row = $res->fetchArray();
		    print(json_encode($row));
		break;
		case 'component_temp_stop':
		    $controller_id = substr(trim($_POST['controller_id']), 0, 40);
		    $sql = "insert into sys_command values ('', CURRENT_TIMESTAMP, 'COMP_COMMAND', '', '', 'command_type=TEMP_STOP&controller_id=".$controller_id."', 0)";
		    $db->query($sql);
		    sleep(4);
		    $sql = "select * from temp_controller where device_id='".$controller_id."'";
		    $res = $db->query($sql);
		    $row = $res->fetchArray();
		    print(json_encode($row));
		break;
		case 'component_temp_stat':
		    $controller_id = substr(trim($_POST['controller_id']), 0, 40);
		    $sql = "insert into sys_command values ('', CURRENT_TIMESTAMP, 'COMP_COMMAND', '', '', 'command_type=TEMP_STAT&controller_id=".$controller_id."', 0)";
		    $db->query($sql);
		    sleep(5);
		    $sql = "select * from temp_controller where device_id='".$controller_id."'";
		    $res = $db->query($sql);
		    $row = $res->fetchArray();
		    print(json_encode($row));
		break;
		case 'component_o2_read':
		    $sql = "insert into sys_command values ('', CURRENT_TIMESTAMP, 'COMP_COMMAND', '', '', 'command_type=O2_READ', 0)";
		    $db->query($sql);
		    sleep(5);
		    $sql = "select * from o2_sensor";
		    $res = $db->query($sql);
		    $row = $res->fetchArray();
		    print(json_encode($row));
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
