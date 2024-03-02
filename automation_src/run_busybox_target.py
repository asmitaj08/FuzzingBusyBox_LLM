import subprocess
import os

def run_busybox_target(busybox_path, arch, dependencies_path = ""):
    chmod_result = subprocess.run(['chmod',  '+x' , busybox_path])
    if chmod_result.returncode!= 0:
            print("Error: chmod failed")
            exit(1) 

    if dependencies_path != "" :
         # Set the LD_LIBRARY_PATH environment variable.
        os.putenv('LD_LIBRARY_PATH', dependencies_path)

    # qemu = 'qemu-arm' 
    if os.path.exists('/usr/bin/qemu-arm') or  os.path.exists('/usr/local/bin/qemu-arm'):
        qemu = 'qemu-arm' 
    elif os.path.exists('/usr/bin/qemu-arm-static') or os.path.exists('/usr/local/bin/qemu-arm-static'):
            qemu = 'qemu-arm-static'
    else:
            print("cannot find qemu-arm or qemu-arm-static")
            exit(1)

    if arch == 'x86_64' :
          busybox_process = subprocess.Popen([busybox_path], stdout=subprocess.PIPE)
          busybox_result , busybox_err = busybox_process.communicate()
          if busybox_err == None :
                print(busybox_result)
                busybox_version = busybox_result.decode().split(' ')[1]
                print(f'Busybox version : {busybox_version}')
                return busybox_version
          else :
                print(f'Error: busybox_run_err : {busybox_err}')
                exit(1)

    elif arch == 'ARM_32' :
        busybox_process = subprocess.Popen([qemu, busybox_path], stdout=subprocess.PIPE)
        busybox_result , busybox_err = busybox_process.communicate()
        if busybox_err == None :
            print(busybox_result)
            busybox_version = busybox_result.decode().split(' ')[1]
            print(f'Busybox version : {busybox_version}')
            return busybox_version
        else :
            print(f'Error: busybox_run_err : {busybox_err}')
            exit(1)       

    else :
          print(f'Error: busybox arch err : {arch} not supported')
          exit(1)

        
