from afl_fuzz import *
from afl_stats import *
from run_busybox_target import *
import argparse
import shutil
import json

# Applet = 'awk'

def get_user_input() :
    parser = argparse.ArgumentParser(
        prog = 'Run fuzzer',
        description = 'Run fuzzing on a single target'
    )
    parser.add_argument("--input", dest='target_binary', help = 'Enter the path of the target binary that you wnat to fuzz', required=True)
    parser.add_argument("--arch",dest='target_architecture', help = 'Specify the architecture of the target binary', 
                            choices = ['x86_64', 'ARM_32'], required=True)
    parser.add_argument("--corpus",dest='input_corpus', help = 'Enter the path of input corpus', required=True)
    parser.add_argument("--output",dest='output_dir', help = 'Enter the path for output dir', required=True)
    parser.add_argument("--afl-path",dest='afl_dir_path', default='/usr/local/bin/', help = 'Enter the path of dir that contains afl-fuzz executables, if other than the default system path' )
    parser.add_argument("--run-time",dest='run_time', default='3600', help = 'Enter the run time in seconds for which you want to run AFL++' )
    parser.add_argument("--depend", dest='dependency_path', default="", help = 'Provide the path of dir containing the library dependencies if any')
    parser.add_argument("--envs", dest='env_list', default="", help = "Provide the list of env variables to be set. NB : provide in format (no space) 'ENV1=val1','ENV2=val2'")
    parser.add_argument("--flags", dest='additional_flags_list', default="", help = "Provide the list of additional flags like 'c=0','M=none' (no space): none if no value is assigned to that flag")
    
    args = parser.parse_args()
    return args



if __name__=='__main__' :
   args = get_user_input()
   target_binary =  args.target_binary
   target_architecure = args.target_architecture
   input_corpus_path = args.input_corpus
   output_dir = args.output_dir
   afl_fuzz_path = os.path.join(args.afl_dir_path, "afl-fuzz")
   run_time = int(args.run_time)
   dependency_path = args.dependency_path
   env_list = args.env_list
   additional_flags_list = args.additional_flags_list
   
   print(f'afl_fuzz_path provided : {afl_fuzz_path}')

   if not os.path.exists(output_dir):
       os.makedirs(output_dir)
   
   if not os.path.exists(afl_fuzz_path):
       print('Error afl-fuzz path: {afl_fuzz_path} not found')
       exit(1)
   
   if not os.path.exists(input_corpus_path):
       print('Error input_corpus: {input_corpus_path} not found')
       exit(1)
   
   if not os.path.exists(target_binary):
       print('Error target_binary: {target_binary} not found')
       exit(1)

   if dependency_path != "" : 
     print(f'Arm dependency file provided : {dependency_path}')
     if not os.path.exists(dependency_path) :
        print(f'Error: arm_dependencies_path not found !!')
        exit(1)
       
   # Rename target_binary as 'busybox' and Copy it in the output_dir
   busybox_path = os.path.join(output_dir, "busybox")
   shutil.copy(target_binary, busybox_path)
   print(f'The targeted busybox path is {busybox_path}')
   
   busybox_version = run_busybox_target(busybox_path, target_architecure, dependency_path)
   
   afl_fuzz_output_dir = os.path.join(output_dir, "crash-out")
   overall_dict = {'busybox_hash_name' : os.path.basename(target_binary), 'busybox_version' : busybox_version, 'stats' : {}}
   # Run afl-fuzz
   print(f'Running afl fuzz for target : {target_binary} and arch : {target_architecure} ')
   running_status = afl_fuzz_run(target_binary=busybox_path, input_corpus=input_corpus_path,arch=target_architecure, output_dir=afl_fuzz_output_dir,path_to_afl_fuzz=afl_fuzz_path, dependency=dependency_path, run_time=run_time, additional_flags=additional_flags_list, env_list=env_list)
  

   if running_status == 2:
       print("Reading fuzzing stats")
       ret_val , stats_dict = get_afl_fuzz_stats(afl_fuzz_output_dir, True)
    #    print(stats_dict)
       if ret_val == False:
           print("Cannot read fuzzer_stats file. Exiting!!")
           exit(1)
    #    print(stats_dict)
   else:
       print(running_status)
       print("Fuzzing failed unknown error")
       exit(1)

   overall_dict['stats'] = stats_dict
   print(overall_dict)
   with open(os.path.join(output_dir, "stats.json"), 'w') as outfile:
       json.dump(overall_dict, outfile)
   
   print("Dumped the fuzzer stats in stats.json file in dir : {output_dir}")
   print("Done")

  
