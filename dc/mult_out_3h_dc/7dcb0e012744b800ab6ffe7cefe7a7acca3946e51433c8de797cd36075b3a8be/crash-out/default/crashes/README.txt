Command line used to find this crash:

/home/asmita/AFLpluplus_arm_exec/afl-fuzz -Q -i ../in_dir/ -o ../mult_out_3h_dc/7dcb0e012744b800ab6ffe7cefe7a7acca3946e51433c8de797cd36075b3a8be/crash-out -- ../mult_out_3h_dc/7dcb0e012744b800ab6ffe7cefe7a7acca3946e51433c8de797cd36075b3a8be/busybox dc

If you can't reproduce a bug outside of afl-fuzz, be sure to set the same
memory limit. The limit used for this fuzzing session was 0 B.

Need a tool to minimize test cases before investigating the crashes or sending
them to a vendor? Check out the afl-tmin that comes with the fuzzer!

Found any cool bugs in open-source tools using afl-fuzz? If yes, please post
to https://github.com/AFLplusplus/AFLplusplus/issues/286 once the issues
 are fixed :)

