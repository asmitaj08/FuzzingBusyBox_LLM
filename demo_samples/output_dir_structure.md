- output_dir
    - json_dumps *(Directory to store the fuzzing stat output of each of the target provided in the input_collection dir)*
    - failed_target.txt *(List of input target filename that failed while execution)*
    - multiple dir with same names as the input_targte name *(The number of these dir will be same as the number of input taregt files)*
        - busybox file (it's the input target file, just renamed as busybox)
        - Default output dir which is the output of afl-fuzz. It has crash, queues,stat and other outpusts from the fuzzer. 

    ** N.B : Try to do fuzzing in a different directory as you might se some random data poulated from `awk` script being fuzzed.