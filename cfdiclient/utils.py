import os

from lxml import etree


class Utils():
    """Class that contains the methods to read the xml files
    
    Instance Variables:
        internal_nsmap (dict): namespaces of the xml file
        external_nsmap (dict): external namespaces of the xml file
        xml_name (str): name of the xml file
    """

    internal_nsmap = {
        's': 'http://schemas.xmlsoap.org/soap/envelope/',
        'o': 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd',
        'u': 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd',
        'des': 'http://DescargaMasivaTerceros.sat.gob.mx',
        '': 'http://www.w3.org/2000/09/xmldsig#',
        #'': 'http://DescargaMasivaTerceros.gob.mx',
    }

    external_nsmap = {
        '': 'http://DescargaMasivaTerceros.sat.gob.mx',
        's': 'http://schemas.xmlsoap.org/soap/envelope/',
        'u': 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd',
        'o': 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd',
        'h':'http://DescargaMasivaTerceros.sat.gob.mx',
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'xsd': 'http://www.w3.org/2001/XMLSchema',
    }

    xml_name: str = None

    def __init__(self) -> None:
        """Constructor of the Utils class

        Instance Variables:
           read_xml (method): Gets the xml file and returns the root element, gets as an argument the name of the xml file
        """
        self.read_xml(self.xml_name)

    def read_xml(self, xml_name: str) -> etree.Element:
        """Gets the xml file and returns the XML root element
        
        Args:
            xml_name (str): name of the xml file
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        xml_path = os.path.join(current_dir, xml_name)
        parser = etree.XMLParser(remove_blank_text=True)
        self.element_root = etree.parse(xml_path, parser).getroot()
        return self.element_root

    def get_element(self, xpath: str) -> etree.Element:
        """Returns the XML element from the XML root element
        
        Returns:
            element (etree.Element): Element from the root element
        """

        return self.element_root.find(xpath, self.internal_nsmap)

    def get_element_external(self, element: etree.Element, xpath: str) -> etree.Element:
        """Returns the external XML element from the XML root element
        
        Returns:
            element (etree.Element): External element from the root element
        """
        
        return element.find(xpath, self.external_nsmap)

    def set_element_text(self, xpath: str, text: str) -> None:
        """Sets the text of the element to create"""
        element = self.element_root.find(xpath, self.internal_nsmap)
        element.text = text

    @classmethod
    def element_to_bytes(cSalels, element: etree.Element) -> bytes:
        """Returns the element in bytes
        
        returns:
            etree.tostring(element, method='c14n', exclusive=1) (bytes): Element in bytes   
        """        
        return etree.tostring(element, method='c14n', exclusive=1)
