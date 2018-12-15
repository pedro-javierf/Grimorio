#!/usr/bin/python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib.request  # resource downloading

# Every function must have at least one parameter: the logged session
# 

def bookRenew(session):
    #Library has an additional login method page, easy to bypass

    print("> Accesing Library Account...")
    #r = session.get('https://ucm.on.worldcat.org/myaccount')
    #print(r)

    login_bib = {
        'contextInstId': '62629',
        'encodedIdpIdentity': "62629||https://shib.oclc.org/shibboleth/oclcfederation||https://sso.ucm.es/simplesaml/saml2/idp/metadata.php",
    }

    r = session.post('https://authn.sd02.worldcat.org/wayf/metaauth-ui/cmnd/wayf/selectIdp', data=login_bib) 

    print(r)
    print("Canario")

    #ahora parsea esta página y consigue el SAML
    page = BeautifulSoup(r.content, "html.parser")
    SAMLr= page.find("input", {"name": "SAMLRequest"})

    login_bib2 = {
        'contextInstId': SAMLr['value'],
    }

    r = session.post('https://sso.ucm.es/simplesaml/saml2/idp/SSOService.php', data=login_bib2)

    print(r)

    filename = "dumpBiblioWeb2.html"
    file = open(filename, "wb")
    file.write(bytes(r.text, 'utf-8'))
    file.close()
    
#def anyOtherFunction(session):
    #your code

def getPublicResource(source, filename):
    print("Obtaining: "+filename+"...")
    urllib.request.urlretrieve(str(source), str(filename))
    print("Done.")
