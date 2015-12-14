<?php

function multiply($a, $b) {
    return $a * $b;
}

$server = new SoapServer('service.wsdl');
$server->addFunction('multiply');
$server->handle();
