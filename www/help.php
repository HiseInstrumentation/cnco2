
<!DOCTYPE HTML>
<html>
	<head>
		<title>CNCO2 - Griffin Lab</title>
		<link rel="stylesheet" href='default.css'>
		<script type='text/javascript' src = 'js/cnco2.js'></script>
	</head>

	<body>
		<div id='app_content'>
			<blockquoet>
			<h1>CNCO2 Usage Instructions</h1><br />
<br />
<h2>Summary:</h2>

<blockquote>This software package contains a set of command line python3 scripts
that allow the user to run the CNCO2 O2 Sampling Machine.</blockquote>
<br />
<h3>Procedure Summaries</h3>
<blockquote>
<b>Run the machine with samples:</b>
<ol>
<li>Create a batch from a template.</li>
<li>Get the batch access key from step 1.</li>
<li>Run the batch using the batch access key.</li>
<li>Access the dataset generated by the run via the built in webpage (http://localhost/).</li>
</ol>

<b>View available Templates:</b>
<ol>
	<li>Run the template details script</li>
</ol>

<b>View available batches:</b>
<ol>
	<li>Run the batch details script with no arguments</li>
</ol>

<b>View details about a specific batch</b>
<ol>
	<li>Run the batch deetails script with the batch access key</li>
</ol>

<b>Export dataset associated with a batch on the command line</b>
<ol>
	<li>Run the data export script</li>
</ol>

<b>Pause the machine while it is running</b>
<ol>
	<li>Use the start script</li>
</ol>

<b>Resume machine operation after being paused</b>
<ol>
	<li>Use the stop script</li>
</ol>

<b>Monitor output log while machine is in operation</b>
<ol>
	<li>Use tail command on output log as shown below.</li>
</ol>
<code> tail -f ./cnco2_log.txt</code>
<br />
<br />
<b>NOTE:</b>
<blockquote>All scripts should be run from the /src/ folder</blockquote>
<br />
<code>> cd Development/cnco2/src/</code>
</blockquote>

<h3>Scripts and Usage</h3>
<blockquote>

<b>View available templates</b><br /><br />

<code>python3 ./cnco2_template_details.py</code><br /><br />

Not the "Access Key" value as you will need this to create a batch.<br /><br />

<b>Create a new sample batch from a template</b><br /><br />

<code>python3 ./cnco2_batch_create.py TEMPLATE_NAME ["USERS NAME"]</code><br /><br />

This will output the new batch access key.  If you pass in the second
parameter, the batch will have that name instead of the template
name.<br /><br />


<b>Run a sample batch</b><br /><br />

<code>python3 ./cnco2_run.py BATCH_ACCESS_KEY</code><br /><br />

This will start the complete run. Ouput will be stored in cnco2_log.txt.
Also monitor the output of this script as a low signal error will 
pause execution until it is resolved.<br /><br />

<b>Pause a batch run in progress</b><br /><br />

<code>python3 ./cnco2_stop.py</code><br /><br />

<b>Resume a paused batch run</b><br /><br />

<code>python3 ./cnco2_start.py</code><br /><br />

<b>Get a list of batchs</b><br /><br />

<code>python3 ./cnco2_batch_details.php</code><br /><br />

<b>Get details of a specific batch</b><br /><br />

<code>python3 ./cnco2_batch_details.php BATCH_ACCESS_KEY</code><br /><br />

<b>Export sampl data to CSV file.</b><br /><br />

<code>python ./cnco2_data_export.py BATCH_ACCESS_KEY</code><br /><br />
</blockquote>

		</div>
	</body>
</html>
