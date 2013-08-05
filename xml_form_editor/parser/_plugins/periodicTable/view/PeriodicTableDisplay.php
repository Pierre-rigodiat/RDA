<?php
/**
 *
 */
class PeriodicTableDisplay {

    private $periodicTableModule;


    // private static $PERTABLE_FILE = "/parser/_plugins/periodicTable/resources/json/periodicTable.json";
    private static $PERTABLE_FILE = "../resources/json/periodicTable.json";

	public function __construct() {
        $argc = func_num_args();
        $argv = func_get_args();

        $this -> periodicTableModule = $argv[0];
	}

	public function update()
	{
		$periodicTable = unserialize($_SESSION['xsd_parser']['modules']['pertable']['model']);
		$this -> periodicTableModule = $periodicTable;
	}

    public function display()
    {
        $periodicTable = null;
        if(isset($_SESSION['xsd_parser']['modules']['pertable']['model']))
        {
            $periodicTable = unserialize($_SESSION['xsd_parser']['modules']['pertable']['model']);
        }

        $periodicTableCode = '<div class="module_title">Periodic table module</div>';

        /**
         * Parse JSON file
         */
        $rawPerTable = file_get_contents(dirname(__FILE__)."/".self::$PERTABLE_FILE);
        $jsonPerTable = json_decode($rawPerTable, true);

        $arrayPerTable = array();
        foreach ($jsonPerTable["table"] as $perTableRow) {
            $tmpPerTableRow = array();

            if(isset($perTableRow["elements"]))
            {
                foreach ($perTableRow["elements"] as $chemicalElement) {
                    $tmpPerTableRow[$chemicalElement["position"]]["name"] = $chemicalElement["name"];
                    $tmpPerTableRow[$chemicalElement["position"]]["tag"] = $chemicalElement["tag"];
                }
            }

            if(isset($perTableRow["lanthanoids"]))
            {
                foreach ($perTableRow["lanthanoids"] as $chemicalElement) {
                    $tmpPerTableRow[$chemicalElement["position"]]["name"] = $chemicalElement["name"];
                    $tmpPerTableRow[$chemicalElement["position"]]["tag"] = $chemicalElement["tag"];
                }
            }

            if(isset($perTableRow["actinoids"]))
            {
                foreach ($perTableRow["actinoids"] as $chemicalElement) {
                    $tmpPerTableRow[$chemicalElement["position"]]["name"] = $chemicalElement["name"];
                    $tmpPerTableRow[$chemicalElement["position"]]["tag"] = $chemicalElement["tag"];
                }
            }

            array_push($arrayPerTable, $tmpPerTableRow);
            unset($tmpPerTableRow);
        }

        /**
         * Draw periodic table
         */
        $periodicTableCode .= '<table id="pertable"><tbody>';

        foreach ($arrayPerTable as $perTableLine) {
            $periodicTableCode .= '<tr>';

            for($i = 0; $i < 18; $i++)
            {
                $periodicTableCode .= '<td';

                if(isset($perTableLine[$i]))
                {
                    $periodicTableCode .= ' class="'.$perTableLine[$i]['tag'];

                    in_array($perTableLine[$i]['name'], $periodicTable -> getElementList()) ? $periodicTableCode .= " selected" : FALSE;

                    $periodicTableCode .= '">';

                    $periodicTableCode .= $perTableLine[$i]['name'];
                }
                else {
                    $periodicTableCode .= '>';
                }

                $periodicTableCode .= '</td>';
            }

            $periodicTableCode .= '</tr>';
        }

        $periodicTableCode .= '</tbody></table>';

        $periodicTableCode .= 'Selected element(s):<div id="selectedElement">';

        if($periodicTable)
        {
            $periodicTableCode .= $this->displayList($periodicTable -> getElementList());
        }

        $periodicTableCode .= '</div>';

        $periodicTableCode .= '<script type="text/javascript" src="parser/_plugins/periodicTable/controllers/js/table.js"></script>';
        $periodicTableCode .= '<script>$(\'td[class^="x"]\').on(\'click\', toggleElement);</script>';

        return $periodicTableCode;
    }

    public function displayList($elementList)
    {
        $elementForm = '<ul>';

        foreach($elementList as $chemicalElement)
        {
        	$elementData = $this -> periodicTableModule -> getDataForElement($chemicalElement);
			$qty = '';
			$err = '';
			$pur = '';

			if($elementData !== NULL)
			{
				$qty = $elementData['quantity'];
				$err = $elementData['error'];

				if(isset($elementData['purity']))
					$pur = $elementData['purity'];
			}


            $elementForm .= '<li>';
            $elementForm .= '<span class="elemName">'.$chemicalElement.'</span>';
            $elementForm .= '<ul>';

            $elementForm .= '<li>Quantity <input class="qty" type="text" value="'. $qty .'"/></li>';
            $elementForm .= '<li>Error <input class="err" type="text" value="'. $err .'"/></li>';
            $elementForm .= '<li>Purity <input class="pur" type="text" value="'. $pur .'"/> <span class="icon remove"></span></li>';

            $elementForm .= '</ul>';
            $elementForm .= '</li>';
        }

        $elementForm .= '</ul>';

        return $elementForm;
    }
}
