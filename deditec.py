# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 10:17:52 2017
1. time git 17.03.2019
2. deposited in try/ipe for further development

@author: Richard Heming
Treiber und Wrapper-Funktionen für DELIB (WIN10 tested)


Annotations for functions
https://stackoverflow.com/questions/38286718/what-does-def-main-none-do

Version
1.2 (09.12.2024)
- error counter48GetCount(Startchannel, Width=32) musste mit Width=32 augerufen werden!
- Fehler wird jetzt durchgegeben, wenn kein Netzwerkkabel angeschlossen! (l. 248)
- Miniänderung jetzt bei DAsetVolt usw.
- try to load the linux .so libs...
- try the command DapiOpenModuleEx - this works for the linux .so lib!
- self. is missing in line 417
"""
import sys, os
#import datetime
import time

try:
    from ctypes import (CDLL, c_ulong,c_float, c_char_p, sizeof, c_char, c_ulonglong,
                        create_string_buffer, byref, Structure, pointer, POINTER)

except ImportError:
    print("Hm, cannot find the ctypes?! Please check with Python pip first!")
    sys.exit(1)
# if os.name=='nt': 
#     try:
#         bib = CDLL("delib64")
#     except OSError:
#         print("Hm, cannot find the DELIB64.DLL. Please install driver first!")
#         sys.exit(1)
# elif os.name=='posix': # linux!
#     try:
#         bib = CDLL("/home/ipe/deditec/delib-sources/delib/lib/build_x64/old_delib.so")
#     except OSError:
#         print("Hm, cannot find the linux .so library. Please look for the driver!")
#         sys.exit(1)        
# DRIVER_NUM = 0 # first driver/ instrument 

class Delib(object):
    """
    Delib() - Warpper class zur DELIB Library (optional Modulnummer)
    """
    # defines from delib.h
    # ( in WIN from ..Program Files\DEDITEC\DELIB64\include\delib.h)
    # RO-Module-ID's
    
    RO_SER  =   5 # RO-SER-Serie
    RO_USB1 =	7 # RO-USB-Serie
    RO_USB 	=   7 # RO-USB-Serie
    RO_ETH  =   8 # RO-ETH-Serie
    RO_CAN	=   11 # RO-CAN-Serie
    RO_CAN2	=   24	# RO-CPU2 / 480 MBit/sec - CAN VERSION
    RO_USB2 =   25	# RO-CPU2 / 480 MBit/sec - USB/SER Version
    RO_ETH_LC = 26	# RO-ETH-LC
    # Special Function-Codes
    DAPI_SPECIAL_CMD_GET_MODULE_CONFIG	= 0x01
    DAPI_SPECIAL_CMD_TIMEOUT            = 0x02
    DAPI_SPECIAL_CMD_DA                 = 0x06
    DAPI_SPECIAL_CMD_COUNTER            = 0x08
    DAPI_SPECIAL_CMD_AD                 = 0x09
    DAPI_SPECIAL_CMD_CNT48				= 0x0b
    # values for PAR1
    DAPI_SPECIAL_GET_MODULE_CONFIG_PAR_DI 				=	1
    DAPI_SPECIAL_GET_MODULE_CONFIG_PAR_DI_FF 			=	7
    DAPI_SPECIAL_GET_MODULE_CONFIG_PAR_DI_COUNTER 		=	8
    DAPI_SPECIAL_GET_MODULE_CONFIG_PAR_DO 				=   2
    DAPI_SPECIAL_GET_MODULE_CONFIG_PAR_DX				=	3
    DAPI_SPECIAL_GET_MODULE_CONFIG_PAR_AD				=	4
    DAPI_SPECIAL_GET_MODULE_CONFIG_PAR_DA				=	5
    DAPI_SPECIAL_GET_MODULE_CONFIG_PAR_TEMP				=	9
    DAPI_SPECIAL_GET_MODULE_CONFIG_PAR_STEPPER			=	6
    DAPI_SPECIAL_GET_MODULE_CONFIG_PAR_CNT48			=	10
    DAPI_SPECIAL_GET_MODULE_CONFIG_PAR_PULSE_GEN		=	11
    DAPI_SPECIAL_GET_MODULE_CONFIG_PAR_PWM_OUT			=	12
    DAPI_SPECIAL_GET_MODULE_CONFIG_PAR_HW_INTERFACE1	=	13
    DAPI_SPECIAL_GET_MODULE_CONFIG_PAR_SW_FEATURE1		=	14
    DAPI_SPECIAL_GET_MODULE_CONFIG_PAR_HW_GROUP			=	15
    DAPI_SPECIAL_GET_MODULE_CONFIG_PAR_SW_CLASS			=	16
    DAPI_SPECIAL_GET_MODULE_CONFIG_PAR_MODULE_ID		=	17
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
    # special for CNT8 units
    DAPI_CNT48_FILTER_20ns								= 0x0000
    DAPI_CNT48_FILTER_100ns								= 0x1000
    DAPI_CNT48_FILTER_250ns								= 0x2000
    DAPI_CNT48_FILTER_500ns								= 0x3000
    DAPI_CNT48_FILTER_1us								= 0x4000
    DAPI_CNT48_FILTER_2_5us								= 0x5000
    DAPI_CNT48_FILTER_5us								= 0x6000
    DAPI_CNT48_FILTER_10us								= 0x7000
    DAPI_CNT48_FILTER_25us								= 0x8000
    DAPI_CNT48_FILTER_50us								= 0x9000
    DAPI_CNT48_FILTER_100us								= 0xA000
    DAPI_CNT48_FILTER_250us								= 0xB000
    DAPI_CNT48_FILTER_500us								= 0xC000
    DAPI_CNT48_FILTER_1ms								= 0xD000
    DAPI_CNT48_FILTER_2_5ms								= 0xE000
    DAPI_CNT48_FILTER_5ms								= 0xF000
    
    DAPI_CNT48_MODE_COUNT_RISING_EDGE					= 0x0000
    # DAPI_CNT48_MODE_COUNT_RISING_EDGE_X2              	= 0x0001
    # DAPI_CNT48_MODE_COUNT_RISING_EDGE_X4              	= 0x0002
    DAPI_CNT48_MODE_T									= 0x000D
    DAPI_CNT48_MODE_FREQUENCY							= 0x000E
    DAPI_CNT48_MODE_PWM									= 0x000F
    
    DAPI_CNT48_SUBMODE_NO_RESET							= 0x0000
    DAPI_CNT48_SUBMODE_RESET_WITH_READ 					= 0x0010
    DAPI_CNT48_SUBMODE_NO_RESET_NO_HW_RESET             = 0x0020
    DAPI_CNT48_SUBMODE_RESET_WITH_READ_NO_HW_RESET      = 0x0030
    DAPI_CNT48_SUBMODE_RESET_ON_CH_7 					= 0x0070
    DAPI_CNT48_SUBMODE_LATCH_COMMON 					= 0x0080
    DAPI_CNT48_SUBMODE_FREQUENCY_TIME_BASE_1ms			= 0x0030
    DAPI_CNT48_SUBMODE_FREQUENCY_TIME_BASE_10ms			= 0x0020
    DAPI_CNT48_SUBMODE_FREQUENCY_TIME_BASE_100ms		= 0x0010
    DAPI_CNT48_SUBMODE_FREQUENCY_TIME_BASE_1sec			= 0x0000
    # specials for cnt8...
    DAPI_SPECIAL_COUNTER_LATCH_ALL						= 1
    DAPI_SPECIAL_COUNTER_LATCH_ALL_WITH_RESET			= 2
    DAPI_SPECIAL_COUNTER_PRELOAD_SET					= 3
    DAPI_SPECIAL_COUNTER_PRELOAD_GET					= 4
    DAPI_SPECIAL_COUNTER_MODE_SET						= 5
    DAPI_SPECIAL_COUNTER_MODE_GET						= 6
    DAPI_CPECIAL_COUNTER_GET							= 7
    
    DAPI_SPECIAL_CNT48_RESET_SINGLE						= 1
    DAPI_SPECIAL_CNT48_RESET_GROUP8						= 2
    DAPI_SPECIAL_CNT48_LATCH_GROUP8						= 3
    DAPI_SPECIAL_CNT48_DI_GET1							= 4
    
    # specials for DI units
    

    
    
    # defines from delib_error_codes.h
    DAPI_ERR_NONE = 0


    def __init__(self, Interface="USB", Number=0):
        """
        Initialising  of *delib64.dll* (WIN10)
            a 64-bit driver is expected.
            Number is the digit when more than one Interface of a Kind
            is configured..!
        """
        # self.bib = CDLL("delib64") # this will NOT fail...
        if os.name=='nt': 
            try:
                self.bib = CDLL("delib64")
            except OSError:
                print("Hm, cannot find the DELIB64.DLL. Please install driver first!")
                sys.exit(1)
        elif os.name=='posix': # linux!
            try:
                # lib compiled from "old" sources derived from "ethernet_sample.c"
                self.bib = CDLL("/home/ipe/deditec/delib-sources/delib/lib/build_x64/old_delib.so")
            except OSError:
                print("Hm, cannot find the linux .so library. Please look for the driver!")
                sys.exit(1)         
        self.interface = Interface
        self.number = 0 #Number
        self.handle = 0
        self.version = 0

        if self.interface == "USB":
            self.createModule(self.RO_USB)
        elif self.interface == "ETH":
            self.createModule(self.RO_ETH)
        elif self.interface == "ETH_LC":
            self.createModule(self.RO_ETH_LC)
        else:
            print("Valid interfaces are USB or ETH and ETH/LC. Default ist USB.")
            sys.exit(1)
        #self.debugModule()
        #print("init object! Handle is: ", self.handle)
        
    
    # Verwaltungsfunktionen RO-USB...RO_ETH...RO_ETH/LC
    def createModule(self, Interface = RO_USB):
        """
        Diese Funktion öffnet ein bestimmtes Modul (optional Nummer)
        """
        self.bib.DapiOpenModule.argtypes = [c_ulong, c_ulong ]
        self.bib.DapiOpenModule.restype = c_ulong

        class EX_BUFFER(Structure): # ...see delib.h for definition!
            _fields_ = [("address", (c_char*256) ),
                        ("timeout", c_ulong),
                        ("portno", c_ulong)] 
        # if not configured use DapiModuleEx
        self.bib.DapiOpenModuleEx.argtypes = [c_ulong, c_ulong, POINTER(EX_BUFFER), c_ulong ]
        self.bib.DapiOpenModuleEx.restype = c_ulong
        # ppy doc 3.7: # c_char_p is a pointer to a string
        # but we cannot easyly convert structure to char *
        ##buffer = EX_BUFFER( b'192.168.178.25', 500, 9912 ) # make it! @home
        buffer = pointer(EX_BUFFER( b'192.168.0.10', 1500, 9912 ) )# make it!
    
        self.interface = Interface

        if self.interface == self.RO_USB:
            try:
                self.handle = self.bib.DapiOpenModule(self.interface, self.number)
                if self.handle == 0:
                    raise ValueError
                # falls ein handle auf ein 'ETH' existiert, wird dies nicht abgefangen :)
            except ValueError:
                print("Cannot OPEN the DediTec with USB! Check USB-Cables to Module!")
                #sys.exit(1)  # RO-Series only..!
        elif self.interface == self.RO_ETH_LC: # low cost version has own id!
            try:
                ## self.handle = 0 # for testing ONLY!
                self.handle = self.bib.DapiOpenModuleEx(self.RO_ETH_LC, self.number,
                                            buffer, 0)      
                # funktioniert!
                #self.handle = self.bib.DapiOpenModule(self.interface, self.number)
                if self.handle == 0:
                    raise ValueError
            except ValueError: #self.handle == 0:
                print("Cannot OPEN the DediTec/LC with Ethernet!", 
                      "\n Check first IP-Address in DELIB-Config!",
                      "\nthen check also TP-Cables to Module!")
                print("No handle available: ", self.handle)
                print("\n Did you install the driver?!")
                raise
                #sys.exit(1)  # RO-Series only..!                
        elif self.interface == self.RO_ETH:
            try:
                self.handle = self.bib.DapiOpenModuleEx(self.RO_ETH, self.number,
                                            byref(buffer), 0)
                # 1. buffer = pointer(EX_BUFFER( b'192.168.178.25', 500, 9912 ) )# make it!
                #    self.handle = self.bib.DapiOpenModuleEx(self.RO_ETH, self.number,
                #                                    buffer, 0)
                # --> is working!
                # 2. buffer = EX_BUFFER( b'192.168.178.25', 500, 9912 ) # make it!
                #    self.handle = self.bib.DapiOpenModuleEx(self.RO_ETH, self.number,
                #                            byref(buffer), 0)
                # --> is working, too..!
                
                #print("das handle ist: ", self.handle)
                if self.handle == 0:
                    raise ValueError
            except ValueError:
                print("Cannot OPEN the DediTec over Ethernet! Check TP-Cables to Module!")
                sys.exit(1)  # RO-Series only..!
        else:
            # the progam can  never come to this line..! 
            # ok, for Debugging "NONE"
            try:
                if self.handle is None:
                    raise ValueError
            except ValueError: #self.handle == 0:
                print("normally the program cannot be in this state :-o")
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
        except (OSError, TypeError):
            print("There was no module to close...")           
#            print("There was no module to close?!!\n" \
#                  "Message:", err.args)
            
    def showModuleConfig(self):
        """
        Diese Funktion gibt die Hardwareaustattung 
        (Anzahl der analogen Ein- bzw. Ausgangskanäle) der Module zurück.
        Argumente sind alle Submodule, die angeschafft wurden ;-)
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
        din_ch = self.bib.DapiSpecialCommand(self.handle, \
                            self.DAPI_SPECIAL_CMD_GET_MODULE_CONFIG,
                                self.DAPI_SPECIAL_GET_MODULE_CONFIG_PAR_DI,0,0)
        din_ff_ch = self.bib.DapiSpecialCommand(self.handle, \
                            self.DAPI_SPECIAL_CMD_GET_MODULE_CONFIG,
                                self.DAPI_SPECIAL_GET_MODULE_CONFIG_PAR_DI_FF,0,0)
        din_cnt_ch = self.bib.DapiSpecialCommand(self.handle, \
                            self.DAPI_SPECIAL_CMD_GET_MODULE_CONFIG,
                                self.DAPI_SPECIAL_GET_MODULE_CONFIG_PAR_DI_COUNTER,0,0)

        dout_ch = self.bib.DapiSpecialCommand(self.handle, \
                            self.DAPI_SPECIAL_CMD_GET_MODULE_CONFIG,
                                self.DAPI_SPECIAL_GET_MODULE_CONFIG_PAR_DO,0,0)
        cnt48_ch = self.bib.DapiSpecialCommand(self.handle, \
                            self.DAPI_SPECIAL_CMD_GET_MODULE_CONFIG,
                                self.DAPI_SPECIAL_GET_MODULE_CONFIG_PAR_CNT48,0,0)
        gen_ch = self.bib.DapiSpecialCommand(self.handle, \
                            self.DAPI_SPECIAL_CMD_GET_MODULE_CONFIG,
                                self.DAPI_SPECIAL_GET_MODULE_CONFIG_PAR_PULSE_GEN,0,0)
            

        print("\n##### Inspect the module #####")
        #print(c_ulong(ad_ch), c_ulong(da_ch))
        if ad_ch == 0 or da_ch == 0:
            print("####Please power the Deditec USB-Interface!\n"\
                  "Number of analog in's =",ad_ch, \
                                 "Numer of digital out's =",da_ch )
            print("Sorry, I give up :-x")
            sys.exit(1)
        else:
            print("Analoge Kanäle:")
            print("Anzahl der analogen Ausgangskanäle: ",da_ch)
            print("Anzahl der analogen Eingangskanäle: ",ad_ch)
            print("\nDigitale Kanäle:")
            print("Anzahl der digitalen Ausgangskanäle: ",dout_ch)
            print("Anzahl der digitalen Eingangskanäle: ",din_ch, 
                  "\n  (davon gleichzeitig Flip-Flops: ", din_ff_ch,")",
                  "\n  (und auch 16-bit Zähler: ",din_cnt_ch,")" )  
            print("\nFPGA Kanäle:")
            print("Schnelle digitale Zähler (48-bit):",cnt48_ch)
            print("Schnelle Pulsgenerator Kanäle:",gen_ch)
            
    def lastError(self):
        """
        Diese Funktion liefert den letzten erfassten Fehler.
        Argumente: keine
        Return: Fehler Code. 0=kein Fehler!
        """
        self.bib.DapiGetLastError.argtypes = [] # None geht nicht?!
        self.bib.DapiGetLastError.restype = c_ulong
        error = self.bib.DapiGetLastError()
        if error > self.DAPI_ERR_NONE:
            print("Delib error number: {", hex(error),"}")
            self.bib.DapiClearLastError()
            return(hex(error))
        else:
            #print("OK",end="", flush=True)
            return(0)

    def lastErrorText(self):
        """
        Diese Funktion liest den Text des letzten erfassten Fehlers.
        Argumente sind (Zeichenkettenbuffer und seine Länge)
        Return: Fehler Code. 0=kein Fehler!
        """
        self.bib.DapiGetLastErrorText.argtypes = [c_char_p, c_ulong]
        self.bib.DapiGetLastErrorText.restype = c_ulong
        msg = create_string_buffer(500)
        #print("wir haben diese Nachricht:",self.msg,"Länge:",sizeof(self.msg))
        error = self.bib.DapiGetLastErrorText(msg,sizeof(msg))
        text = msg.value.decode()  # was byte-string b'....
        #print(str(self.msg.value))
        if error != self.DAPI_ERR_NONE:
            print('{',text,'}')
            self.bib.DapiClearLastError()
            return(text)
        else:
            return(0)
            #pass
    
    def lastErrorClear(self):
        """
        Diese Funktion löscht den letzten Fehler, der mit DapiGetLastError() 
        erfasst wurde.
        Argumente : keine
        Return: nichts!
        """        
        self.bib.DapiClearLastError.argtypes = [] # None geht nicht?!
        self.bib.DapiClearLastError.restype = None
        #
        self.bib.DapiClearLastError()

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
        print("AD Channel",Channel,"set.")
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
        Dieser Befehl liest einen Datenwert von einen Kanal eines 
        A/D Wandlers in mA.
        Return: Dieser Befehl ist Modul abhängig. 
        Er funktioniert natürlich nur, wenn das Modul auch den Strom-Modus 
        unterstützt.
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
        Return. Dictionary mit Werten!
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
        print("DA Channel",Channel,"set.")
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
            print("DA Channel",Channel,"read. Mode is",mode)
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
        #return(print(str(Voltage)+'V')) # hier muss noch gerundet werden

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
        (Spannung/Strom-Wert, Enable/Disable und D/A Wandler Modus) in das 
        EEPROM gespeichert.
        Diese Spannungswerte gelten bei einem/mehreren Kanal/Kanälen dann
        beim Einschalten bzw. nach einem Timeout eines D/A Wandlers
        (EEPROM-Konfiguration).
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
        Mit diesem Befehl wird der D/A Wandler, mit der im EEPROM gespeicherten
        Konfiguration, gesetzt.
        Diese Spannungswerte gelten bei einem/mehreren Kanal/Kanälen dann
        beim Einschalten bzw. nach einem Timeout eines D/A Wandlers
        (EEPROM-Konfiguration).
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
            print("\nInterface check:")
            print("Starting pinging with:",Zeichen)
            print("UTF8 gives:",output)
        if Zeichen == output:
            print("...ok!")
            return(0)
        else:
            print("...error...")
            sys.exit(1)
            #return(-1) # comm error 

        #nur für Zahlen bis 255!
#        response = self.bib.DapiPing(self.handle, Zeichen) # Zahl!!!
#        print(response)
        #format(ord(Zeichen[0]), 'd') ist ein "str"!!
        
    ## CNT48 Inputs

    # ULONG  DapiCnt48ModeGet(ULONG handle, ULONG ch);
    # ULONG  DapiCnt48CounterGet32(ULONG handle, ULONG ch);
    # ULONGLONG  DapiCnt48CounterGet48(ULONG handle, ULONG ch);
    
    # ---------------------------------------
    # # CNT48 Pulse Generator Outputs
    # void DapiPulseGenSet(ULONG handle, ULONG ch, ULONG mode, ULONG par0, 
    #       ULONG par1, ULONG par2);
    # ---------------------------------------
    # # CNT48 PWM Outputs       
    # void DapiPWMOutSet(ULONG handle, ULONG ch, float data);
    # float DapiPWMOutReadback(ULONG handle32, ULONG ch);
    def counter48SetMultiple(self, Startchannel, Stopchannel=None, Debug=0): 
        """
        Mit diesem Befehl wird der CNT48 FPGA Zäler gesetzt.
        Dabei können Modi und Sub-Modi verODERt werden.
        Argumente (Startchannel, [Stopchannel>=Startchannel], [Debug=1])
        Return: Keiner. 
        """  
        # common modes  and submodes for counters
        mm = self.DAPI_CNT48_MODE_COUNT_RISING_EDGE # main mode rising edge
        mmt = self.DAPI_CNT48_MODE_T
        sm_rr = self.DAPI_CNT48_SUBMODE_RESET_WITH_READ # sub mode: Read & Reset
        sm_comla = self.DAPI_CNT48_SUBMODE_LATCH_COMMON
        sm_tp = self.DAPI_CNT48_SUBMODE_FREQUENCY_TIME_BASE_100ms # gleicher sm !!
        filt = self.DAPI_CNT48_FILTER_1us
        
        # void   DapiCnt48ModeSet(ULONG handle, ULONG ch, ULONG mode);
        self.bib.DapiCnt48ModeSet.argtypes = [c_ulong, c_ulong, c_ulong]
        self.bib.DapiCnt48ModeSet.restype = None
        if Stopchannel == None or Stopchannel == Startchannel:
            #Stopchannel = 
            for Startchannel in range(Startchannel, Startchannel+1):
                self.bib.DapiCnt48ModeSet(self.handle, Startchannel, \
                    mm | sm_rr | sm_comla | filt)
                if Debug == 0:
                    print("Single Counter Channel ",Startchannel,"configured.")
                else:
                    print("Single Counter Channel ",Startchannel,"configured.", \
                      self.counter48ModeRead(Startchannel), "register map")
        else:
            print("Multiple counter channels soon ready:")
            for Startchannel in range(Startchannel, Stopchannel+1):
                self.bib.DapiCnt48ModeSet(self.handle, Startchannel, \
                     mm | sm_rr | sm_comla | filt ) 
                if Debug == 0:
                    print("Single Counter Channel ",Startchannel,"configured.")
                else:
                    print("Single Counter Channel ",Startchannel,"configured.", \
                      self.counter48ModeRead(Startchannel), "register map")
    
    def counter48ModeRead(self, Startchannel, Stopchannel=None):
        """
        Dieser Befehl fragt die Register der Counter ab. Anhand der "map"
        kann die korrekte Betriebsweise überprüft werden.
        Kann automatisch mit dem Debug-Flag von counter48SetMultiple() aufgerufen
        werden.
        Argumente (Startchannel, [Stopchannel>=Startchannel])
        register map p. 22/23 (german pdf)
        """
        # ULONG  DapiCnt48ModeGet(ULONG handle, ULONG ch);
        self.bib.DapiCnt48ModeGet.argtypes = [c_ulong, c_ulong]
        self.bib.DapiCnt48ModeGet.restype = c_ulong        
        if Stopchannel == None or Stopchannel == Startchannel:
            #Stopchannel = 
            for Startchannel in range(Startchannel, Startchannel+1):                
                response = self.bib.DapiCnt48ModeGet(self.handle, Startchannel ) 
                #print("{:016b}".format(response))
                
                # you can choose the width !
                #return("{:016b}".format(response))
                return("{:032b}".format(response))
        else:
            pass     

    def counter48LatchAll(self, Channels=None, Debug=0): 
        """
        Dieser Befehl speichert die Zählerstände von 8 Eingangszähler 
        gleichzeitig in ein Zwischenspeicher (Latch).
        So können anschließend alle Zählerstände des Latches nacheinander 
        ausgelesen werden.
        Argumente (Channels= Low, High, All, [Debug=0]) 
        Low=0-7, High= 8-15, All=0..15 counter
        Return: Dictionary mit Werten oder 1 wenn falsche Konfiguration
        """
        # void DapiSpecialCommand(ULONG handle, DAPI_SPECIAL_CMD_CNT48, 
        #           DAPI_SPECIAL_CNT48_LATCH_GROUP8, ULONG ch, 0)
        self.bib.DapiSpecialCommand.argtypes = \
                            [c_ulong, c_ulong, c_ulong, c_ulong, c_ulong]
        self.bib.DapiSpecialCommand.restype = None # void
        
        #ch_range = Channels
        if Channels == "Low":
            ch_range = (0, )
            Startchannel = 0
            Stopchannel = 7
        elif Channels == "High":
            ch_range = (8, )  
            Startchannel = 8
            Stopchannel = 15
        elif Channels == None or Channels == "All":
            ch_range = (0,8)
            Startchannel = 0
            Stopchannel = 15
        else:
            print("No vaild counter channel configuration..!")
            self.lastError()
            self.lastErrorText()
            return(1)            
            # 
        for _, ch in enumerate(ch_range):
            self.bib.DapiSpecialCommand(self.handle, \
                    self.DAPI_SPECIAL_CMD_CNT48, \
                       self.DAPI_SPECIAL_CNT48_LATCH_GROUP8, ch, 0 )
            # print("Latched:", ch, "-",ch+7 )
                #
        if Debug == 1:  
            #self.counter48AllReset("All", Debug=1) 
            print("Latched:", ch, "-",ch+7 )
             # Debug=1 hier ist Blödsinn!
            return( { Startchannel:self.counter48GetCount(Startchannel, Width=32, Debug=1)  \
                      for Startchannel in range(Startchannel,Stopchannel+1)} )
            
            
            # return( { Startchannel:self.analogAdGetVolt(0x8000+Startchannel) \
            #          for Startchannel in range(Startchannel,Stopchannel+1)})
        else:
            # get a list here:
            #return( list(self.analogGetVolt(0x8000+Startchannel) \
                      #for Startchannel in range(Startchannel,Stopchannel+1)) )
            # I like dicts ;-)
            return( { Startchannel:self.counter48GetCount(Startchannel, Width=32) \
                      for Startchannel in range(Startchannel,Stopchannel+1)})
                
    def counter48GetCount(self, Channel, Width=None, Debug=0):
        """
        Dieser Befehl liest einen 48 Bit Zähler eines Eingangszählerkanals.
        Argumente (Channel, Width=[32|48], default=48bit, [Debug=0]) 
        Return: counter value 
        """
        #ULONGLONG DapiCnt48CounterGet48(ULONG handle, ULONG ch);
        self.bib.DapiCnt48CounterGet48.argtypes = [c_ulong, c_ulong]
        self.bib.DapiCnt48CounterGet48.restype = c_ulonglong
        # ULONG DapiCnt48CounterGet32(ULONG handle, ULONG ch);
        self.bib.DapiCnt48CounterGet32.argtypes = [c_ulong, c_ulong]
        self.bib.DapiCnt48CounterGet32.restype = c_ulong  
        
        if Width == None or Width == 48:
            # python int is big enough
            # gives the register map back
            # 0100000010010000 000000000000000000000000111111111111111111111110
            # register        - here the counter: you must mask! 
            value = self.bib.DapiCnt48CounterGet48(self.handle, Channel)
        elif Width == 32:
            value = self.bib.DapiCnt48CounterGet32(self.handle, Channel)
        else:
            print("No vaild counter width or channel for readout!")
            self.lastError()
            self.lastErrorText()
            return(1)  

        if Debug == 1:       
            return( print("Counter ", Channel,":",value))
        else:
            return( value)
        
    def counter48AllReset(self, Width=None, Debug=0):
        """
        Dieser Befehl resettet gleichzeitig die Zählerstände von 8 Eingangszählern.
        Wenn die Werte gelachted sind, sind diese davon nicht betroffen!!
        """
        # void DapiSpecialCommand(ULONG handle, DAPI_SPECIAL_CMD_CNT48, 
        #       DAPI_SPECIAL_CNT48_RESET_GROUP8, ULONG ch, 0)
        self.bib.DapiSpecialCommand.argtypes = \
                            [c_ulong, c_ulong, c_ulong, c_ulong, c_ulong]
        self.bib.DapiSpecialCommand.restype = None # void
        #
        if Width == "Low":
            ch_range = (0, )
            #Startchannel = 0
            #Stopchannel = 7
        elif Width == "High":
            ch_range = (8, )  
            #Startchannel = 8
            #Stopchannel = 15
        elif Width == None or Width == "All":
            ch_range = (0,8)
            #Startchannel = 0
            #Stopchannel = 15
        else:
            print("No vaild counter channel configuration..!")
            self.lastError()
            self.lastErrorText()
            return(1)   
            # 
        
        if Debug == 1:
            for _, ch in enumerate(ch_range):
                self.bib.DapiSpecialCommand(self.handle, \
                                        self.DAPI_SPECIAL_CMD_CNT48, \
                                self.DAPI_SPECIAL_CNT48_RESET_GROUP8, ch, 0 )           
                # print("Reset:", ch, "-",ch+7 )
                ret = 'Reset:' + str(ch) + '-' + str(ch+7)
            return( ret )
        else:
            # print("CNT8 reset...")
            for _, ch in enumerate(ch_range):
                self.bib.DapiSpecialCommand(self.handle, \
                                            self.DAPI_SPECIAL_CMD_CNT48, \
                                self.DAPI_SPECIAL_CNT48_RESET_GROUP8, ch, 0 )
            #print("Reset:", ch, "-",ch+8 )            
            return( 0)
            
    def digitalDiGet(self, Startchannel_width, Debug=0):
        """
        Dieser Befehl liest die digitalen Eingänge von 1,8 oder 16 Eingängen.
        Eine Zahl zwischen 0 und 15 liefert einen EINZELNEN entsprechenden Eingang. 
        Bezeichnungen Low, High, All liefern Ausschnitte von H oder L.
        Hier wird das Modul RO-OPTIN16 verwendet. Alle Eingägnge via Optokoppler.
        """        
        # ULONG DapiDIGet1(ULONG handle, ULONG ch)
        self.bib.DapiDIGet1.argtypes = [c_ulong, c_ulong]
        self.bib.DapiDIGet1.restype = c_ulong
        # ULONG DapiDIGet8(ULONG handle, ULONG ch)
        self.bib.DapiDIGet8.argtypes = [c_ulong, c_ulong]
        self.bib.DapiDIGet8.restype = c_ulong
        # ULONG DapiDIGet16(ULONG handle, ULONG ch)
        self.bib.DapiDIGet16.argtypes = [c_ulong, c_ulong]
        self.bib.DapiDIGet16.restype = c_ulong
        #
        if Startchannel_width in range(0,16): # is form 0..15
            if Debug == 0:
                return( self.bib.DapiDIGet1(self.handle, Startchannel_width)) # return only the int (0 or 1)
            else:
                return( print( "Digital InBit",Startchannel_width,":",self.bib.DapiDIGet1(self.handle, Startchannel_width)) )
        
        elif Startchannel_width == "Low":
            Startchannel = 0
            #Startchannel = 0
            #Stopchannel = 7
            if Debug == 0:
                return( self.bib.DapiDIGet8(self.handle, Startchannel)) # return only the int
            else:
                return( print( "Digital InByte:",Startchannel_width,"{:08b}".format(self.bib.DapiDIGet8(self.handle, Startchannel)))  )
        
        elif Startchannel_width == "High":
            Startchannel = 8
            #Startchannel = 8
            #Stopchannel = 15
            if Debug == 0:
                return( self.bib.DapiDIGet8(self.handle, Startchannel)) # return only the int
            else:
                return( print( "Digital InByte:",Startchannel_width,"{:08b}".format(self.bib.DapiDIGet8(self.handle, Startchannel))) )
        
        elif Startchannel_width == None or Startchannel_width == "All":
            Startchannel = 0
            #Startchannel = 0
            #Stopchannel = 15
            if Debug == 0:
                return( self.bib.DapiDIGet16(self.handle, Startchannel))
            else:
                return( print("Digital InWord:",Startchannel_width,"{:016b}".format(self.bib.DapiDIGet16(self.handle, Startchannel))) )
        else:
            print("No vaild digital input (DI) channel configuration..!")
            self.lastError()
            self.lastErrorText()
            return(1)   

    def digitalDiGetFF(self, Debug=0):
        """
        Dieser Befehl gibt einen Flanken-Capture (LHL) aller 16 Eingänge aus.
        Bei "Debug=1" erfolgt die Ausgabe auf die Konsole.
        Vermutlich ist ein Filter mit 100ms vorgeschaltet (default)
        Hier wird das Modul RO-OPTIN16 verwendet!
        """        
        # ULONG DapiDIGetFF32(ULONG handle, ULONG ch)
        self.bib.DapiDIGetFF32.argtypes = [c_ulong, c_ulong]
        self.bib.DapiDIGetFF32.restype = c_ulong
        #
        Startchannel = 0 # always!
        #Startchannel = 0
        #Stopchannel = 15
        if Debug == 0:
            return( self.bib.DapiDIGetFF32(self.handle, Startchannel)) # return only the int
        else:
            return( print( "InWord FF Capture:","{:016b}".format(self.bib.DapiDIGetFF32(self.handle, Startchannel)))  ) 

            
    def digitalDoSet(self, Startchannel_width=None, Data=0, Debug=0):
        """
        Dieser Befehl setzt die digitalen Ausgänge von 1,8 oder 16 Ausgängen mit 
        vorgegebenen  Werten ("Data").
        Eine Zahl zwischen 0 und 15 setzt einen EINZELNEN entsprechenden Ausgang. 
        Bezeichnungen Low, High, All setzen das Byte oder ein Word auf H oder L. 
        wird "Data" weggelassen, werden die Ausgägnge resetet!
        Hier wird das Modul RO-MOS16-2 verwendet!
        """        
        # void DapiDOSet1(ULONG handle, ULONG ch, ULONG data)
        self.bib.DapiDOSet1.argtypes = [c_ulong, c_ulong, c_ulong]
        self.bib.DapiDOSet1.restype = None # void  
        # void DapiDOSet8(ULONG handle, ULONG ch, ULONG data         
        self.bib.DapiDOSet8.argtypes = [c_ulong, c_ulong, c_ulong]
        self.bib.DapiDOSet8.restype = None # void  
        # void DapiDOSet16(ULONG handle, ULONG ch, ULONG data) 
        self.bib.DapiDOSet16.argtypes = [c_ulong, c_ulong, c_ulong]
        self.bib.DapiDOSet16.restype = None # void  
        #          
        if Startchannel_width in range(0,16): # is form 0..15
            if Data in range(0,2): # 0 or 1 or False/ True
                if Debug == 0:
                    self.bib.DapiDOGet1(self.handle, Startchannel_width, Data)
                    return(0)
                else:
                    self.bib.DapiDOSet1(self.handle, Startchannel_width, Data)
                    return( print("Digital Outupt:",Startchannel_width,":" ,Data) )
            else:
                return(1)
        
        elif Startchannel_width == "Low":
            if Data in range(0,256): # 0..255 bei 8 bit!
                Startchannel = 0
                #Startchannel = 0
                #Stopchannel = 7
                if Debug == 0:
                    self.bib.DapiDOSet8(self.handle, Startchannel, Data)
                    return(0)
                else:
                    self.bib.DapiDOSet8(self.handle, Startchannel, Data)
                    print( "Digital OutByte",Startchannel_width,": {:08b}".format(Data)) # beginnt bei MOS1 !!
                    return(0)
            else:
                return(1)
        
        elif Startchannel_width == "High":
            if Data in range(0,256): # 0..255 bei 8 bit!
                Startchannel = 8
                #Startchannel = 8
                #Stopchannel = 15
                if Debug == 0:
                    self.bib.DapiDOSet8(self.handle, Startchannel, Data)
                    return(0)
                else:
                    self.bib.DapiDOSet8(self.handle, Startchannel, Data)
                    print( "Digital OutByte",Startchannel_width,": {:08b}".format(Data))
                    return(0)
            else:
                return(1)
        
        elif Startchannel_width == None or Startchannel_width == "All":
            Startchannel = 0
            if Startchannel_width == None: 
                Startchannel_width = 'RESET'
            #Startchannel = 0
            #Stopchannel = 15
            if Debug == 0:
                self.bib.DapiDOSet16(self.handle, Startchannel, Data)
                return(0)
            else:
                self.bib.DapiDOSet16(self.handle, Startchannel, Data)
                return( print( "Digital OutWord",Startchannel_width,"{:016b}".format(Data)) )
        else:
            print("No vaild digital input (DI) channel configuration..!")
            self.lastError()
            self.lastErrorText()
            return(1)        
        
    def digitalDoGetAll(self, Debug=0):
        """
        Dieser Befehl gibt einen Readback aller 16 MOS-Ausgänge.
        Bei "Debug=1" erfolgt die Ausgabe auf die Konsole.
        Hier wird das Modul RO-MOS16-2 verwendet!
        """        
        # ULONG DapiDOReadback32(ULONG handle, ULONG ch)
        self.bib.DapiDOReadback32.argtypes = [c_ulong, c_ulong]
        self.bib.DapiDOReadback32.restype = c_ulong
        #
        Startchannel = 0 # always!
        #Startchannel = 0
        #Stopchannel = 15
        if Debug == 0:
            return( self.bib.DapiDOReadback32(self.handle, Startchannel)) # return only the int
        else:
            return( print( "Digital OutWord Readback:","{:016b}".format(self.bib.DapiDOReadback32(self.handle, Startchannel)))  )
    
    # es könen noch Bibliotheksbefehle verwendet werden, die gleichzeitig
    # einen "beliebigen" Abschnitt ändern kann. Man unterliegt dann nicht 
    # der willkürlichen Einteilung nach Low-/Highbyte oder Word.
        # her ein SET
        # void DapiDOSetBit32(uint handle, uint ch, uint data)
        # und hier ein REset
        # void DapiDOClrBit32(uint handle, uint ch, uint data)

       
        
        
if __name__ == "__main__": # if imported as module, don't test it..
        
    import logging as log
    formatter = '%(asctime)s.%(msecs)03d %(levelname)s - %(funcName)s: %(message)s'
    date_form = '%H:%M:%S'
    
    #logfile = ''
#    log_dir = os.path.join(os.path.normpath(os.environ['USERPROFILE'] + os.sep ), 'logs')
#    if not os.path.exists(log_dir):
#        os.makedirs(log_dir)                                                       
#    logfile = 'ipe-writer-log.txt'
#    logfile = os.path.join(log_dir, logfile)
    log.basicConfig(
    level=log.INFO,
    format=formatter, 
    datefmt=date_form, )
    
    delib = Delib(Interface='ETH_LC') # name of the class
    #delib = Delib(Interface='USB') # name of the class
    #delib.createModule(delib.RO_ETH)
    time.sleep(1) # needs a Timeout!!
    delib.debugModule() 
    #time.sleep(1)
    delib.lastError()
    delib.lastErrorText()
    #delib.clearModule()
    #delib.clearModule()
    delib.showModuleConfig()
    delib.pingModule( "Ping!", Debug=1)
    #time.sleep(1)
    delib.lastError()
    delib.lastErrorText()
    # #time.sleep(1)
    # delib.showModuleConfig()
    # delib.analogAdSetMode(15,delib.DAPI_ADDA_MODE_BIPOL_10V)
    # delib.analogAdGetMode(15)
#    print('AD1= ',delib.analogAdGetVolt(1) ) # Spannung in mV
    # voltslist = delib.analogAdGetMultiple(0,10,0)
    # print(voltslist)
    # voltslist = delib.analogAdGetMultiple(0,10,1)
    # print(voltslist)
    # print(voltslist[0])
    # print(voltslist[9])
    # print("##### digital stuff ####")
    delib.analogDaSetMode(0,delib.DAPI_ADDA_MODE_UNIPOL_10V,Debug=1)
    delib.analogDaSetMode(1,delib.DAPI_ADDA_MODE_UNIPOL_10V,Debug=1)
    delib.analogDaSetMode(2,delib.DAPI_ADDA_MODE_UNIPOL_10V,Debug=1)
    delib.analogDaSetMode(3,delib.DAPI_ADDA_MODE_UNIPOL_10V,Debug=1)
    delib.analogDaSetMode(4,delib.DAPI_ADDA_MODE_UNIPOL_10V,Debug=1)
    delib.analogDaSetMode(5,delib.DAPI_ADDA_MODE_UNIPOL_10V,Debug=1) 
    delib.analogDaGetMode(0, Debug=1)
    delib.analogDaGetMode(1, Debug=1)
    delib.analogDaGetMode(2, Debug=1)
    delib.analogDaGetMode(3, Debug=1)
    delib.analogDaGetMode(4, Debug=1)
    delib.analogDaGetMode(5, Debug=1)
    delib.analogDaTimeoutOn(10,0,1)
    delib.analogDaTimeoutStatus(1)
    # delib.analogDaSetMode(1,delib.DAPI_ADDA_MODE_UNIPOL_5V)
    delib.analogDaSetVolt(0,1.0   ,0)
    delib.analogDaSetVolt(1,1.1   ,0)
    delib.analogDaSetVolt(2,1.2   ,0)
    delib.analogDaSetVolt(3,1.3   ,0)
    delib.analogDaSetVolt(4,1.4   ,0)
    delib.analogDaSetVolt(5,1.5   ,0)
    delib.analogDaSetVolt(5,1.6   ,0)

    delib.analogDaTimeoutOff(1)
    # #delib.analogDaSetZero(1, None,1)
    #delib.analogDaSetZero(0, 3,1)
    # #delib.analogDaSaveVolts(11,None,1)
    # delib.analogDaGetMode(1,1) # Bipolar 10V...
    
    # # Delib() Test mit Rampe beim D/A...
    # print("\n Benchmark:")
    # print("Start time interval measurement")
    # start_time = datetime.datetime.now().time().strftime('%H:%M:%S')
    # for waveform in range(8): #1000 "periods"
    #     for voltage in range(0,65535,64): #32767
    #         delib.analogDaSetDigit(1,voltage) # und raus
    
    # end_time = datetime.datetime.now().time().strftime('%H:%M:%S')
    # total_time=(datetime.datetime.strptime(end_time,'%H:%M:%S') - datetime.datetime.strptime(start_time,'%H:%M:%S'))
    # print (total_time) # 26s for 8192 digits written...gives 3,17ms/digit
    # RO-ETH: jetzt richtig mit gelungender Kommunikation
        # Start time interval measurement
        # 0:00:08
        # -> also 8s for 8192 digits written...gives 977us/digit..YES!!
    print(delib.counter48ModeRead(1))
    delib.counter48SetMultiple(0,15, Debug=0 )
    print("individual counter read:", delib.counter48ModeRead(1) )
    print('?!', delib.counter48GetCount(0,Width=32, Debug=0))
    delib.lastError()
    delib.lastErrorText()
    print('Latch all',delib.counter48LatchAll('Low', Debug=0)) # debug=1 ist Blödsinn, gibt leeres (none) dict!
    #time.sleep(0.5)
    print(' Reset - 4s delay',delib.counter48AllReset("Low", Debug=1) )
    #time.sleep(4)
    print('Latch all',delib.counter48LatchAll('Low',Debug=0))
    #delib.counter48AllReset("All", Debug=1) 
    #delib.counter48LatchAll(Debug=1)    
    delib.lastError()
    delib.lastErrorText() 
    delib.digitalDiGet(0,Debug=1)
    delib.lastError()
    delib.lastErrorText()  
    delib.digitalDiGet("Low",Debug=1)
    delib.lastError()
    delib.lastErrorText()  
    delib.digitalDiGet("All",Debug=1)
    delib.lastError()
    delib.lastErrorText()  
    delib.digitalDoSet(1, Data=1, Debug=1)
    delib.lastError()
    delib.lastErrorText()
    delib.digitalDoSet('Low', Data=0b0101, Debug=1)
    delib.digitalDoSet('High', Data=255, Debug=1)
    delib.lastError()
    delib.lastErrorText()
    #time.sleep(2)
    #delib.digitalDoSet( Debug=1) # RESET the entire WORD !
#    delib.analogDaTimeoutOff(1) 
    delib.digitalDoGetAll(Debug=1)
    delib.lastError()
    delib.lastErrorText()
    delib.digitalDiGetFF(Debug=1)
    delib.clearModule() 
    
    
### Counter Test with Period on ch0 = Kanal 1 on the frontpanel...
# In [28]: runfile('E:/WinPython/notebooks/richard/ipe/deditec.py', wdir='E:/WinPython/notebooks/richard/ipe')
# DELIB-Treiber Version: (hex)  0x235
# init debug! Handle is:  1209474

# mit RO_ETH_LC
# init debug! Handle is:  1209474 !!! (26.08.2020, DHCP, andere IO fest...)
# define DAPI_ERR_GEN_UNKNOWN_ENCRYPTION_TYPE						0x0120
# mit RO_ETH...
# init debug! Handle is:  1209475 (26.08.2020, DHCP, andere IO fest...)
# define DAPI_ERR_GEN_UNKNOWN_ENCRYPTION_TYPE						0x0120
# Fehlermeldung..?!

# Interface check:
# Starting pinging with: Ping!
# UTF8 gives: Ping!
# ...ok!
# Multiple counter channels soon ready:
# Single Counter Channel  0 configured.
# Single Counter Channel  1 configured.
# Single Counter Channel  2 configured.
# Single Counter Channel  3 configured.
# Single Counter Channel  4 configured.
# Single Counter Channel  5 configured.
# Single Counter Channel  6 configured.
# Single Counter Channel  7 configured.
# Single Counter Channel  8 configured.
# Single Counter Channel  9 configured.
# Single Counter Channel  10 configured.
# Single Counter Channel  11 configured.
# Single Counter Channel  12 configured.
# Single Counter Channel  13 configured.
# Single Counter Channel  14 configured.
# Single Counter Channel  15 configured.
# individual counter read: 0100000110011101
# Reset: 0 - 7
# Latched: 0 - 7
# Latched: 8 - 15
# Counter  0 : 1036310
# Counter  1 : 0
# Counter  2 : 0
# Counter  3 : 0
# Counter  4 : 0
# Counter  5 : 0
# Counter  6 : 0
# Counter  7 : 0
# Counter  8 : 0
# Counter  9 : 0
# Counter  10 : 0
# Counter  11 : 0
# Counter  12 : 0
# Counter  13 : 0
# Counter  14 : 0
# Counter  15 : 0
# Reset: 0 - 7
# Module closed! Error:  None


# erstes Modul
# Uni
# 00:C0:D5:02:08:83
# 192.168.0.10
# 255.255.255.0
# 192.168.0.254
# 9912

# @home:
# nur wichtig: PIN 1 auf OFF (DHCP an)     
    
# 1. DT Module Config!! -->Check! Eventuell wieder auf DHCP = OFF stellen
# 2. DELIB Configuration Utility!