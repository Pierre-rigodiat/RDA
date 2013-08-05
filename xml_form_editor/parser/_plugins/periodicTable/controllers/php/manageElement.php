<?php
session_start();
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/_plugins/periodicTable/core/PeriodicTableModule.php';
require_once $_SESSION['xsd_parser']['conf']['dirname'].'/parser/_plugins/periodicTable/view/PeriodicTableDisplay.php';

if( !isset($_GET['a']) || !isset($_GET['e']) )
    throw new Exception('Requested parameters missing');

$element = $_GET['e'];

if( !isset($_SESSION['xsd_parser']['modules']['pertable']['model']) )
    throw new Exception('PeriodicTable module not initialized');

$periodicTableModule = unserialize($_SESSION['xsd_parser']['modules']['pertable']['model']);
$chemicalElementIndex = $periodicTableModule -> getElementIndex($element);


switch($_GET['a'])
{
    case 'a':
        if($chemicalElementIndex !== -1)
            throw new Exception('Element already selected');

        $periodicTableModule -> addElement($element);

        break;
    case 'r':
        if($chemicalElementIndex === -1)
            throw new Exception('Element not selected');

        $periodicTableModule -> removeElement($element);

        break;
    default:
        throw new Exception('Action unknown');
        break;
}

$_SESSION['xsd_parser']['modules']['pertable']['model'] = serialize($periodicTableModule);

//var_dump($periodicTableModule);
$periodicTableDisplay = unserialize($_SESSION['xsd_parser']['modules']['pertable']['view']);

echo $periodicTableDisplay -> displayList ( $periodicTableModule -> getElementList() );
/*$elementList = $periodicTableModule -> getElementList();
foreach($elementList as $element)
{
    $elementListString .= $element;
    if($element !== end($elementList)) $elementListString .= ', ';
}

echo $elementListString;*/
