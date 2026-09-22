# -*- coding: utf-8 -*-
import time, datetime, os, subprocess, logging, sys

# v0.47 20130219 fqd463 - added additional logging in .csv format to track attach network times, deleted additional wait times, cleaned up 

# Test requirements----------------------------------------------------------------
# initial conditions: wifi off, airplane mode off, 4G/3G coverage.  Also, disable automatic network time sync.

#configuration items
logging_loops = 10
verbose = 1          # 0 for basic pass & failure info, 1 for more info, 2 for even more detailed info...
pwr_up_sleep = 60    # time to wait post-boot; *adjust per product*
max_cnt = 100          # number of loops to run
loop_delay = 2       # wait time between measurments within loop
attach_timeout = 180 # time to exit each loop if no success
stop_on_fail = 0     # change to 1 to pause on a failure
stop_at_complete = 1 # if running outside of console, 1 to keep window open at completion
LTE_adb = 0          # set to 1 if LTE adb is available (wrigley devices)
debug_qc = 0         # set to 1 to enable additional (device) logging

fail_mode = "Unexpected Fail Mode"
network_attach_time_min = 9999
network_attach_time_avg = 9999
network_attach_time_max = 0

debug = None
t = datetime.datetime.now()

try:
    uut_sn = sys.argv[1]  # serial no of device; passed via command line.
    print "Device is " + uut_sn
except:
    print "Serial number is required.  Please enter as 'python scriptName serial_number' and restart"
    time.sleep(1)
    sys.exit()    

log_dir = 'PU_Attach_'+t.strftime("%m_%d_%H%M")
os.mkdir(log_dir)
os.chdir(os.getcwd()+'\\'+ log_dir)
#log.info("PWD "+os.getcwd())
os.system('adb shell rm -r /data/aplogd/*')
os.system('adb shell rm -r /data/diag_mdlog/logs/*')
os.system('adb shell rm -r /data/ss-ram-dumps/*')
os.system('adb shell rm -r /sdcard/bug2go/*')

adb_str = "adb -s " + uut_sn
log_file = 'PUAttach' + '_' + uut_sn + '_' + t.strftime("%Y%m%d%H%M%S") + '.log'
hist_file = 'PUAttach' + '_' + uut_sn + '_' + t.strftime("%Y%m%d%H%M%S") + '.csv'

 #logging stuff
log = logging.getLogger()
ch  = logging.StreamHandler()

#ensure_dir(log_file)
fh = logging.FileHandler(log_file)
fh2 = open(hist_file, 'w+')

log.addHandler(ch)
log.addHandler(fh)

ch_fmt = logging.Formatter("\t%(message)s")
fh_fmt = logging.Formatter("%(asctime)s \t: %(message)s")
ch.setFormatter(ch_fmt)
fh.setFormatter(fh_fmt)

if debug:
  log.setLevel(logging.DEBUG)
else:
  log.setLevel(logging.INFO)

i = 1
numfailed = 0
numpassed = 0
lte_cnt = 0
nr5g_cnt = 0
eHRPD_cnt = 0
HSPA_cnt = 0
EDGE_cnt = 0
UMTS_cnt = 0
onex_cnt = 0
test_start_time = datetime.datetime.now()

log.info("Power-up Attach test v0.47 -----------------------------------")
log.info("Start time: " + str(datetime.datetime.now()))
log.info("product is " + (os.popen(adb_str + ' shell getprop ro.product.name').readlines())[0])
log.info("SN is " + (os.popen(adb_str +' shell getprop ro.serialno').readlines())[0])
log.info("BL is " + (os.popen(adb_str +' shell getprop ro.bootloader').readlines())[0])
log.info("Build is " + (os.popen(adb_str +' shell getprop ro.build.fingerprint').readlines())[0])
log.info("BP is " + (os.popen(adb_str +' shell getprop gsm.version.baseband').readlines())[0])
fh2.write("Loop " + ", " + "Time(sec)" + "\n")


while i < max_cnt+1:
        print " "
        log.info("Starting loop " + str(i) + " of " + str(max_cnt) + " at " + (os.popen(adb_str +' shell date').readlines())[0])        
        #print "device time is " + (os.popen(adb_str +' shell date').readlines())[0]
        ntype_stat = 1  #0<>LTE 1=LTE
        if not LTE_adb:
            lping_stat = 0
            lping = "n/a"
        else:    
            lping_stat = 1  #0=attached 1=unreachable
        nping_stat = 1  #0=attached 1=unreachable
        log.info("Rebooting device and waiting ")
        os.system(adb_str + ' reboot')
        start_loop_timer = time.time()
        time.sleep(2)
        os.system(adb_str + ' kill-server')  
        time.sleep(2)		
        os.system(adb_str + ' wait-for-device')
        time.sleep(1)		
        os.system(adb_str + ' shell "echo TEST: device has been rebooted on loop ' + str(i) + ' at $(date) > /dev/kmsg"')
        if debug_qc:    
            os.system(adb_str + ' remount')
            time.sleep(3)
            os.system(adb_str + ' shell "echo Y > /sys/module/qcusbnet2k/parameters/qcusbnet_debug"')
            log.info("enabled qcusbnet debugging")

        network_attach_timer = time.time() - start_loop_timer
        log.info("Ping start at : " + str(network_attach_timer))        
        while (ntype_stat | lping_stat | nping_stat) & (network_attach_timer < attach_timeout):
                #search for LTE in getprop gsm.network.type
                f2=os.popen(adb_str + ' shell getprop gsm.network.type')
                if verbose > 1: logging.info(f2)
                f2lineList=f2.readlines(1)
                for k in f2lineList:
                    if verbose > 1: logging.info(k)
                    # 优先判断5G NR
                    if k.find('NR') != -1 or k.find('5G') != -1:
                        ntype_stat = 0
                        ntype = "5G_NR"
                    elif k.find('LTE') != -1:
                        ntype_stat = 0
                        ntype = "LTE"
                    elif k.find('eHRPD') != -1:
                        ntype_stat = 0
                        ntype = "eHRPD"
                    elif k.find('HSPA') != -1:
                        ntype_stat = 0
                        ntype = "HSPA"
                    elif k.find('EDGE') != -1:
                        ntype_stat = 0
                        ntype = "EDGE"
                    elif k.find('UMTS') != -1:
                        ntype_stat = 0
                        ntype = "UMTS"
                    elif k.find('1xRTT') != -1:
                        ntype_stat = 0
                        ntype = "1xRTT"
                    else:
                        ntype_stat = 1
                        ntype = "not attached"
                #ping LTE modem
                if LTE_adb:
                    f3=os.popen(adb_str + ' shell ping -s 512 -c 1 192.168.20.2')
                    if verbose > 1: logging.info(f3)
                    f3lineList = f3.readlines()                       
                    for k in f3lineList:
                        if k.find('unreachable') != -1:
                                lping_stat = 1
                                lping = "LTE modem ping failed"
                        else:
                                lping_stat = 0
                                lping = "LTE modem ping successful"
                #ping outside network                                             
                f4=os.popen(adb_str + ' shell ping -s 512 -c 1 67.208.64.240')
                if verbose > 1: logging.info(f4)
                f4lineList = f4.readlines()                       
                for k in f4lineList:
                        if k.find('unreachable') != -1:
                                nping_stat = 1
                                nping = "Network ping failed"
                        elif '100% packet loss' in k:
                                nping_stat = 1
                                nping = "Network ping returned no packets"
                        else:
                                nping_stat = 0
                                nping = "Network ping successful"            
                network_attach_timer = time.time() - start_loop_timer
                time.sleep(loop_delay)

        if (ntype_stat | lping_stat | nping_stat):
                fail_mode = "FAIL: Not connected to network"
                log.info(">< >< >< >< " + fail_mode + " after " + str(network_attach_timer) + " seconds. >< >< >< ><")
                log.info(ntype + ", " + lping + ", and " + nping)
                os.system(adb_str + ' shell "echo TEST: failed loop ' + str(i) + ' at $(date) > /dev/kmsg"')
                os.system(adb_str + ' kill-server')  
                time.sleep(2)		
                os.system(adb_str + ' devices')		
                time.sleep(5)				
                if verbose > 0: logging.info("network attach time MIN/AVG/MAX " + str(round(network_attach_time_min,1)) + "/" + str(round(network_attach_time_avg,1)) + "/" + str(round(network_attach_time_max,1)))
                numfailed=numfailed+1
                if stop_on_fail: raw_input('Press Enter to continue...')
        else:
                if verbose > 1: print ntype + ", " + lping + ", and " + nping
                log.info("Connected to " + str(ntype) + " network in " + str(round(network_attach_timer,1)) + " seconds.")
                fh2.write("Loop " + str(i) + ", " +  str(round(network_attach_timer,1)) + "\n")
                if ntype == "5G_NR": nr5g_cnt = nr5g_cnt + 1
                if ntype == "LTE": lte_cnt = lte_cnt+1
                if ntype == "eHRPD": eHRPD_cnt = eHRPD_cnt+1
                if ntype == "HSPA": HSPA_cnt = HSPA_cnt+1
                if ntype == "EDGE": EDGE_cnt = EDGE_cnt+1
                if ntype == "UMTS": UMTS_cnt = UMTS_cnt+1
                if ntype == "1xRTT": onex_cnt = onex_cnt+1				
                numpassed=numpassed+1
                if numpassed == 1:
                    network_attach_time_avg = network_attach_timer
                else:  
                    network_attach_time_avg = ((network_attach_time_avg * (numpassed-1)) + network_attach_timer)/ numpassed
                if network_attach_timer < network_attach_time_min: network_attach_time_min = network_attach_timer
                if network_attach_timer > network_attach_time_max: network_attach_time_max = network_attach_timer
                if verbose > 0: logging.info("network attach time MIN/AVG/MAX " + str(round(network_attach_time_min,1)) + "/" + str(round(network_attach_time_avg,1)) + "/" + str(round(network_attach_time_max,1)))
                os.system(adb_str + ' kill-server')  
                time.sleep(2)		
                os.system(adb_str + ' devices')		
                time.sleep(5)				

        
        elapsed_time = str(datetime.datetime.now() - test_start_time)        
        log.info("--------------------------------------------------------------------------------")
        log.info("ElapsedTestTime: " + elapsed_time + " | Pass: " + str(numpassed) + " | Fail: " + str(numfailed) + " | 5G: " + str(nr5g_cnt) + " | LTE: " + str(lte_cnt) + " | eHRPD: " + str(eHRPD_cnt) + " | HSPA: " + str(HSPA_cnt) + " | EDGE: " + str(EDGE_cnt) + " | UMTS: " + str(UMTS_cnt) + " | 1xRTT: " + str(onex_cnt))
        log.info("--------------------------------------------------------------------------------")
        if i%logging_loops == 0:
            log_dir = 'logs_loop_'+str(i-logging_loops)+'_'+str(i)
            os.mkdir(log_dir)
            os.system('adb pull /data/aplogd/ '+log_dir+'/data')
            os.system('adb pull /data/diag_mdlog/logs/ '+log_dir+'/bp')
            os.system('adb pull /data/ss-ram-dumps/ '+log_dir+'/bp_dump')
            os.system('adb pull /sdcard/bug2go/ '+log_dir+'/bug2go')
            os.system('adb shell dumpsys dropbox > '+log_dir+'\\dropbox.log')
            os.system('adb shell rm -r /data/aplogd/*')
            os.system('adb shell rm -r /data/diag_mdlog/logs/*')
            os.system('adb shell rm -r /data/ss-ram-dumps/*')
        i=i+1
fh2.close()                                        
log.info(" Test Complete ")
log.info("###################################################")
if stop_at_complete == 1: raw_input('Press Enter to continue...')
# finis
                                
