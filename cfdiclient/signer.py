import base64
import hashlib

from lxml import etree

from .fiel import Fiel
from .utils import Utils


class Signer(Utils):
    """ Class that contains the methods to sign the xml file
    
    Utils -> Signer

    Instance Variables:
        nsmap (dict): namespace of the xml file
        xml_name (str): name of the xml file
    """


    nsmap = {
        None: 'http://www.w3.org/2000/09/xmldsig#'
    }

    xml_name = 'signer.xml'

    def __init__(self, fiel: Fiel) -> None:
        """Constructor of the Signer class
        
        Args:
            fiel (Fiel): Fiel Certificate object
        
        Instance Variables:
            fiel (Fiel): Fiel Certificate object
        """

        super().__init__()
        self.fiel = fiel

    def sign(self, element: etree.Element) -> etree.Element:
        """ Signs the xml file

        Args:
            element (etree.Element): Elemen t to sign
        
        Returns:
            etree.Element: Signed element
        """

        # Generates a SHA1 hash of the XML element and encodes it in base64
        element_bytes = self.element_to_bytes(element.getparent())
        element_hash = hashlib.new('sha1', element_bytes)
        element_digest = element_hash.digest()
        element_digest_base64 = base64.b64encode(element_digest)

        # Encodes the digest in base64 and sets it in the xml file
        digest_xpath = 'SignedInfo/Reference/DigestValue'
        digest_element = self.get_element(digest_xpath)
        digest_element.text = element_digest_base64

        # Signs the digest with the private key of the Fiel Certificate
        signed_info_xpath = 'SignedInfo'
        signed_info = self.get_element(signed_info_xpath)
        signed_info_bytes = self.element_to_bytes(signed_info)
        signed_info_sign = self.fiel.firmar_sha1(signed_info_bytes)

        # Sets the signature in the xml file
        xpath = 'SignatureValue'
        self.set_element_text(xpath, signed_info_sign)

        # Sets the certificate in the xml file
        xpath = 'KeyInfo/X509Data/X509Certificate'
        self.set_element_text(xpath, self.fiel.cer_to_base64())

        # Sets the issuer and serial number in the xml file
        xpath = 'KeyInfo/X509Data/X509IssuerSerial/X509IssuerName'
        self.set_element_text(xpath, self.fiel.cer_issuer())

        # Sets the serial number in the xml file
        xpath = 'KeyInfo/X509Data/X509IssuerSerial/X509SerialNumber'
        self.set_element_text(xpath, self.fiel.cer_serial_number())

        element.append(self.element_root)

        return element
