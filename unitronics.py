#***************************************************************************************************
'''
АВК ОМА Козырев С.А

новая версия Unitronics

24.07.19(старт)  воспоминания
26.07.19 запустил Unitronics
29.07.19 работа с многопоточностью
30.07.19 разбор принятой строки и подсчет контрольной суммы
         начало формирования запроса на сервер
31.07.19 рабочий вариант         

'''
import serial, time
from struct import *
from idlelib.multicall import r
import time
from datetime import datetime, date, timedelta   # import time
import threading
import requests
import logging

 #--------------------------------------------------------------
 # строка обращения к Unitronics
 # "D:\моя машина\unitronics\Unitronics PCOM Protocol.pdf"
 #
 #
 #--------------------------------------------------------------
 
 #-------------------------
 #
 # aeyrwbz dslth;rb 5 ctr
 #
 #-------------------------
 
 
 
def two_sec ():
    global l
    time.sleep(5)
    l = 1 
    
#-------------------------------------
#
#  функция подсчета контрольной суммы
#
#------------------------------------

def my_crc():
 
    crc = 0
    i = 1
    while i < 12:
        crc += cmd2[i]
                                            #print ('crc:'+hex(crc)+' i:'+str(i)+' cmd[i]:'+hex(cmd2[i]))
        i += 1
        
                                            #print ('crc:'+hex(crc))    
                                            #print (hex(crc))   
    if crc > 256:
        cr = crc % 256
                                            #print (cr)    
    
    return cr    
 
ByteStringToSend = "\x2f\x34\x36\x52\x4e\x4c\x30\x30\x30\x30\x30\x35\x37\x42\0d"
nu = '/46RNL0000057b\0x0d\0x0a'
cmd = 'b\x2f\x34\x36\x52\x4e\x4c\x30\x30\x30\x30\x30\x35\x37\x42\0d\x00'
cmd2 = bytearray(b'/46RNL00001500\x0d')
buffer = []
#ser = serial.Serial('COM8', 19200 ,parity=serial.PARITY_ODD,    stopbits=serial.STOPBITS_TWO,    bytesize=serial.SEVENBITS)

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





ser = serial.Serial(
    port = 'COM8',\
    baudrate=19200,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
    timeout=0)
ser.close()
ser.open()
while 1: 
    l = 0
    legza = 70
    legza2 = hex(legza)
    #print (legza2)
    cmd2[1] = ord(legza2[2].upper() )
    cmd2[2] = ord(legza2[3].upper() )
    
    
    crc = hex(my_crc())
                                                        #print (hex((crc)))
                                                        #print (type(hex((crc))))
                                                        #print (len(hex((crc))))
                                        #print (cmd2)
                                        #print ((crc.encode("utf-8")   ))
                                        #print (type(crc.encode("utf-8")   ))
    cmd2[12] = ord(crc[2].upper() )
    cmd2[13] = ord(crc[3].upper() )
                                                        #cmd2[14] = crc[3].encode("utf-8") 
                                                        #print (cmd2)
    my_thread = threading.Thread(target=two_sec, name='two', args=())
    my_thread.start()  


    
    ser.write((cmd2))
    t1 = time.time()                                                    #ser.write(str.encode(cmd))
    #print (cmd2)
    count = 0
    c = b"\0"
                        # Читаем ответ Unitronics
    while count < 1:
        c = b"\0"
        if ser.inWaiting():
            while True:
                val = ser.read(1)
                                                        #print (val)
                if b"\r" in val:
                    break
                else:
                    c = c+val
                    #print (c)
            buffer.append(c) # stores all data received into a list   
                                                                #print(buffer)
            count += 1
                                                                #print (count)
                                                                #print (buffer)
    
   
    t2 = time.time()
    print(" --  время связи с Unitronics : ",str(t2-t1)," ---")                                                            
    fac = buffer[0]
                                                                #print (fac)
                                                                #print (type(fac))
        #    достали первую температуру продукта
    fac2 = (fac[31:39])
                                                                #print (fac2)
    t = int(fac2, 16)
    tt='{:0=4d}'.format(t)
    buf = "=" + legza2[2].upper()+legza2[3].upper() 
    print(' Температура продукта  : ',tt,' °C')
                                                                #print (qttt)
    
        #    достали вторую температуру рубашки
    fac2 = (fac[40:47])
                                                                #print (fac2)
    t = int(fac2, 16)
    ttt='{:0=4d}'.format(t)
    print(' Температура рубашки   : ',ttt,' °C')
    #buf = buf + '$' +ttt
                                                                #print (qttt) 
    
    # достали вес
    fac2 = (fac[7:15])
                                                                #print (fac2)
    t = int(fac2, 16)
    qt='{:0=+6d}'.format(t)
    print(' Вес емкости           :',qt,' кг')
    buf = buf + '$' + qt+ "$" +ttt+ '$' +tt
    #print (buf)
    payload={'name':(buf)}
            #logger.info(" вес K1: " + str(tmp)+"  :"+ buf)  
			#print(t_qt_+'$+0000'+'$'+t_qqt_+'$'+t_t_+'$'+tt_t_+'$'+ttt_t_+'$'+tttt_t_+'$01')
    t1 = time.time()
    r = requests.get('http://10.3.2.19/Connect/Unitronics2.php',params=payload)   
    t2 = time.time()
    print(" --  время связи с сервером : ",(t2-t1)," ---")
                                                                #print (qttt) 
    
   
                                                                #print (fac2)
    buffer.clear()
                                                                #time.sleep(2))
    while l == 0:
            continue
    print (" after 5sek :",(datetime.now()).ctime())  
ser.close()

