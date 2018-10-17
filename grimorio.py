#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import sys
import time
from bs4 import BeautifulSoup
import funcs #funcs.py file

# Login Details
EMAIL    = 'user@ucm.es'
PASSWORD = 'password'

# Set of base URLs to use, login, craft requests, etc
BASEURL_LOGIN_BACKEND = 'https://sso.ucm.es/simplesaml/module.php/userpasswordcaptcha/loginuserpass.php?'
BASEURL_LOGIN_FORM    = 'https://www.ucm.es/login_sso/'
BASEURL_TOKEN_VERIF    = 'https://www.ucm.es/simplesaml/module.php/saml/sp/saml2-acs.php/default-sp?'

# Response 200 returned by requests module
REP200 = "<Response [200]>"

def responsePrint(data):
    if str(data) == "<Response [200]>":
        print("> 200")
    else:
        print(data)
    time.sleep(1)

def main():
    #art based on the one by shimrod !! :)
    logo = """ 
        _.-"\\
    _.-"     \\
 ,-"          \\
( \       |    \\
 \ \     -G-    \\    
  \ \     |      \\         
   \ \         _.-;
    \ \    _.-"   :
     \ \,-"    _.-"
      \(   _.-"  
       `--"
     """
    print(logo)
    print(">  Grimorio Started.\n")

    if EMAIL == 'usuariotest@ucm.es':
        print("! Default credentials detected. Exiting..")
        exit(1)

    # Start a session so we can have persistant cookies
    session = requests.session()

    # Get the login page to scrap it
    r = session.get(BASEURL_LOGIN_FORM)

    responsePrint(r)

    # Parse Page
    page = BeautifulSoup(r.content, "html.parser")

    print("> Extracting hidden token...")

    #Warning, .find() only returns the first found value. Works great for this page.
    #https://stackoverflow.com/questions/2612548/extracting-an-attribute-value-with-beautifulsoup
    PossibleAuthState = page.find("input", {"name": "AuthState"})

    print("> Token Located: "+PossibleAuthState['value'])
    #print(PossibleAuthState['value'])



    print("> Crafting request...")

    # This is the form data that the page sends when logging in
    login_data = {
        'username': EMAIL,
        'password': PASSWORD,
        'AuthState': PossibleAuthState['value'],
    }

    print("> Accessing unified login...")

    # Authenticate
    r = session.post(BASEURL_LOGIN_BACKEND, data=login_data)

    responsePrint(r)

    #filename = "dumpBiblioWeb1.html"
    #file = open(filename, "wb")
    #file.write(bytes(r.text, 'utf-8'))
    #file.close()

    print("> Crafting verification(damn lazy web programmers)...")
    
    page = BeautifulSoup(r.content, "html.parser")

    hiddenVal1= page.find("input", {"name": "SAMLResponse"})
    hiddenVal2= page.find("input", {"name": "RelayState"})

    #THIS WILL RAISE AN ERROR IF THE LOGIN FIALS (IE: WRONG CREDENTIALS)
    #Here's a good place for error catching
    #print("> hidden value1: ")
    #print(hiddenVal1['value'])

    #print("> hidden value2: ")
    #print(hiddenVal2['value'])

    #################3
    login_data2 = {
        'SAMLResponse': hiddenVal1['value'],
        'RelayState': hiddenVal2['value'],
    }

    r = session.post(BASEURL_TOKEN_VERIF, data=login_data2)

    responsePrint(r)

    print("############### SESSION OBTAINED! ################\n")
    '''
    If you have reached this section, you now have a working session for scraping/playing ;)
    It took me a lot of effort to reverse/understand the login form chain so make sure to give it a great use!!!
    -Pedro
    '''

    funcs.bookRenew(session)

    
    
    

    #close session
    #r = session.post('https://ucm.on.worldcat.org/signout')






if __name__ == '__main__':
    main()
