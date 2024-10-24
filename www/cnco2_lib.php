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
