Command line used to find this crash:

/home/asmita/AFLpluplus_arm_exec/afl-fuzz -Q -i ../in_dir/ -o ../out_48_10f2_dc/crash-out -- ../out_48_10f2_dc/busybox dc

If you can't reproduce a bug outside of afl-fuzz, be sure to set the same
memory limit. The limit used for this fuzzing session was 0 B.

Need a tool to minimize test cases before investigating the crashes or sending
them to a vendor? Check out the afl-tmin that comes with the fuzzer!

Found any cool bugs in open-source tools using afl-fuzz? If yes, please post
to https://github.com/AFLplusplus/AFLplusplus/issues/286 once the issues
 are fixed :)

