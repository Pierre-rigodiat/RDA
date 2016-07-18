import xerces_wrapper
import sys
import argparse

def main(argv):
    xsd_string = None
    xml_string = None
    error = ""

    parser = argparse.ArgumentParser(description="Validate XML Schema and Documents")
    required_arguments = parser.add_argument_group("Required Argument")
    
    required_arguments.add_argument ('-xsd', '--xsd-string', help='String containing the XML Schema', nargs=1, required=True)
    parser.add_argument('-xml', '--xml-string', help='String containing the XML Document to be validated', nargs=1)
    
    args = parser.parse_args()
    
    # get the XSD string
    xsd_string = args.xsd_string[0]
    
    if args.xml_string:
        xml_string = args.xml_string[0]
        error = xerces_wrapper.validate_xml(xsd_string, xml_string)
    else:
        error = xerces_wrapper.validate_xsd(xsd_string)

    print error

        
def usage():        
    print 'usage: python xerces_wrapper_cmd.py -xsd <xsd_string> -xml <xml_string>'
    
if __name__ == "__main__":
    main(sys.argv[1:])