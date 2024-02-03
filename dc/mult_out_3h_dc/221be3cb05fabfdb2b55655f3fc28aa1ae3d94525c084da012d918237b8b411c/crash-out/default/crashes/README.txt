Command line used to find this crash:

/home/asmita/AFLpluplus_arm_exec/afl-fuzz -Q -i ../in_dir/ -o ../mult_out_3h_dc/221be3cb05fabfdb2b55655f3fc28aa1ae3d94525c084da012d918237b8b411c/crash-out -- ../mult_out_3h_dc/221be3cb05fabfdb2b55655f3fc28aa1ae3d94525c084da012d918237b8b411c/busybox dc

If you can't reproduce a bug outside of afl-fuzz, be sure to set the same
memory limit. The limit used for this fuzzing session was 0 B.

Need a tool to minimize test cases before investigating the crashes or sending
them to a vendor? Check out the afl-tmin that comes with the fuzzer!

Found any cool bugs in open-source tools using afl-fuzz? If yes, please post
to https://github.com/AFLplusplus/AFLplusplus/issues/286 once the issues
 are fixed :)

