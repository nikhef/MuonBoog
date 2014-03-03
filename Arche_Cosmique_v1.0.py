import os
import serial
import thread
import time

def asIntArray (s):
    return [ord(c) for c in s]

if __name__ == "__main__":
    device = serial.Serial ("/dev/ttyUSB0")  # device zit aangesloten op ttyUSB0
    device.write ("\x99\x20\x0b\x66")        # Stuurt het startbit
    print 'Set threshold 1'
    device.write ("\x99\x16\x05\x66")        # Hier stelt u threshold 1 in
    print 'Set threshold 2'
    device.write ("\x99\x17\x05\x66")        # Hier stelt u threshold 2 in

    delta_time1_cnt = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    delta_time2_cnt = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    output_cnt = [0,0,0,0,0,0,0]
    total_hit_cnt = [0]
    unfilterd_hit_cnt = [0]
#    overflow = 0

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
            print ("Startbit:")
            print temp
            if temp == [153]:
                temp = asIntArray (device.read(1))
                print ("Identifier:")
                print temp
                if temp == [170]:
                    delta_time1temp = asIntArray (device.read(1))
                    print ("Delta time 1 temp:")
                    print delta_time1temp
                    delta_time2temp = asIntArray (device.read(1))
                    print ("Delta time 2 temp:")
                    print delta_time2temp
                    temp = asIntArray (device.read(1))
                    temp = asIntArray (device.read(1))
                    if temp == [102]: 
                        print ("End of data string")
                        unfilterd_hit_cnt[0] = unfilterd_hit_cnt[0] + 1
                
                        delta_time1 = int(str (delta_time1temp).strip('[]'))
                        delta_time2 = int(str (delta_time2temp).strip('[]'))
                        
                        if delta_time1 <50:
                            print ("Delta time 1 is een geldige waarde")
                            delta_time1_cnt[delta_time1] = delta_time1_cnt[delta_time1] + 1
                        if delta_time2 <50:
                            print ("Delta time 2 is een geldige waarde\n")
                            delta_time2_cnt[delta_time2] = delta_time2_cnt[delta_time2] + 1
#Tot hier lezen we data uit
#Vanaf hier zit het filter

                        Range = [1,1,2,3,2,1,1]
                        mean1 = 35
                        mean2 = 17
        
                        if delta_time1 == (mean1-3) :
                            if ((delta_time2 <= (mean2+3)) and (delta_time2 >= ((mean2+3)-Range[0]))) :
                                output_cnt[0] = output_cnt [0] +1
                                total_hit_cnt[0] = total_hit_cnt[0] +1
                                print ("Hit!")
                                os.system ("omxplayer 1.mp3 &")
                                time.sleep (.5)
                        elif delta_time1 == (mean1-2) :
                            if ((delta_time2 <= ((mean2+2)+Range[1])) and (delta_time2 >= ((mean2+2)-Range[1]))) :
                                output_cnt[1] = output_cnt [1] +1
                                total_hit_cnt[0] = total_hit_cnt[0] +1
                                print ("Hit!")
                                os.system ("omxplayer 2.mp3 &")
                                time.sleep (.5)
                        elif delta_time1 == (mean1-1) :
                            if ((delta_time2 <= ((mean2+1)+Range[2])) and (delta_time2 >= ((mean2+1)-Range[2]))) :
                                output_cnt[2] = output_cnt [2] +1
                                total_hit_cnt[0] = total_hit_cnt[0] +1
                                print ("Hit!")
                                os.system ("omxplayer 3.mp3 &")
                                time.sleep (.5)
                        elif delta_time1 == (mean1) :
                            if ((delta_time2 <= ((mean2)+Range[3])) and (delta_time2 >= ((mean2)-Range[3]))) :
                                output_cnt[3] = output_cnt [3] +1
                                total_hit_cnt[0] = total_hit_cnt[0] +1
                                print ("Hit!")
                                os.system ("omxplayer 4.mp3 &")
                                time.sleep (.5)
                        elif delta_time1 == (mean1+1) :
                            if ((delta_time2 <= ((mean2-1)+Range[4])) and (delta_time2 >= ((mean2-1)-Range[4]))) :
                                output_cnt[4] = output_cnt [4] +1
                                total_hit_cnt[0] = total_hit_cnt[0] +1
                                print ("Hit!")
                                os.system ("omxplayer 5.mp3 &")
                                time.sleep (.5)
                        elif delta_time1 == (mean1+2) :
                            if ((delta_time2 <= ((mean2-2)+Range[5])) and (delta_time2 >= ((mean2-2)-Range[5]))) :
                                output_cnt[5] = output_cnt [5] +1
                                total_hit_cnt[0] = total_hit_cnt[0] +1
                                print ("Hit!")
                                os.system ("omxplayer 6.mp3 &")
                                time.sleep (.5)
                        elif delta_time1 == (mean1+3) :
                            if ((delta_time2 <= ((mean2-3)+Range[6])) and (delta_time2 >= ((mean2-3)))) :
                                output_cnt[6] = output_cnt [6] +1
                                total_hit_cnt[0] = total_hit_cnt[0] +1
                                print ("Hit!")
                                os.system ("omxplayer 7.mp3 &")
                                time.sleep (.5)
                                print ("Hit!")
                        print   output_cnt

                        overflow = 0
                        for i in range (7):
                            print i
                            if int(str (output_cnt[i]).strip('[]')) == 16:
                                overflow = 1
                            print ("overflow="),overflow,("\n")

                        if overflow == 1:
                            f = open('output_overflow','a')
                            f.write( str(output_cnt) )
                            f.write( "\n" )
                            f.close()
                            os.system ("omxplayer test.mp3 &")

                        for i in range (7):
                            if overflow == 1:
                                if output_cnt[i] == 17:
                                    output_cnt[i] = 1
                                else:
                                    output_cnt[i] = 0


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
    
#    print ("Delta time 1:")
#    print delta_time1_cnt    
#    print ("Delta time 2:")
#    print delta_time2_cnt    

#   Filtered data:
    f = open('output count','w')
    for i in range (7):
        f.write( str(output_cnt[i]) )
        f.write( "\n" )
    f.close()


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



