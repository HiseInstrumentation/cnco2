<?php

function getIpAddress()
{
	$matches = array();
	$res = exec("ifconfig | grep 'inet 192'");
	preg_match("/192\.168\.[0-9]*\.[0-9]*/", $res, $matches);
	return $matches[0];
}

function getAllBatches()
{
	$db = new SQLite3("../src/cnco2.db");
	$res = $db->query("select * from batch order by created desc");
	$batches = array();

	while($row = $res->fetchArray()) {
		$b = new Batch();
		$b->name = $row['name'];
		$b->description = $row['description'];
		$b->accessKey = $row['access_key'];
		$b->created = $row['created'];

		$batches[] = $b;
	}

	$db->close();
	return $batches;
}

function getBatchDetails($batch_access_key)
{

}

function systemStop()
{

}

function systemStart()
{

}

function systemStatus()
{

}

class Batch 
{
	public $name;
	public $description;
	public $accessKey;
	public $created;

}
