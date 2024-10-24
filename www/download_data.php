<?php

$key = substr(trim($_GET['batch_access_key']), 0, 32);

header('Content-Type: text/csv');
header('Content-Disposition: attachment; filename="cnco2_'.$key.'.csv"');
	
$db = new SQLite3("../src/cnco2.db");
$res = $db->query("select * from sample_store where batch_access_key = '".$key."' order by collected");
while($row = $res->fetchArray()) {
	print("'".$row['batch_access_key']."','".$row['collected']."',".$row['x_pos'].",".$row['y_pos'].",".$row['o2_value'].",".$row['temp_value'].",".$row['pressure_value'].",'".$row['status']."'\n");
}
