<?php
/**
 *
 */
class PeriodicTableModule /*extends Module*/ {

    private $tree; // Elements used in the plugin
    private static $referenceTree = null;

    private $dataArray; // Data associated with the tree

    private $chemicalElementList; // xxx Move it to $dataArray

	public function __construct()
	{
		$this -> dataArray = array();
        $this -> chemicalElementList = array();
	}

    public function addElement($elementName)
    {
        $elementIndex = $this -> getElementIndex($elementName);
        if($elementIndex !== -1)
            throw new Exception("Element already selected");

        array_push($this -> chemicalElementList, $elementName);
    }

    /**
     *
     */
    public function removeElement($elementName)
    {
        $elementIndex = $this -> getElementIndex($elementName);
        if($elementIndex === -1)
            throw new Exception("Element not found");

        unset($this -> chemicalElementList [ $elementIndex ]);
    }

    /**
     * Search for an element inside the
     */
    public function getElementIndex($elementName)
    {
        $elementIndex = array_search($elementName, $this -> chemicalElementList);

        if($elementIndex === FALSE)
            return -1;

        return $elementIndex;
    }

	public function setDataForElement($elementName, $elementQty, $elementErr, $elementPur = null)
	{
		if(!is_string($elementName))
			return;

		$this -> dataArray[$elementName] = array(
			'quantity' => $elementQty,
			'error' => $elementErr
		);

		if( $elementPur != null )
			$this -> dataArray[$elementName]['purity'] = $elementPur;
	}

	public function getDataForElement($elementName)
	{
		if(isset($this -> dataArray[$elementName]))
			return $this -> dataArray[$elementName];

		return null;
	}

    /**
     * Return the list of selected element
     */
    public function getElementList()
    {
        return $this -> chemicalElementList;
    }

	public function getXmlData()
	{
		return array('<test>resteest</test>');
	}




}
