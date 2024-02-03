import os
import subprocess
from afl_stats import *
import time
import signal
import shutil
import asyncio

# Currently it is for busybox awk applet fuzzing,
# change afl_fuzz_command in case of different applet

def afl_fuzz_run(target_binary : str,
                input_corpus : str,
                output_dir : str, 
                arch : str,
                path_to_afl_fuzz: str = 'afl-fuzz',
                run_time : int = 3600,
                dependency : str = "",
                additional_flags: list =None,
                env_list: list=None,
                hide_output: bool=False,) -> None:
   
    afl_fuzz_command = []
    
    if env_list != "":
         env_vars = env_list.split(",")
         print(f"env_list : {env_vars}")
         for env_var in env_vars :
            key, val = env_var.split("=")
            print(f'setting env var : {key} to {val}')
            os.environ[key] =  val
            print(f'Verifying if it was actually set. The set value is : {os.environ.get(key)}')
    
    
    afl_fuzz_command += [ 
            path_to_afl_fuzz,
            '-Q',
            '-i',
            input_corpus,
            '-o',
            output_dir,
          ]
    
    if additional_flags != "":
        flag_vars = additional_flags.split(",")
        print(f'Additional flags : {flag_vars}')
        for flag_var in flag_vars :
            keyf, valf = flag_var.split("=")
            print(f'Key : {keyf}, val : {valf}')
            if valf != 'none' :
                flag_val = '-' + keyf + ' ' + valf
                print(f'Flag : {flag_val}')
                afl_fuzz_command.append(flag_val)
            else :
                flag_val1 = '-' + keyf
                print(f'Flag1: {flag_val1}')
                afl_fuzz_command.append(flag_val1)
        

    afl_fuzz_command += [
        '--',
        target_binary,
        'man',
        '@@',
    ]
    
    # Check if the output directory already  exists
    if os.path.exists(output_dir):
        # Delete the directory
        subprocess.run(['rm',  '-rf' , output_dir])
        print(f'Directory {output_dir} deleted')

    print(f'Run time : {run_time}')
    print('Running command: ' + ' '.join(afl_fuzz_command))


    if dependency != "" :  # Not needed here as already done in run_target
         # Set the LD_LIBRARY_PATH environment variable.
        os.putenv('LD_LIBRARY_PATH', dependency)

    output_stream = subprocess.PIPE if hide_output else None
    try :
        afl_fuzz_run_process = subprocess.Popen(afl_fuzz_command, stdout=output_stream, stdin=output_stream)
        # fuzzing_result , fuzzing_err = afl_fuzz_run_process.communicate()
        # print(f'Fuzzing process error : {fuzzing_err}')
        # except subprocess.CalledProcessError as e:
        #     print(f"Fuzzing failed with exit code {e.returncode}")
        time.sleep(60)
        print("reading fuzz stat file \n")
        return_val , read_fuzz_stats_dict = get_afl_fuzz_stats(output_dir)
        print(f'Fuzzing stats return val : {return_val}')
        if return_val == False:
             print("Cannot read fuzzer_stats file in start. Exiting!!")
             exit(1)
            # print(f'Fuzzing stats: {read_fuzz_stats_dict}, return val : {return_val}')

        print(f'Fuzzing stats file exists. \n')
        # print(f'Fuzzing stats: {read_fuzz_stats_dict}, return val : {return_val}')
        print(f'Fuzzing stats return val : {return_val} \n')
        # Run afl-fuzz until given run_time
        # print((int(read_fuzz_stats_dict['cycles_done'])))
        while (int(read_fuzz_stats_dict['run_time'])) < run_time :
            return_val , read_fuzz_stats_dict = get_afl_fuzz_stats(output_dir)
            print(f"Run time: {read_fuzz_stats_dict['run_time']}")
            
            if (int(read_fuzz_stats_dict['run_time'])) >= run_time:
                print(f'{run_time} seconds completed.\n')
                # print(f"Killing the fuzzer pid : {int(read_fuzz_stats_dict['fuzzer_pid'])}")
                # os.kill(int(read_fuzz_stats_dict['fuzzer_pid']), signal.SIGINT)
                print("Terminating fuzzer process \n")
                afl_fuzz_run_process.terminate()
                return 2
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"KeyboardInterrupt")
        return 2
    
    except subprocess.CalledProcessError as e:
            print(f"Fuzzing failed for unknown reason. Error : \n {e.output}")
            return 1
        
