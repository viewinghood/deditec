# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 10:17:52 2017
1. time git 17.03.2019

@author: Richard Heming
Treiber und Wrapper-Funktionen für DELIB (WIN10 tested)
"""
import sys, os
import datetime
#import time

try:
    from ctypes import CDLL, c_ulong,c_float,c_char_p,sizeof,create_string_buffer
except ImportError:
    print("Hm, cannot find the ctypes?! Please check with Python pip first!")
    sys.exit(1)
if (os.name=='nt'): 
    try:
        bib = CDLL("delib64")
    except OSError:
        print("Hm, cannot find the DELIB64.DLL. Please install driver first!")
        sys.exit(1)

class Delib(object):
    """
    Delib() - Warpper class zur DELIB Library (optional Modulnummer)
    """
    # defines from delib.h
    # Module-ID's
    RO_USB1 =	7 # RO-USB-Serie
    RO_USB 	=	7 # RO-USB-Serie
    # Special Function-Codes
    DAPI_SPECIAL_CMD_GET_MODULE_CONFIG	 = 0x01
    DAPI_SPECIAL_CMD_TIMEOUT = 0x02
    DAPI_SPECIAL_CMD_DA = 0x06
    DAPI_SPECIAL_CMD_AD = 0x09
    # values for PAR1
    DAPI_SPECIAL_GET_MODULE_CONFIG_PAR_AD = 4
    DAPI_SPECIAL_GET_MODULE_CONFIG_PAR_DA = 5
    # values for  A/D and D/A Modes
    DAPI_ADDA_MODE_UNIPOL_10V								= 0x00
    DAPI_ADDA_MODE_UNIPOL_5V								= 0x01
    DAPI_ADDA_MODE_UNIPOL_2V5								= 0x02
        
    DAPI_ADDA_MODE_BIPOL_10V								= 0x40
    DAPI_ADDA_MODE_BIPOL_5V									= 0x41
    DAPI_ADDA_MODE_BIPOL_2V5								= 0x42
    # we don't have this mode installed
    #DAPI_ADDA_MODE_0_20mA									= 0x80
    #DAPI_ADDA_MODE_4_20mA									= 0x81
    #DAPI_ADDA_MODE_0_24mA									= 0x82
    #DAPI_ADDA_MODE_0_25mA									= 0x83
    #DAPI_ADDA_MODE_0_50mA									= 0x84
        
    DAPI_ADDA_MODE_BI_CAL_MODE								= 0xfd
    #DAPI_ADDA_MODE_0_20mA_TESTMODE							= 0xfe
    DAPI_ADDA_MODE_BIPOL_10V_TESTMODE						= 0xff
        
    DAPI_ADDA_MODE_DA_DISABLE								= 0x100
    DAPI_ADDA_MODE_DA_ENABLE								= 0x200
    # special for AD
    DAPI_SPECIAL_AD_READ_MULTIPLE_AD						= 1
    DAPI_ADDA_MODE_PREVENT_DAPI_MODE_ERROR				= 0x8000
    # special for D/A timeouts
    DAPI_SPECIAL_TIMEOUT_SET_VALUE_SEC					= 1
    DAPI_SPECIAL_TIMEOUT_ACTIVATE							= 2
    DAPI_SPECIAL_TIMEOUT_DEACTIVATE						= 3
    DAPI_SPECIAL_TIMEOUT_GET_STATUS						= 4
    # special for D/A
    DAPI_SPECIAL_DA_PAR_DA_LOAD_DEFAULT					= 1
    DAPI_SPECIAL_DA_PAR_DA_SAVE_EEPROM_CONFIG			= 2
    DAPI_SPECIAL_DA_PAR_DA_LOAD_EEPROM_CONFIG			= 3
        
    # values for A/D and D/A units
    DAPI_ADDA_UNIT_ILLEGAL									= 0x00
    DAPI_ADDA_UNIT_VOLT										= 0x01
    DAPI_ADDA_UNIT_MA								       = 0x02
    # defines from delib_error_codes.h
    DAPI_ERR_NONE = 0


    def __init__(self, Number=0):
        """
        Initialisierung der *delib64.dll* (WIN10)
        """
        self.bib = CDLL("delib64")
        self.number = Number
        self.handle = 0
        self.version = 0
        self.createModule()
        #self.debugModule()
        #print("init object! Handle is: ", self.handle)
        
    
    # Verwaltungsfunktionen RO-USB
    def createModule(self):
        """
        Diese Funktion öffnet ein bestimmtes Modul (optional Nummer)
        """
        self.bib.DapiOpenModule.argtypes = [c_ulong, c_ulong]
        self.bib.DapiOpenModule.restype = c_ulong
        try:
            self.handle = self.bib.DapiOpenModule(self.RO_USB, self.number)
        except self.handle == 0:
            print("Opps, cannot OPEN the DediTec! Check USB-Cables to Module!")
            sys.exit(1)
            
    def debugModule(self):
        """
        Diese Funktion gibt die installierte DELIB-Version zurück.
        """
        self.bib.DapiGetDELIBVersion.argtypes = [c_ulong, c_ulong]
        self.bib.DapiGetDELIBVersion.restype = c_ulong
        self.version = self.bib.DapiGetDELIBVersion(0, 0)
        print("DELIB-Treiber Version: (hex) ", hex(self.version))
        print("init debug! Handle is: ", self.handle)

    def clearModule(self):
        """
        Dieser Befehl schliesst ein geöffnetes Modul.
        """
        self.bib.DapiCloseModule.argtypes = [c_ulong]
        self.bib.DapiCloseModule.restype = None # void
        try:
            init = self.bib.DapiCloseModule(self.handle)
            
            print("Module closed! Error: ", init )
        except OSError as err:
            print("There was no module to close?!!\n" \
                  "Message:", err.args)
            
    def showModuleConfig(self):
        """
        Diese Funktion gibt die Hardwareaustattung 
        (Anzahl der analogen Ein- bzw. Ausgangskanäle) der Module zurück.
        """
        self.bib.DapiSpecialCommand.argtypes = \
                            [c_ulong, c_ulong, c_ulong, c_ulong, c_ulong]
        self.bib.DapiSpecialCommand.restype = c_ulong
        ad_ch = self.bib.DapiSpecialCommand(self.handle, \
                            self.DAPI_SPECIAL_CMD_GET_MODULE_CONFIG,
                                self.DAPI_SPECIAL_GET_MODULE_CONFIG_PAR_AD,0,0)
        da_ch = self.bib.DapiSpecialCommand(self.handle, \
                            self.DAPI_SPECIAL_CMD_GET_MODULE_CONFIG,
                                self.DAPI_SPECIAL_GET_MODULE_CONFIG_PAR_DA,0,0)
        if ad_ch == 0 or da_ch == 0:
            print("####Please power the Deditec USB-Interface!\n"\
                  "Number of analog in's =",ad_ch, \
                                 "Numer of digital out's =",da_ch )
            print("Sorry, I give up :-x")
            sys.exit(1)
        else:
            print("Anzahl der digitalen Ausgangskanäle: ",da_ch)
            print("Anzahl der analogen Eingangskanäle: ",ad_ch)
            
    def lastError(self):
        """
        Diese Funktion gibt die Hardwareaustattung 
        (Anzahl der Ein- bzw. Ausgangskanäle) des Moduls zurück.
        Return: Fehler Code. 0=kein Fehler!
        """
        self.bib.DapiGetLastError.argtypes = [] # None geht nicht?!
        self.bib.DapiGetLastError.restype = c_ulong
        error = self.bib.DapiGetLastError()
        if error > self.DAPI_ERR_NONE:
            print("Delib error number: {", hex(error),"}")
        else:
            #print("OK",end="", flush=True)
            pass
            
    def lastErrorText(self):
        """
        Diese Funktion liest den Text des letzten erfassten Fehlers.
        """
        self.bib.DapiGetLastErrorText.argtypes = [c_char_p, c_ulong]
        self.bib.DapiGetLastErrorText.restype = c_ulong
        msg = create_string_buffer(500)
        #print("wir haben diese Nachricht:",self.msg,"Länge:",sizeof(self.msg))
        error = bib.DapiGetLastErrorText(msg,sizeof(msg))
        str = msg.value.decode()  # was byte-string b'....
        #print(str(self.msg.value))
        if error != self.DAPI_ERR_NONE:
            print('{',str,'}')
        else:
            #100
            pass

    # RO-USB-16*A/D analoge Eingabe-Funktionen mit 16-Bit
    def analogAdSetMode(self, Channel: c_ulong, Mode: c_ulong, Debug: int = 0) -> None:
        """
       Dieser Befehl konfiguriert den Spannungsbereich für einen A/D Wandler.
       Return: Keiner.
       Folgende Modi werden unterstützt:
       (diese sind abhängig von dem verwendeten A/D-Modul)
       Unipolare Spannungen:
           ADDA_MODE_UNIPOL_10V
           ADDA_MODE_UNIPOL_5V
           ADDA_MODE_UNIPOL_2V5 (not supported!)
       Bipolare Spannungen:
           ADDA_MODE_BIPOL_10V
           ADDA_MODE_BIPOL_5V
           ADDA_MODE_BIPOL_2V5 5 (not supported!)
       Ströme: (not installed!)
           ADDA_MODE_0_20mA 
           ADDA_MODE_4_20mA
           ADDA_MODE_0_24mA
           ADDA_MODE_0_25mA
           ADDA_MODE_0_50mA
        """
        self.bib.DapiADSetMode.argtypes = [c_ulong, c_ulong, c_ulong]
        self.bib.DapiADSetMode.restype = None # void
        self.bib.DapiADSetMode(self.handle, Channel, Mode)
        print("Channel",Channel,"set.")
        if Debug == 1:        
            self.lastError()
            self.lastErrorText()

    def analogAdGetMode(self,Channel, Debug=0):        
        """
        Dieser Befehl liest den eingestellten Modus eines A/D Wandlers zurück. 
        Modus-Beschreibung siehe help(myobj.analogAdSetMode).
        Return: Modus des A/D Wandlers.
        """
        self.bib.DapiADGetMode.argtypes = [c_ulong, c_ulong]
        self.bib.DapiADGetMode.restype = c_ulong
        mode = self.bib.DapiADGetMode(self.handle, Channel)
        if Debug == 1:
            print("A/D Channel",Channel,"read. Mode is",mode)
            self.lastError()
            self.lastErrorText()
        return(mode)
        
    def analogAdGetVolt(self, Channel, Debug=0):
        """
        Dieser Befehl liest einen Datenwert von einen Kanal 
        eines A/D Wandlers in Volt.
        Return: Wert vom A/D Wandler in Volt.
        """
        self.bib.DapiADGetVolt.argtypes = [c_ulong, c_ulong]
        self.bib.DapiADGetVolt.restype = c_float
        voltage = self.bib.DapiADGetVolt(self.handle, Channel)
        if Debug == 1:
            print("A/D Channel",Channel,"read. Voltage is",voltage)
            self.lastError()
            self.lastErrorText()
        return(voltage)

    def analogAdGetDigit(self, Channel, Debug=0):
        """
        Dieser Befehl liest einen Datenwert von einen Kanal eines A/D Wandlers.
        Return: Wert vom A/D Wandler in Digits.
        """    
        self.bib.DapiADGet.argtypes = [c_ulong, c_ulong]
        self.bib.DapiADGet.restype = c_ulong
        digit = self.bib.DapiADGet(self.handle, Channel)
        print("Channel",Channel,"read. Digit is",digit)
        if Debug == 1:
            self.lastError()
            self.lastErrorText()
        return(digit)
    
    def analogAdGetMAmps(self, Channel, Debug=0):
        """
        Dieser Befehl liest einen Datenwert von einen Kanal eines A/D Wandlers in mA.
        Return: Dieser Befehl ist Modul abhängig. 
        Er funktioniert natürlich nur, wenn das Modul auch den Strom-Modus unterstützt.
        """    
        self.bib.DapiADGetmA.argtypes = [c_ulong, c_ulong]
        self.bib.DapiADGetmA.restype = c_float
        current = self.bib.DapiADGetmA(self.handle, Channel)
        print("Channel",Channel,"read. Current is",current,"mA.")
        if Debug == 1:
            self.lastError()
            self.lastErrorText()
        return(current)
    
    def analogAdGetMultiple(self, Startchannel, Stopchannel, Debug=0):
        """
        Dieser Befehl speichert die Werte bestimmer, benachbarter Kanäle eines
        A/D Wandlers gleichzeitig in einen Zwischenpuffer.
        So können anschließend die Werte nacheinander ausgelesen werden. 
        Vorteil hierbei ist, dass die A/D-Werte zum einen gleichzeitig gepuffert
        werden, zum anderen können die Werte (im Vergleich zum Befehl DapiADGet) 
        anschließend schneller abgefragt werden.
        Return. Keiner! Werte müssen einzeln mit den Funktionen gelesen werden.
        """     
        self.bib.DapiSpecialCommand.argtypes = \
                            [c_ulong, c_ulong, c_ulong, c_ulong, c_ulong]
        self.bib.DapiSpecialCommand.restype = None # void
        self.bib.DapiSpecialCommand(self.handle, \
                    self.DAPI_SPECIAL_CMD_AD, self.DAPI_SPECIAL_AD_READ_MULTIPLE_AD, \
                    Startchannel,Stopchannel)
        #print("Buffering analog values from ch",Startchannel,"to",Stopchannel)

        if Debug == 1:
            self.lastError()
            self.lastErrorText()
#            return( {print("Multi-Ch",Startchannel,"Voltage:", \
#                       self.analogAdGetVolt(0x8000+Startchannel)) \
#                      for Startchannel in range(Startchannel,Stopchannel+1)} )
            return( { Startchannel:self.analogAdGetVolt(0x8000+Startchannel) \
                     for Startchannel in range(Startchannel,Stopchannel+1)})
        else:
            # get a list here:
            #return( list(self.analogGetVolt(0x8000+Startchannel) \
                      #for Startchannel in range(Startchannel,Stopchannel+1)) )
            # I like dicts ;-)
            return( { Startchannel:self.analogAdGetVolt(0x8000+Startchannel) \
                      for Startchannel in range(Startchannel,Stopchannel+1)})     

    # RO-USB-8*D/A analoge Ausgabe-Funktionen mit 16-Bit
    def analogDaTimeoutOn(self, Sekunden, Hundertmillisekunden, Debug=0):
        """
        Dieser Befehl dient zum Setzen UND aktivieren der Timeout-Zeit.
        Argumente sind (Sekunden, Hundertmillisekunden, [Debug=1])
        Return: Keiner. [debug: 0 (kein TO), 1 (TO aktiv), 2 (TO passiert)]
        """
        self.bib.DapiSpecialCommand.argtypes = \
                            [c_ulong, c_ulong, c_ulong, c_ulong, c_ulong]
        self.bib.DapiSpecialCommand.restype = None # void
        self.bib.DapiSpecialCommand(self.handle, \
                self.DAPI_SPECIAL_CMD_TIMEOUT, self.DAPI_SPECIAL_TIMEOUT_SET_VALUE_SEC, \
                    Sekunden, Hundertmillisekunden) # set and...
        self.bib.DapiSpecialCommand(self.handle, self.DAPI_SPECIAL_CMD_TIMEOUT, \
                self.DAPI_SPECIAL_TIMEOUT_ACTIVATE, 0, 0) # ...activate
        timeout_status = self.analogDaTimeoutStatus()
        if Debug == 1 and timeout_status == 1:
            print("Timeout aktiv mit",Sekunden,"s,",Hundertmillisekunden,"ms.")
        return(timeout_status)

    def analogDaTimeoutOff(self, Debug=0):
        """
        Dieser Befehl dient zum deaktivieren des Timeout.
        Argumente ([Debug=1])
        Return: Keiner. [debug: 0 (kein TO), 1 (TO aktiv), 2 (TO passiert)]
        """
        self.bib.DapiSpecialCommand.argtypes = \
                            [c_ulong, c_ulong, c_ulong, c_ulong, c_ulong]
        self.bib.DapiSpecialCommand.restype = None
        self.bib.DapiSpecialCommand(self.handle, self.DAPI_SPECIAL_CMD_TIMEOUT, \
                self.DAPI_SPECIAL_TIMEOUT_DEACTIVATE, 0, 0) # ...switch off TO 
        timeout_status = self.analogDaTimeoutStatus() # check it...
        if Debug == 1 and timeout_status == 0:
            print("Timeout off:",timeout_status)
        else:
            return(timeout_status)

    def analogDaTimeoutStatus(self, Debug=0):
        """
        Dieser Befehl dient zum Auslesen des Timeout-Status.
        Argumente ([Debug=1])
        Return: 0 (kein TO), 1 (TO aktiv), 2 (TO passiert)
        """
        self.bib.DapiSpecialCommand.argtypes = \
                            [c_ulong, c_ulong, c_ulong, c_ulong, c_ulong]
        self.bib.DapiSpecialCommand.restype = c_ulong
        timeout_status = self.bib.DapiSpecialCommand(self.handle,\
            self.DAPI_SPECIAL_CMD_TIMEOUT, \
                self.DAPI_SPECIAL_TIMEOUT_GET_STATUS, 0, 0) # ...switch off TO 
        if Debug == 1:
            print("Timeout no/yes/done:",timeout_status)
        else:
            return(timeout_status)
						
    def analogDaSetMode(self,Channel,Mode, Debug=0):
        """
        Dieser Befehl setzt den den Spannungsbereich für einen D/A Wandler.
        Return: Keiner.
        Folgende Modi werden unterstützt:
        (diese sind abhängig von dem verwendeten A/D-Modul)
        Unipolare Spannungen:
           ADDA_MODE_UNIPOL_10V
           ADDA_MODE_UNIPOL_5V
           ADDA_MODE_UNIPOL_2V5 (not supported!)
        Bipolare Spannungen:
           ADDA_MODE_BIPOL_10V
           ADDA_MODE_BIPOL_5V
           ADDA_MODE_BIPOL_2V5 5 (not supported!)
        Ströme: (not installed!)
           ADDA_MODE_0_20mA 
           ADDA_MODE_4_20mA
           ADDA_MODE_0_24mA
           ADDA_MODE_0_25mA
           ADDA_MODE_0_50mA
        """
        self.bib.DapiDASetMode.argtypes = [c_ulong, c_ulong, c_ulong]
        self.bib.DapiDASetMode.restype = None # void
        self.bib.DapiDASetMode(self.handle, Channel, Mode)
        print("Channel",Channel,"set.")
        if Debug == 1:        
            self.lastError()
            self.lastErrorText()

    def analogDaGetMode(self,Channel, Debug=0):        
        """
        Dieser Befehl liest den eingestellten Modus eines A/D Wandlers zurück. 
        Modus-Beschreibung siehe help(myobj.analogDaSetMode).
        Return: Modus des D/A Wandlers.
        """
        self.bib.DapiDAGetMode.argtypes = [c_ulong, c_ulong]
        self.bib.DapiDAGetMode.restype = c_ulong
        mode = self.bib.DapiDAGetMode(self.handle, Channel)
        if Debug == 1:
            print("D/A Channel",Channel,"read. Mode is",mode)
            self.lastError()
            self.lastErrorText()
        return(mode)
        
    def analogDaSetVolt(self, Channel, Voltage, Debug=0):
        """
        Dieser Befehl setzt eine Spannung an einen Kanal eines D/A Wandlers.
        Return: Keiner.
        """
        self.bib.DapiDASetVolt.argtypes = [c_ulong, c_ulong, c_float]
        self.bib.DapiDASetVolt.restype = None
        self.bib.DapiDASetVolt(self.handle, Channel, Voltage)
        if Debug == 1:
            print("D/A Channel",Channel,"set. Voltage is",Voltage)
            self.lastError()
            self.lastErrorText()
        #return(voltage)

    def analogDaSetDigit(self, Channel, Digit, Debug=0):
        """
        Dieser Befehl übergibt ein Datenwert an einen Kanal eines D/A Wandlers.        
        Return: Keiner.
        """    
        self.bib.DapiDASet.argtypes = [c_ulong, c_ulong, c_ulong]
        self.bib.DapiDASet.restype = None
        self.bib.DapiDASet(self.handle, Channel, Digit)
        #print("Channel",Channel,"read. Digit is",digit)
        if Debug == 1:
            self.lastError()
            self.lastErrorText()
        #return(digit)

    def analogDaSetZero(self, Startchannel, Stopchannel=None, Debug=0):
        """
        Mit diesem Befehl wird die Default Konfiguration eines D/A Wandlers geladen. 
        Der D/A Wandler Kanal wird sofort auf die Ausgabespannung 0V gesetzt.
        Argumente (Startchannel, [Stopchannel>=Startchannel], [Debug=1])
        Return: Keiner. 
        """       
        self.bib.DapiSpecialCommand.argtypes = \
                            [c_ulong, c_ulong, c_ulong, c_ulong, c_ulong]
        self.bib.DapiSpecialCommand.restype = None
        if Stopchannel == None or Stopchannel == Startchannel:
            #Stopchannel = 
            for Startchannel in range(Startchannel, Startchannel+1):
                self.bib.DapiSpecialCommand(self.handle, self.DAPI_SPECIAL_CMD_DA, \
                    self.DAPI_SPECIAL_DA_PAR_DA_LOAD_DEFAULT, Startchannel, 0) 
                print("D/A Channel",Startchannel,"set to zero volts.")
        else:
            for Startchannel in range(Startchannel, Stopchannel+1):
                self.bib.DapiSpecialCommand(self.handle, self.DAPI_SPECIAL_CMD_DA, \
                    self.DAPI_SPECIAL_DA_PAR_DA_LOAD_DEFAULT, Startchannel, 0) 
                print("D/A Channel",Startchannel,"set to zero volts.")            

    def analogDaSaveVolts(self, Startchannel, Stopchannel=None, Debug=0):
        """
        Mit diesem Befehl wird die aktuelle D/A Wandler Einstellung 
        (Spannung/Strom-Wert, Enable/Disable und D/A Wandler Modus) in das EEPROM gespeichert.
        Diese Spannungswerte gelten bei einem/mehreren Kanal/Kanälen dann
        beim Einschalten bzw. nach einem Timeout eines D/A Wandlers (EEPROM-Konfiguration).
        Argumente (Startchannel, [Stopchannel>=Startchannel], [Debug=1])
        Return: Keiner. 
        """        
        self.bib.DapiSpecialCommand.argtypes = \
                            [c_ulong, c_ulong, c_ulong, c_ulong, c_ulong]
        self.bib.DapiSpecialCommand.restype = None
        if Stopchannel == None or Stopchannel == Startchannel:
            #Stopchannel = 
            for Startchannel in range(Startchannel, Startchannel+1):
                self.bib.DapiSpecialCommand(self.handle, self.DAPI_SPECIAL_CMD_DA, \
                    self.DAPI_SPECIAL_DA_PAR_DA_SAVE_EEPROM_CONFIG, Startchannel, 0) 
                print("D/A Channel",Startchannel,"voltage saved.")
        else:
            for Startchannel in range(Startchannel, Stopchannel+1):
                self.bib.DapiSpecialCommand(self.handle, self.DAPI_SPECIAL_CMD_DA, \
                    self.DAPI_SPECIAL_DA_PAR_DA_SAVE_EEPROM_CONFIG, Startchannel, 0) 
                print("D/A Channel",Startchannel,"voltage saved.") 

    def analogDaLoadVolts(self, Startchannel, Stopchannel=None, Debug=0):
        """
        Mit diesem Befehl wird der D/A Wandler, mit der im EEPROM gespeicherten Konfiguration, gesetzt.
        Diese Spannungswerte gelten bei einem/mehreren Kanal/Kanälen dann
        beim Einschalten bzw. nach einem Timeout eines D/A Wandlers (EEPROM-Konfiguration).
        Argumente (Startchannel, [Stopchannel>=Startchannel], [Debug=1])
        Return: Keiner. 
        """        
        self.bib.DapiSpecialCommand.argtypes = \
                            [c_ulong, c_ulong, c_ulong, c_ulong, c_ulong]
        self.bib.DapiSpecialCommand.restype = None
        if Stopchannel == None or Stopchannel == Startchannel:
            #Stopchannel = 
            for Startchannel in range(Startchannel, Startchannel+1):
                self.bib.DapiSpecialCommand(self.handle, self.DAPI_SPECIAL_CMD_DA, \
                    self.DAPI_SPECIAL_DA_PAR_DA_LOAD_EEPROM_CONFIG, Startchannel, 0) 
                print("D/A Channel",Startchannel,"prelaoded.")
        else:
            for Startchannel in range(Startchannel, Stopchannel+1):
                self.bib.DapiSpecialCommand(self.handle, self.DAPI_SPECIAL_CMD_DA, \
                    self.DAPI_SPECIAL_DA_PAR_DA_LOAD_EEPROM_CONFIG, Startchannel, 0) 
                print("D/A Channel",Startchannel,"preloaded.")

    def pingModule(self, Zeichen, Debug=0):
        """
        Dieser Befehl prüft die Verbindung zu einem geöffneten Modul.
        Argumente (Zeichenkette, [Debug=1])
        Return: Zeichenkette
        """ 
        output = ""
        self.bib.DapiSpecialCommand.argtypes =  [c_ulong, c_ulong]
        self.bib.DapiSpecialCommand.restype = c_ulong
        #print("Starting pinging with:",Zeichen)
        for string in enumerate(Zeichen):
            response = self.bib.DapiPing(self.handle, int(format(ord(string[1]), 'd')))
            #print("Interface response:",response) 
            output += chr(response)
        if Debug == 1:
            print("Starting pinging with:",Zeichen)
            print("UTF8 gives:",output)
        if Zeichen == output:
            return(0)
        else:
            return(-1) # comm error 
        #nur für Zahlen bis 255!
#        response = self.bib.DapiPing(self.handle, Zeichen) # Zahl!!!
#        print(response)
        #format(ord(Zeichen[0]), 'd') ist ein "str"!!
        

if __name__ == "__main__": # if imported as module, don't test it..
        
    delib = Delib() # name of the class
    delib.debugModule() 
    #delib.clearModule()
    #delib.clearModule()
    delib.showModuleConfig()
    delib.pingModule( "Ping!")
    delib.lastError()
    delib.lastErrorText()
    delib.analogAdSetMode(15,delib.DAPI_ADDA_MODE_BIPOL_10V)
    delib.analogAdGetMode(15)
    delib.analogAdGetVolt(1)
    voltslist = delib.analogAdGetMultiple(0,10,0)
    print(voltslist)
    voltslist = delib.analogAdGetMultiple(0,10,1)
    print(voltslist)
    print(voltslist[0])
    print(voltslist[9])
    print("##### digital stuff ####")
    delib.analogDaTimeoutOn(10,0,1)
    delib.analogDaTimeoutStatus(1)
    delib.analogDaSetMode(1,delib.DAPI_ADDA_MODE_UNIPOL_5V)
    delib.analogDaSetVolt(1,0.05   ,1)
    #delib.analogDaSetZero(1, None,1)
    delib.analogDaSetZero(5, 9,1)
    delib.analogDaSaveVolts(11,None,1)
    delib.analogDaGetMode(1,1) # Bipolar 10V...
    
    # Delib() Test mit Rampe beim D/A...
    print("Start time interval measurement")
    start_time = datetime.datetime.now().time().strftime('%H:%M:%S')
#    for waveform in range(2): #1000 "periods"
#        for voltage in range(0,65535,64): #32767
#            delib.analogDaSetDigit(1,voltage) # und raus
    
    end_time = datetime.datetime.now().time().strftime('%H:%M:%S')
    total_time=(datetime.datetime.strptime(end_time,'%H:%M:%S') - datetime.datetime.strptime(start_time,'%H:%M:%S'))
    print (total_time) # 26s for 8192 digits written...gives 3,17ms/digit
    delib.analogDaTimeoutOff(1)   
    delib.clearModule() 