import os
import subprocess
import argparse
import shutil

def get_user_input() :
    parser = argparse.ArgumentParser(
        prog = 'Run fuzzer - multiple target',
        description = 'Run fuzzing on multiple target'
    )
    parser.add_argument("--input", dest='target_binary_collection_dir', help = 'Enter the path of the input dir that contains bunch of target binaries to be fuzzed', required=True)
    parser.add_argument("--arch",dest='target_architecture', help = 'Specify the architecture of the target binary', 
                            choices = ['x86_64', 'ARM_32'], required=True)
    parser.add_argument("--corpus",dest='input_corpus', help = 'Enter the path of input corpus', required=True)
    parser.add_argument("--output",dest='output_dir', help = 'Enter the path for output dir', required=True)
    parser.add_argument("--afl-path",dest='afl_dir_path', default='/usr/bin/', help = 'Enter the path of dir that contains afl-fuzz executables, if other than the default system path' )
    parser.add_argument("--run-time",dest='run_time', default='3600', help = 'Enter the run time in seconds for which you want to run AFL++' )
    parser.add_argument("--depend", dest='dependency_path', default="", help = 'Provide the path of dir containing the library dependencies if any')
    parser.add_argument("--envs", dest='env_list', default="", help = "Provide the list of env variables to be set. NB : provide in format (no space) 'ENV1=val1','ENV2=val2'")
    parser.add_argument("--flags", dest='additional_flags_list', default="", help = "Provide the list of additional flags like 'c=0','M=none' (no space): none if no value is assigned to that flag")
    
    
    args = parser.parse_args()
    return args



if __name__=='__main__' :
   args = get_user_input()
   target_binary_collection_dir =  args.target_binary_collection_dir
   target_architecure = args.target_architecture
   input_corpus_path = args.input_corpus
   output_dir = args.output_dir
   afl_dir_path = args.afl_dir_path
   run_time = args.run_time
   dependency_path = args.dependency_path
   env_list = args.env_list
   additional_flags_list = args.additional_flags_list
   

   if not os.path.exists(output_dir):
       os.makedirs(output_dir)
   
   if not os.path.exists(afl_dir_path):
       print('Error afl-fuzz path: {afl_dir_path} not found')
       exit(1)
   
   if not os.path.exists(input_corpus_path):
       print('Error input_corpus: {input_corpus_path} not found')
       exit(1)
   
   if not os.path.exists(target_binary_collection_dir):
       print('Error binary_collection: {target_binary_collection_dir} not found')
       exit(1)

   if dependency_path != "" :
     print(f'Arm dependency file provided : {dependency_path}')
     if not os.path.exists(dependency_path) :
        print(f'Error: arm_dependencies_path not found !!')
        exit(1)

    
       
   stats_json_dump_dir = os.path.join(output_dir, 'json_dumps')
   if not os.path.exists(stats_json_dump_dir):
       os.makedirs(stats_json_dump_dir)
   
   files = os.listdir(target_binary_collection_dir)
   print(f'No. of targets : {len(files)}')
#    processes = []
   failed_target_name_file = os.path.join(output_dir, 'failed_target.txt')
   for file in files:
        print(f'Target : {file}')
        target_output_dir = os.path.join(output_dir, file)
        print(f'Target output dir is : {target_output_dir}')
        target_run_command = [
            'python3',
            'fuzz_one_target_main.py',
            '--input',
            os.path.join(target_binary_collection_dir, file),
            '--arch',
            target_architecure,
            '--corpus',
            input_corpus_path,
            '--output',
            target_output_dir,
            '--afl-path',
            afl_dir_path,
            '--run-time',
            run_time,
            '--depend',
            dependency_path,
            '--envs',
            env_list,
            '--flags',
            additional_flags_list,
        ]
        print(type(target_run_command))
        process = subprocess.Popen(target_run_command)
        process.wait()
        print(f'Process return code : {process.returncode}')
        if process.returncode!= 0:
            print(f'Error in target : {file}')
            with open(failed_target_name_file, 'a') as f:
                f.write(f'{file}\n')
            f.close()

        else :
            json_filename = file + '.json'
            target_json_file = os.path.join(stats_json_dump_dir, json_filename)
            shutil.copy(os.path.join(target_output_dir, 'stats.json'), target_json_file)
            print(f'The stats json file for target : {file} is at : {target_json_file}')




#         processes.append(process)

#    for process in processes:
#        process.wait()
#        print(process.returncode)
#        if process.returncode!= 0:
#            print()