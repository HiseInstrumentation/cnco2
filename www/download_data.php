<?php

$key = substr(trim($_GET['batch_access_key']), 0, 32);

header('Content-Type: text/csv');
header('Content-Disposition: attachment; filename="cnco2_'.$key.'.csv"');
	
$db = new SQLite3("../src/cnco2_data.db");
$res = $db->query("select * from sample_store where batch_access_key = '".$key."' order by collected");
print("Access Key,Collected,Type,X Pos,Y Pos,O2 %,Temp C, Pressure Mb,Status\n");
while($row = $res->fetchArray()) {
	$sample_type = ($row['sample_type'] == 0) ? 'Sample' : (($row['sample_type'] == 1) ? 'Control' : 'Blank');
	print($row['batch_access_key'].",".$row['collected'].",".$sample_type.",".$row['x_pos'].",".$row['y_pos'].",".$row['o2_value'].",".$row['temp_value'].",".$row['pressure_value'].",".$row['status']."\n");
}
