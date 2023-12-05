# -*- coding: utf-8 -*-
import base64

from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from OpenSSL import crypto


class Fiel():
    """ Class that contains the methods to load, and import the FIEL certificate and key"""
    
    def __init__(self, cer_der, key_der, passphrase):
        """ Constructor of the Fiel class
        
        Args:
            cer_der (str): Certificate in DER format
            key_der (str): Key in DER format
            passphrase (str): Passphrase of the key

        Instance Variables:
            __importar_cer__ (method): Imports the certificate in DER format
            __importar_key__ (method): Imports the key in DER format
        """

        self.__importar_cer__(cer_der)
        self.__importar_key__(key_der, passphrase)

    def __importar_cer__(self, cer_der):
        """ Imports the certificate in DER format   
        
        Args:
            cer_der (str): Certificate in DER format
        """
        self.cer = crypto.load_certificate(crypto.FILETYPE_ASN1, cer_der)

    def __importar_key__(self, key_der, passphrase):
        """ Imports the key in DER format
       
        Args:
            key_der (str): Key in DER format
            passphrase (str): Passphrase of the key
        """
        self.key = RSA.importKey(key_der, passphrase)
        self.signer = PKCS1_v1_5.new(self.key)

    def firmar_sha1(self, texto):
        """Generates a SHA1 hash of the text and signs it with the key

        Args:
            texto (str): Text to sign
        
        Returns:
            b64_firma (str): Signed text in base64
        """
        sha1 = SHA.new(texto)
        firma = self.signer.sign(sha1)
        b64_firma = base64.b64encode(firma)
        return b64_firma

    def cer_to_base64(self):
        """ Extracts the certfiicate in DER format and converts it to base64
        
        Returns:
            cer (str): Certificate in base64
        """
        cer = crypto.dump_certificate(crypto.FILETYPE_ASN1, self.cer)
        return base64.b64encode(cer)

    def cer_issuer(self):
        """ Extracts the issuer of the certificate and generates a string
        
        Returns: 
            issuer (str): String with the issuer of the certificate
        """
        d = self.cer.get_issuer().get_components()
        return u','.join(['{key}={value}'.format(key=key.decode(), value=value.decode()) for key, value in d])

    def cer_serial_number(self):
        """ Extracts the serial number of the certificate and generates a string
        
        Returns:
            serial (str): String with the serial number of the certificate
        """
        serial = self.cer.get_serial_number()
        return str(serial)
