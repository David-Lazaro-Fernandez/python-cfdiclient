"""cfdiclient.WebServiceRequest"""
import logging

import requests
from lxml import etree

from .fiel import Fiel
from .signer import Signer
from .utils import Utils

logger = logging.getLogger(__name__)


class WebServiceRequest(Utils):
    """Class that contains the methods to make the request to the web service
    Utils -> WenServiceRequest

    Instance Variables:
        Soap_url (str): url of the web service
        Soap_action (str): action of the web service
        Result_xpath (str): xpath of the result
        fault_xpath (str): xpath of the fault
    """

    DATE_TIME_FORMAT: str = '%Y-%m-%dT%H:%M:%S'

    soap_url: str = None
    soap_action: str = None
    result_xpath: str = None
    fault_xpath: str = 's:Body/s:Fault/faultstring'


    def __init__(self, fiel: Fiel, verify: bool = True, timeout: int = 15) -> None:
        """ Constructor of the WebServiceRequest class
        
        Args:
            fiel (Fiel): Fiel Certificate object
            verify (bool): Defaults to True. Verifies the certificate
            timeout (int): Defaults to 15. Time limit of the request

        Instance Variables:
            signer (Signer): Signer object, recieves the fiel certificate to sign the request
            verify (bool): Verifies the certificate
            timeout (int): Time limit of the request
        
        Returns:
            None
        """

        super().__init__()
        self.signer = Signer(fiel)
        self.verify = verify
        self.timeout = timeout

    def get_headers(self, token: str) -> dict:
        """Returns the headers of the request
        
        Args:
            token (str): Auth token for making the request
        
        Returns:
            headers (dict): Necesary headers for making the request
        """

        headers = {
            'Content-type': 'text/xml;charset="utf-8"',
            'Accept': 'text/xml',
            'Cache-Control': 'no-cache',
            'SOAPAction': self.soap_action,
            'Authorization': 'WRAP access_token="{}"'.format(token) if token else ''
        }
        return headers

    def set_request_arguments(self, arguments: dict) -> etree.Element:
        """Sets the arguments of the request
        
        Gets the xpath XML element of the request in the XML file
        Then iterates over the arguments and sets the values in the XML element

        Args:
            arguments (dict): Arguments to set in the request

        Returns:
            solicitud (etree.Element): Element with the arguments setted
        
        TODO:
            * Remove hardcode of RfcReceptores
            * Add more than one RFC
        """

        solicitud = self.get_element(self.solicitud_xpath)
        for key in arguments:
            if key == 'RfcReceptores':
                for i, rfc_receptor in enumerate(arguments[key]):
                    if i == 0:
                        self.set_element_text(
                            's:Body/des:SolicitaDescarga/des:solicitud/des:RfcReceptores/des:RfcReceptor',
                            rfc_receptor
                        )
                continue
            if arguments[key] != None:
                solicitud.set(key, arguments[key])
        return solicitud

    def request(self, token: str = None, arguments: dict = None) -> etree.Element:
        """Makes the request to the web service

        If arguments are passed, sets the arguments in the request
        Then signs the request by getting the signature from the signer object
        Gets the headers of the request
        Gets the XML element in bytes
        Makes the request
        Gets the response XML element
        If the status code of the response is not 200, raises an exception
        Finally returns the result of the response
        
        Args:
            token (str): Defaults to None. Auth token for making the request
            arguments (dict): Defaults to None. Arguments to set in the request
        
        Returns:
            response_xml (etree.Element): Response of the request
        """
        if arguments:
            solicitud = self.set_request_arguments(arguments)
            self.signer.sign(solicitud)

        headers = self.get_headers(token)

        soap_request = self.element_to_bytes(self.element_root)

        logger.debug('Request soap_url: %s', self.soap_url)
        logger.debug('Request headers: %s', headers)
        logger.debug('Request soap_request: %s', soap_request)

        response = requests.post(
            self.soap_url,
            data=soap_request,
            headers=headers,
            verify=self.verify,
            timeout=self.timeout,
        )

        logger.debug('Response headers: %s', response.headers)
        logger.debug('Response text: %s', response.text)

        try:
            response_xml = etree.fromstring(
                response.text,
                parser=etree.XMLParser(huge_tree=True)
            )
        except Exception:
            raise Exception(response.text)

        if response.status_code != requests.codes['ok']:
            error = self.get_element_external(response_xml, self.fault_xpath)
            raise Exception(error)

        return self.get_element_external(response_xml, self.result_xpath)
