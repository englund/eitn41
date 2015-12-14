<?php
$client = new SoapClient('service.wsdl');
$response = $client->__soapCall('multiply', array('a' => 5, 'b' => 10));
echo $response;
