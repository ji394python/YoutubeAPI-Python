
import os
import time
def errorLog(exe_status:str):
    '''Recording instance log'''
    log_path= 'log'
    if os.path.exists('log/ERROR.log'):
        os.remove('log/ERROR.log')
    if not os.path.exists(log_path):
        os.mkdir(log_path)   
        log_file = open(f'log/ERROR.log',mode='a',encoding='utf-8')
        record_time = time.strftime("%Y%m%d %H:%M:%S")
        log_file.write('Process:'+str(__file__)+'\n')
        log_file.write('Execute time:'+record_time+'\n')
        log_file.write('---------------------------------------'+'\n')
        log_file.write(record_time+"："+str(exe_status)+'\n')
    else:
        record_time = time.strftime("%Y%m%d %H:%M:%S")
        log_file = open(f'log/ERROR.log',mode='a',encoding='utf-8')
        log_file.write(record_time+"："+str(exe_status)+'\n')

'''
model_log(__file__,'Process start')
'''

def processLog(exe_string:str):
    log_path= 'log'
    if not os.path.exists(log_path):
        os.mkdir(log_path) 
        record_time = time.strftime("%Y%m%d %H:%M:%S")  
        log_file = open(f'log/Process.log',mode='a',encoding='utf-8')
        log_file.write('Process:'+str(__file__)+'\n')
        log_file.write('Execute time:'+record_time+'\n')
        log_file.write('---------------------------------------'+'\n')
        log_file.write(record_time+"："+str(exe_string)+'\n')
    else:
        record_time = time.strftime("%Y%m%d %H:%M:%S")
        log_file = open(f'log/Process.log',mode='a',encoding='utf-8')
        log_file.write(record_time+"："+str(exe_string)+'\n')

        