# -*- coding: utf-8 -*-
from .webservicerequest import WebServiceRequest
import datetime

class SolicitaDescarga(WebServiceRequest):
    """ Class that contains the methods to make a request to the SolicitaDescarga web service
    
    WebServiceRequest -> SolicitaDescarga

    Instance Variables:
        xml_name (str): name of the xml file
        soap_url (str): url of the web service
        soap_action (str): action of the web service
        solicitud_xpath (str): xpath of the request
        result_xpath (str): xpath of the resulxt
    """


    xml_name = 'solicitadescarga.xml'
    soap_url = 'https://cfdidescargamasivasolicitud.clouda.sat.gob.mx/SolicitaDescargaService.svc'
    soap_action = 'http://DescargaMasivaTerceros.sat.gob.mx/ISolicitaDescargaService/SolicitaDescarga'
    solicitud_xpath = 's:Body/des:SolicitaDescarga/des:solicitud'
    result_xpath = 's:Body/SolicitaDescargaResponse/SolicitaDescargaResult'

    def solicitar_descarga(
        self, 
        token:str, 
        rfc_solicitante:str, 
        fecha_inicial: datetime.date , 
        fecha_final: datetime.date,
        rfc_emisor:str = None:, 
        rfc_receptor:str = None:, 
        tipo_solicitud:str = 'CFDI',
        tipo_comprobante:str = None, 
        estado_comprobante:str = None, 
        rfc_a_cuenta_terceros:str = None, 
        complemento=None, 
        uuid=None
    ):
        """Makes a request to the SolicitaDescarga web service
        
        Args:
            token (str): Auth token for making the request
            rfc_solicitante (str): RFC of the requester
            fecha_inicial (datetime.date): Initial date of the request
            fecha_final (datetime.date): Final date of the request
            rfc_emisor (str): RFC of the issuer
            rfc_receptor (str): RFC of the receiver
            tipo_solicitud (str): Defaults to 'CFDI'. Type of the request
            tipo_comprobante (str): Defaults to None. Type of the comprobante
            estado_comprobante (str): Defaults to None. State of the comprobante
            rfc_a_cuenta_terceros (str): Defaults to None. RFC of the third party
            complemento (str): Defaults to None. Complement of the request
            uuid (str): Defaults to None. UUID of the request

        Returns:
            ret_val (dict) Dictionary with the response of the request containing the following keys:
            {
                'id_solicitud'(str):  
                'cod_estatus'(str): 
                'mensaje' (str):
            }
        """


        arguments = {
            'RfcSolicitante': rfc_solicitante,
            'FechaFinal': fecha_final.strftime(self.DATE_TIME_FORMAT),
            'FechaInicial': fecha_inicial.strftime(self.DATE_TIME_FORMAT),
            'TipoSolicitud': tipo_solicitud,
            'TipoComprobante': tipo_comprobante,
            'EstadoComprobante': estado_comprobante,
            'RfcACuentaTerceros': rfc_a_cuenta_terceros,
            'Complemento': complemento,
            'UUID': uuid,
        }

        if rfc_emisor:
            arguments['RfcEmisor'] = rfc_emisor

        if rfc_receptor:
            arguments['RfcReceptores'] = [rfc_receptor]

        element_response = self.request(token, arguments)

        ret_val = {
            'id_solicitud': element_response.get('IdSolicitud'),
            'cod_estatus': element_response.get('CodEstatus'),
            'mensaje': element_response.get('Mensaje')
        }

        return ret_val
