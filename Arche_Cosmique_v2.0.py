#!/usr/bin/python

import os
import serial
import thread
import time
import sys
import datetime

def asIntArray (s):
    return [ord(c) for c in s]

if __name__ == "__main__":
#vanaf hier schrijven we data naar de kosmische boog
    device = serial.Serial ("/dev/ttyUSB0")  # device zit aangesloten op ttyUSB0
    device.write ("\x99\x20\x0b\x66")        # Stuurt het startbit
    print 'Set threshold 1'
    device.write ("\x99\x16\x05\x66")        # Hier stelt u threshold 1 in
    print 'Set threshold 2'
    device.write ("\x99\x17\x05\x66")        # Hier stelt u threshold 2 in
    device.write ("\x99\x80\x00\x66")        # Hit pattern
    device.write ("\x99\x81\x00\x66")        # Histogram most left
    device.write ("\x99\x82\x00\x66")        
    device.write ("\x99\x83\x00\x66")        
    device.write ("\x99\x84\x00\x66")        
    device.write ("\x99\x85\x00\x66")        
    device.write ("\x99\x86\x00\x66")        
    device.write ("\x99\x87\x00\x66")        # Histogram most right

#tot hier schrijven we data naar de kosmische boog
#vanaf hier difineren we array's

    delta_time1_cnt = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    delta_time2_cnt = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    output_cnt = [0,0,0,0,0,0,0]
    display = [0,0,0,0,0,0,0]
    display_hit = [0,0,0,0,0,0,0]
    total_hit_cnt = [0]
    unfilterd_hit_cnt = [0]
    hit_pattern = [0,0,0,0,0,0,0]
    overflow = 0
    display_wr = [0,0,0,0,0,0,0]
    data = ''


#Tot hier difineren we array's
#Vanaf hier lezen we data uit
    print ("Start collecting data...")
    def input_thread(Stop):
        raw_input()
        Stop.append(None)

    def do_DAQ():
        Stop = []
        thread.start_new_thread(input_thread, (Stop,))
        while 1:
            time.sleep(.5)
            if Stop: break   

            temp = asIntArray (device.read(1))
            if temp == [153]:
                temp = asIntArray (device.read(1))
                if temp == [170]:
                    delta_time1temp = asIntArray (device.read(1))
                    print ("Delta time 1 temp:")
                    print delta_time1temp
                    delta_time2temp = asIntArray (device.read(1))
                    print ("Delta time 2 temp:")
                    print delta_time2temp, ("\n")
                    temp = asIntArray (device.read(1))
                    if temp == [102]: 
                        unfilterd_hit_cnt[0] = unfilterd_hit_cnt[0] + 1
                
                        delta_time1 = int(str (delta_time1temp).strip('[]'))
                        delta_time2 = int(str (delta_time2temp).strip('[]'))
                        
                        if delta_time1 <50:
                            delta_time1_cnt[delta_time1] = delta_time1_cnt[delta_time1] + 1
                        if delta_time2 <50:
                            delta_time2_cnt[delta_time2] = delta_time2_cnt[delta_time2] + 1
#Tot hier lezen we data uit
#Vanaf hier zit het filter

                        Range = [1,1,2,3,2,1,1]
                        mean1 = 29
                        mean2 = 13
                        hit = 0
                        hit_pattern = [0,0,0,0,0,0,0]
                        max_count = 4000
                        Time_tmp = time.time()
                        Timestamp = datetime.datetime.fromtimestamp(Time_tmp).strftime('%Y-%m-%d %H:%M:%S')

                        if delta_time1 == (mean1-3) :
                            if ((delta_time2 <= (mean2+3)) and (delta_time2 >= ((mean2+3)-Range[0]))) :
                                output_cnt[0] = output_cnt [0] +1
                                total_hit_cnt[0] = total_hit_cnt[0] +1
                                hit = 1
                                hit_pattern[0] = 1
                                os.system ("omxplayer 1.mp3 &")
                                time.sleep (.5)
                        elif delta_time1 == (mean1-2) :
                            if ((delta_time2 <= ((mean2+2)+Range[1])) and (delta_time2 >= ((mean2+2)-Range[1]))) :
                                output_cnt[1] = output_cnt [1] +1
                                total_hit_cnt[0] = total_hit_cnt[0] +1
                                hit = 1
                                hit_pattern[1] = 1
                                os.system ("omxplayer 2.mp3 &")
                                time.sleep (.5)
                        elif delta_time1 == (mean1-1) :
                            if ((delta_time2 <= ((mean2+1)+Range[2])) and (delta_time2 >= ((mean2+1)-Range[2]))) :
                                output_cnt[2] = output_cnt [2] +1
                                total_hit_cnt[0] = total_hit_cnt[0] +1
                                hit = 1
                                hit_pattern[2] = 1
                                os.system ("omxplayer 3.mp3 &")
                                time.sleep (.5)
                        elif delta_time1 == (mean1) :
                            if ((delta_time2 <= ((mean2)+Range[3])) and (delta_time2 >= ((mean2)-Range[3]))) :
                                output_cnt[3] = output_cnt [3] +1
                                total_hit_cnt[0] = total_hit_cnt[0] +1
                                hit = 1
                                hit_pattern[3] = 1
                                os.system ("omxplayer 4.mp3 &")
                                time.sleep (.5)
                        elif delta_time1 == (mean1+1) :
                            if ((delta_time2 <= ((mean2-1)+Range[4])) and (delta_time2 >= ((mean2-1)-Range[4]))) :
                                output_cnt[4] = output_cnt [4] +1
                                total_hit_cnt[0] = total_hit_cnt[0] +1
                                hit = 1
                                hit_pattern[4] = 1
                                os.system ("omxplayer 5.mp3 &")
                                time.sleep (.5)
                        elif delta_time1 == (mean1+2) :
                            if ((delta_time2 <= ((mean2-2)+Range[5])) and (delta_time2 >= ((mean2-2)-Range[5]))) :
                                output_cnt[5] = output_cnt [5] +1
                                total_hit_cnt[0] = total_hit_cnt[0] +1
                                hit = 1
                                hit_pattern[5] = 1
                                os.system ("omxplayer 6.mp3 &")
                                time.sleep (.5)
                        elif delta_time1 == (mean1+3) :
                            if ((delta_time2 <= ((mean2-3)+Range[6])) and (delta_time2 >= ((mean2-3)))) :
                                output_cnt[6] = output_cnt [6] +1
                                total_hit_cnt[0] = total_hit_cnt[0] +1
                                hit = 1
                                hit_pattern[6] = 1
                                os.system ("omxplayer 7.mp3 &")
                                time.sleep (.5)
                        print   output_cnt

                        max_value = 0
                        overflow = 0

                        for i in range (7):
                            if int(str (output_cnt[i]).strip('[]')) > max_value:
                                max_value = int(str (output_cnt[i]).strip('[]'))
                            if int(str (output_cnt[i]).strip('[]')) == max_count:
                                overflow = 1

                        if overflow == 1:
                            f = open('output_overflow','a')
                            f.write( str(output_cnt) )
                            f.write(Timestamp)
                            f.write( "\n" )
                            f.close()
                            os.system ("omxplayer test.mp3 &")
			
                        if overflow == 1:
                            for i in range (7):
                                output_cnt[i] = 0

                        if hit == 1:
                            for i in range (7):
                                if max_value > 16:
                                    display[i] = int(round(int(str (output_cnt[i]).strip('[]')) * (16.00/max_value)))
                                else:
                                    display[i] = int(str (output_cnt[i]).strip('[]'))
                            
                            for i in range (7):
                                if hit_pattern[i] == 1:
                                    display_hit[i] = 0

                                else:
                                    display_hit[i] = display[i]

                            f = open('Time_stamp_data','a')#Schrijf de tijd en datum van een "goede" hit in een text bestand
                            f.write(str (display))
                            f.write(Timestamp)
                            f.write( "\n" )
                            f.close()

                            f = open('Complete_Time_stamp','a')#Schrijf de tijd en datum van elke hit in een text bestand
                            f.write(str (output_cnt))
                            f.write(Timestamp)
                            f.write( "\n" )
                            f.close()

                            f = open('output_display','a')
                            f.write(str (hit_pattern))
                            f.write( "\n" )
                            f.close()

                            if hit_pattern[0] == 1:
                                device.write ("\x99\x80\x01\x66")
                            if hit_pattern[1] == 1:
                                device.write ("\x99\x80\x02\x66")
                            if hit_pattern[2] == 1:
                                device.write ("\x99\x80\x03\x66")
                            if hit_pattern[3] == 1:
                                device.write ("\x99\x80\x04\x66")
                            if hit_pattern[4] == 1:
                                device.write ("\x99\x80\x05\x66")
                            if hit_pattern[5] == 1:
                                device.write ("\x99\x80\x06\x66")
                            if hit_pattern[6] == 1:
                                device.write ("\x99\x80\x07\x66")

                            time.sleep (.5)
                            f = open('output_display','a')
                            f.write(str (display_hit))
                            f.write( "\n" )
                            f.close()

                            device.write ("\x99\x81")
                            device.write (chr(display_hit[0]))
                            device.write ("\x66")
                            device.write ("\x99\x82")
                            device.write (chr(display_hit[1]))
                            device.write ("\x66")
                            device.write ("\x99\x83")
                            device.write (chr(display_hit[2]))
                            device.write ("\x66")
                            device.write ("\x99\x84")
                            device.write (chr(display_hit[3]))
                            device.write ("\x66")
                            device.write ("\x99\x85")
                            device.write (chr(display_hit[4]))
                            device.write ("\x66")
                            device.write ("\x99\x86")
                            device.write (chr(display_hit[5]))
                            device.write ("\x66")
                            device.write ("\x99\x87")
                            device.write (chr(display_hit[6]))
                            device.write ("\x66")

                            time.sleep (.5)
                            f = open('output_display','a')
                            f.write(str (display))
                            f.write( "\n" )
                            f.close()

                            device.write ("\x99\x81")
                            device.write (chr(display[0]))
                            device.write ("\x66")
                            device.write ("\x99\x82")
                            device.write (chr(display[1]))
                            device.write ("\x66")
                            device.write ("\x99\x83")
                            device.write (chr(display[2]))
                            device.write ("\x66")
                            device.write ("\x99\x84")
                            device.write (chr(display[3]))
                            device.write ("\x66")
                            device.write ("\x99\x85")
                            device.write (chr(display[4]))
                            device.write ("\x66")
                            device.write ("\x99\x86")
                            device.write (chr(display[5]))
                            device.write ("\x66")
                            device.write ("\x99\x87")
                            device.write (chr(display[6]))
                            device.write ("\x66")

                            time.sleep (.5)
                            f = open('output_display','a')
                            f.write(str (display_hit))
                            f.write( "\n" )
                            f.close()

                            device.write ("\x99\x81")
                            device.write (chr(display_hit[0]))
                            device.write ("\x66")
                            device.write ("\x99\x82")
                            device.write (chr(display_hit[1]))
                            device.write ("\x66")
                            device.write ("\x99\x83")
                            device.write (chr(display_hit[2]))
                            device.write ("\x66")
                            device.write ("\x99\x84")
                            device.write (chr(display_hit[3]))
                            device.write ("\x66")
                            device.write ("\x99\x85")
                            device.write (chr(display_hit[4]))
                            device.write ("\x66")
                            device.write ("\x99\x86")
                            device.write (chr(display_hit[5]))
                            device.write ("\x66")
                            device.write ("\x99\x87")
                            device.write (chr(display_hit[6]))
                            device.write ("\x66")

                            time.sleep (.5)
                            f = open('output_display','a')
                            f.write(str (display))
                            f.write( "\n" )
                            f.close()

                            device.write ("\x99\x81")
                            device.write (chr(display[0]))
                            device.write ("\x66")
                            device.write ("\x99\x82")
                            device.write (chr(display[1]))
                            device.write ("\x66")
                            device.write ("\x99\x83")
                            device.write (chr(display[2]))
                            device.write ("\x66")
                            device.write ("\x99\x84")
                            device.write (chr(display[3]))
                            device.write ("\x66")
                            device.write ("\x99\x85")
                            device.write (chr(display[4]))
                            device.write ("\x66")
                            device.write ("\x99\x86")
                            device.write (chr(display[5]))
                            device.write ("\x66")
                            device.write ("\x99\x87")
                            device.write (chr(display[6]))
                            device.write ("\x66")

                        print display, "\n"

                elif  temp == [85]:
                    for i in range (7):
                        output_cnt[i] = 0
                    device.write ("\x99\x81\x00\x66")        # Histogram most left
                    device.write ("\x99\x82\x00\x66")        
                    device.write ("\x99\x83\x00\x66")        
                    device.write ("\x99\x84\x00\x66")        
                    device.write ("\x99\x85\x00\x66")        
                    device.write ("\x99\x86\x00\x66")        
                    device.write ("\x99\x87\x00\x66")        # Histogram most right
                    print ("reset")


#Tot hier zit het filter

            else:
                print ("incorrect meetresultaat")

    do_DAQ()
    print ("End of data\n")

    print ("Data results:\n")    
    print ("Number of unfiltered hits:")
    print unfilterd_hit_cnt
    print ("Number of filtered hits:")
    print total_hit_cnt
    
#   Raw data:
    f = open('delta time 1','w')
    for i in range (50):
        f.write( str(delta_time1_cnt[i]) )
        f.write( "\n" )
    f.close()
    f = open('delta time 2','w')
    for i in range (50):
        f.write( str(delta_time2_cnt[i]) )
        f.write( "\n" )
    f.close()



