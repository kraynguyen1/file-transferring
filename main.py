  
#import needed dependencies
from genericpath import getmtime
import os
import fnmatch
import shutil
from pathlib import Path
import glob
import time
from datetime import datetime, timedelta
import psutil    
import smtplib, ssl
import signal,sys
import atexit

report_summary = []
# select files that have xml extensions
#assign source-destination folder path
from_folder_files = r"C:\Users\krayn\test-file-transfering\From\*"
source_folder = r"C:\Users\krayn\test-file-transfering\From"
to_folder = r"C:\Users\krayn\test-file-transfering\To4"

def transferFile():
    # define file patern
    pattern = "*txt*"

    files = glob.glob(os.path.expanduser(from_folder_files))
    sorted_by_mtime_ascending = sorted(files, key=lambda t: os.stat(t).st_mtime)

    count = 0
    global_time = 0
    report_list = []
    list = []
    # move file
    for file in sorted_by_mtime_ascending:
        # if filename match pattern
        if(fnmatch.fnmatch(file, pattern)):
            count +=1
            count_str = str(count)
            # extract full file name
            full_file_name = os.path.join(source_folder, file)
            if(count == 1):
                global_time = os.path.getmtime(full_file_name)
                if(os.path.isfile(full_file_name)):
                    print(full_file_name)
                    format_global_time = time.ctime(global_time)
                    obj_global = time.strptime(format_global_time)
                    date_format = "%Y-%m-%d %H:%M"
                    T_stamp_global = time.strftime(date_format, obj_global)
                    # report first item in batch
                    report_list.append('NEW BATCH!!!! Starting with file: ' + full_file_name + ' @ ' + T_stamp_global + '\n')
                    list.append(full_file_name)
                    
            else:
                thresh_hold = os.path.getmtime(full_file_name)
                format_global_time = time.ctime(global_time)
                format_threshold = time.ctime(thresh_hold)
                obj_global = time.strptime(format_global_time)
                obj_threshold = time.strptime(format_threshold)
                date_format = "%Y-%m-%d %H:%M"
                T_stamp_global = time.strftime(date_format, obj_global)
                T_stamp_threshold = time.strftime(date_format, obj_threshold)
                

                # convert to datetime object
                global_date_time = datetime.strptime(T_stamp_global, date_format).time()
                thresh_hold_date_time = datetime.strptime(T_stamp_threshold, date_format).time()
                t_global = timedelta(hours = global_date_time.hour, minutes=global_date_time.minute,seconds = global_date_time.second)
                t_threshold = timedelta(hours = thresh_hold_date_time.hour, minutes=thresh_hold_date_time.minute, seconds = thresh_hold_date_time.second)
                print("global time: " + T_stamp_global)
                print("threshold: " + T_stamp_threshold)
                duration = t_threshold - t_global
                print(duration)
                
                if(T_stamp_global == T_stamp_threshold or (duration <= timedelta(minutes=10) and duration > timedelta(minutes = 0))):
                    #print(global_time)
                    #print(thresh_hold)
                    #print("same modified date detected")
                    # if path contains the full filename, move the file from source to destination
                    if(os.path.isfile(full_file_name)):
                        print(full_file_name)
                        report_list.append(full_file_name + ' @ ' + T_stamp_threshold + '\n')
                        list.append(full_file_name)
                        
                else: 
                    break   
            
        
    
    
    for item in list:
        
        shutil.move(item, to_folder)

    return report_list

@atexit.register
def goodbye():
    print("program stopped")
    gmail_user = ''
    gmail_pw = ''
    #email properties
    sent_from = gmail_user
    to = ['']
    subject = 'FILE TRANSFERING PROGRAM STOPPED'
    email_text = "The program has been stopped by the authorizer. Here is the report log before stoppage: \n"
    for batch in report_summary:
        for file in batch:
            email_text += file 
        email_text += '\n-------------------------------------------------------------------------------------------\n'
    msg = 'Subject: {}\n\n{}'.format(subject, email_text)
    
    #email send request
    smtp_server = ''
    port = 587
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(gmail_user, gmail_pw)
            server.sendmail(sent_from, to, msg)
            server.close()

        print ('Email sent!')
    except Exception as e:
        print(e)
        print ('Something went wrong...')


try:
    while(True):
        source_f = os.listdir(source_folder)
        to_f = os.listdir(to_folder)

        len_source = len(source_f)
        len_dest = len(to_f)
        if(len_dest == 0):
            current_batch_summary = transferFile()
            #len_source-=len_deduct
            #len_dest+=len_deduct
            report_summary.append(current_batch_summary)
except SystemExit:
    print("System exit")
    print("program terminated")
    
except KeyboardInterrupt:
    print("keyboardinterrupt")
    print("program terminated")

except GeneratorExit:
    print("Generator exit")
    print("program terminated")

except Exception:
    print("Exception")
    print("program terminated")


    
# C:\Users\krayn\OneDrive\Documents\GitHub\File-transfering   

    
    
    


        
