#***************************************************************************************************
'''
АВК ОМА Козырев С.А

03.09.18(старт)  темпермашина 2


'''
#***************************************************************************************************
from struct import *
from idlelib.multicall import r
import time
from datetime import datetime, date, timedelta   # import time
import snap7
import threading
import requests
import logging
                                            #a=123
                                            #print(bin(a))
                                            #print((-1024).to_bytes(10, byteorder='big', signed=True))
                                            #print(int.bit_length(a) )
                                            #print((1024).to_bytes(2, byteorder='big'))
                                            #print((1024).to_bytes(10, byteorder='big')
                                            #print(int.from_bytes(b'\x00\x10', byteorder='big'))
                                            #print(unpack('>f', b'<#\xd7\n'))
                                            #print(pack('>f',0.01))
                                            #print(pack('>L', 154))
                                            #print(unpack('>bb',b'\x01\x12'))
                                            #print(pack('>h', -12))
                                            #print(unpack('>h',b'\xff\xf4'))
ENGINE  = '192.168.1.11'                                           

a =[1,2,3,4]

def two_sec ():
    global l
    time.sleep(5)
    l = 1

class Siemens (object):

    def __init__ ( self, host ):
        self.client = snap7.client.Client ()
        self.client.connect (host, 0x0, 0x0)  # 0,2

    def read_input ( self, i , adr):
        r = self.client.read_area (snap7.types.areas['DB'], adr, i, 2)  # PE
        return r[0]

    def read_markers ( self, i ):
        r = self.client.read_area (snap7.types.areas['MK'], 410, i, 2)  # 1064
        return r[0]


    def read_bit ( self, a ):
        r = self.client.read_area (snap7.types.areas['MK'], 0, a, 2)
        return r[0] 


    def write_output ( self, area, data ):
        data = bytearray ([0x01])
        r = self.client.write_area (snap7.types.areas['PA'], 0, 0, data)
        return r


    def close ( self ):
        self.client.disconnect ()
    
tmp = datetime.now()    
logger = logging.getLogger("диагностика")
logger.setLevel(logging.INFO)
    
    # create the logging file handler
fh = logging.FileHandler("new_snake.log")
 
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
    # add handler to logger object
logger.addHandler(fh)
logger.info("Program started сгодня: "+str(tmp))       
while True: 
    l = 0
    my_thread = threading.Thread(target=two_sec, name='two', args=())
    my_thread.start()      
    try:    
        
        tmp = datetime.now()
        t1 = time.time()
        s7 = Siemens (ENGINE)
        t2 = time.time()
        print(" --  время связи с siemens : ",str(t2-t1)," ---")
        print ('ENGINE  - подключен')
        t1 = time.time()
        a[0] =  (s7.read_input (0, 8)) #  db8.DBD0
        t2 = time.time()
        print(t2-t1)
        a[1] =  (s7.read_input (1, 8))
		#print(a[0])
		#print(a[1])
        t=unpack('>H',pack('B',(a[0]))+pack('B',(a[1])))
        tt='{:0=+5d}'.format(t[0])
        print(' Декристализатор шоколад t : ',tt,' °C')
        #logger.info(" вес K1: " + str(tmp)+"  :"+ tt+"кг")   # +"  :"+ tt "= +"кг"
        buf = tt
        #print(buf)
        
        a[0] =  (s7.read_input (2, 8))
        a[1] =  (s7.read_input (3, 8))
        t=unpack('>H',pack('B',(a[0]))+pack('B',(a[1])))
        tt='{:0=+5d}'.format(t[0])
        buf = buf + '$' +tt
        #print (buf)
        print(' Декристализатор вода t    : ',tt,' °C')

        
        a[0] =  (s7.read_input (4, 8))
        a[1] =  (s7.read_input (5, 8))
        t=unpack('>H',pack('B',(a[0]))+pack('B',(a[1])))
        tt='{:0=+5d}'.format(t[0])
        buf = buf + '$' +tt
        #print (buf)
        print(' Декристализатор задание t : ',tt,' °C')
		
        
        a[0] =  (s7.read_input (6, 8))
        a[1] =  (s7.read_input (7, 8))
        t=unpack('>H',pack('B',(a[0]))+pack('B',(a[1])))
        tt='{:0=+5d}'.format(t[0])
        buf = buf +'$'+tt
        #print (buf)
        print(' Декристализатор клапан %  : ',tt,' %')
        print(' ')
		#--------------------------------------------------------------
        a[0] =  (s7.read_input (8, 8))
        a[1] =  (s7.read_input (9, 8))
        t=unpack('>H',pack('B',(a[0]))+pack('B',(a[1])))
        tt='{:0=+5d}'.format(t[0])
        buf = buf +'$'+tt
        #print (buf)
        print(' Зона 1 шоколад t   : ',tt,' °C')
        a[0] =  (s7.read_input (10, 8))
        a[1] =  (s7.read_input (11, 8))
        t=unpack('>H',pack('B',(a[0]))+pack('B',(a[1])))
        tt='{:0=+5d}'.format(t[0])
        buf = buf +'$'+tt
        #print (buf)
        print(' Зона 1 вода t      : ',tt,' °C')                   #   DB31.DBW42 = piw288

        
       
        a[0] =  (s7.read_input (12, 8))
        a[1] =  (s7.read_input (13, 8))
        #print(a[0])
        #print(a[1])
        t=unpack('>h',pack('B',(a[0]))+pack('B',(a[1])))
        tt='{:0=+5d}'.format(t[0])
        buf = buf +'$'+tt
        #print (buf)
        print(' Зона 1 задание t   : ',tt,' °C')
        
        a[0] =  (s7.read_input (14, 8))
        a[1] =  (s7.read_input (15, 8))
        t=unpack('>h',pack('B',(a[0]))+pack('B',(a[1])))
        tt='{:0=+5d}'.format(t[0])
        buf = buf +'$'+tt
        #print (buf)
        print(' Зона 1 клапан      : ',tt,' %')
		#---------------------------------------------------
        a[0] =  (s7.read_input (16, 8))
        a[1] =  (s7.read_input (17, 8))
        t=unpack('>H',pack('B',(a[0]))+pack('B',(a[1])))
        tt='{:0=+5d}'.format(t[0])
        buf = buf +'$'+tt
        print(' ')		
        #print (buf)
        print(' Зона 2 шоколад t   : ',tt,' °C')
		
        a[0] =  (s7.read_input (18, 8))
        a[1] =  (s7.read_input (19, 8))
        t=unpack('>H',pack('B',(a[0]))+pack('B',(a[1])))
        tt='{:0=+5d}'.format(t[0])
        buf = buf +'$'+tt
        #print (buf)
        print(' Зона 2 вода t      : ',tt,' °C')                   #   DB31.DBW42 = piw288
        #print(' ')
        
       
        a[0] =  (s7.read_input (20, 8))
        a[1] =  (s7.read_input (21, 8))
        #print(a[0])
        #print(a[1])
        t=unpack('>h',pack('B',(a[0]))+pack('B',(a[1])))
        tt='{:0=+5d}'.format(t[0])
        buf = buf +'$'+tt
        #print (buf)
        print(' Зона 2 задание t   : ',tt,' °C')
        
        a[0] =  (s7.read_input (22, 8))
        a[1] =  (s7.read_input (23, 8))
        t=unpack('>h',pack('B',(a[0]))+pack('B',(a[1])))
        tt='{:0=+5d}'.format(t[0])
        buf = buf +'$'+tt
        #print (buf)
		
		
		
        print(' Зона 2 клапан      : ',tt,' %')
        print(' ')
		#----------------------------------------------
		
        a[0] =  (s7.read_input (24, 8))
        a[1] =  (s7.read_input (25, 8))
        t=unpack('>H',pack('B',(a[0]))+pack('B',(a[1])))
        tt='{:0=+5d}'.format(t[0])
        buf = buf +'$'+tt
        print(' ')		
        #print (buf)
        print(' Зона  выход шоколад t   : ',tt,' °C')
		
        a[0] =  (s7.read_input (26, 8))
        a[1] =  (s7.read_input (27, 8))
        t=unpack('>H',pack('B',(a[0]))+pack('B',(a[1])))
        tt='{:0=+5d}'.format(t[0])
        buf = buf +'$'+tt
        #print (buf)
        print(' Зона  выход вода t      : ',tt,' °C')                   #   DB31.DBW42 = piw288
        #print(' ')
        
       
        a[0] =  (s7.read_input (28, 8))
        a[1] =  (s7.read_input (29, 8))
        #print(a[0])
        #print(a[1])
        t=unpack('>h',pack('B',(a[0]))+pack('B',(a[1])))
        tt='{:0=+5d}'.format(t[0])
        buf = buf +'$'+tt
        #print (buf)
        print(' Зона  выход задание t   : ',tt,' °C')
        
        a[0] =  (s7.read_input (30, 8))
        a[1] =  (s7.read_input (31, 8))
        t=unpack('>h',pack('B',(a[0]))+pack('B',(a[1])))
        tt='{:0=+5d}'.format(t[0])
        buf = buf +'$'+tt+'$+0002'
        #print (buf)
		
		
		
        print(' Зона  выход клапан      : ',tt,' %')
        print(' ')
        t3 = time.time()
        print(' ПАКЕТ  : ',(t3-t1))      
        '''
            engine 2 : 192.168.1.11
            
            
            Декристализатор	шоколад t	    db8.DBD0
            Декристализатор вода t		    db8.DBD2
            Декристализатор задание t		db8.DBD4
            Декристализатор клапан %		db8.DBD6

            Зона 1 шоколад t				db8.DBD8
            Зона 1 вода t					db8.DBD10
            Зона 1 задание t				db8.DBD12
            Зона 1 клапан %				    db8.DBD14

            Зона 2 шоколад t				db8.DBD16
            Зона 2 вода t					db8.DBD18
            Зона 2 задание t				db8.DBD20
            Зона 2 клапан %				    db8.DBD22

            Зона выход шоколад t			db8.DBD24
            Зона выход вода t				db8.DBD26
            Зона выход задание t			db8.DBD28
            Зона выход клапан %			    db8.DBD30   
            

      


        '''
        s7.close()
            #payload ={'key1':(t_qt_+'$+0000'+'$'+t_qqt_+'$'+t_t_+'$'+tt_t_+'$'+ttt_t_+'$'+tttt_t_+'$01')}
            #payload #={'key1':('-0123$-0124$+0125$+0126$-0127$-0223$-0224$+0225$+0226$-0227$-0323')}payload
        payload={'key1':(buf)}
            #logger.info(" вес K1: " + str(tmp)+"  :"+ buf)  
			#print(t_qt_+'$+0000'+'$'+t_qqt_+'$'+t_t_+'$'+tt_t_+'$'+ttt_t_+'$'+tttt_t_+'$01')
        t1 = time.time()
        r = requests.get('http://10.3.2.19/exempl92.php',params=payload)   
        t2 = time.time()
        print(" --  время связи с сервером : ",(t2-t1)," ---")
    except:
        print ('Нет подключения  ENGINE 2 ')
        t2 = time.time()
        logger.info(" **  П О Т Е Р Я   С В Я З И  ENGINE 2    :"  + str(tmp)+ "----"+ str(t2-t1)) 
        print(" **  П О Т Е Р Я   С В Я З И  ENGINE 2    :"  + str(tmp)+ "----"+ str(t2-t1))
    
    
    #time.sleep(5)
    while l == 0:
            continue
    print (" after 5sek :",(datetime.now()).ctime())  