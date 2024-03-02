# FuzzingBusyBox_LLM
We have performed fuzzing on BusyBox target extracted from firmware of real-world embedded products (Firmware database provided by [NetRise](https://www.netrise.io/)).
Apart from fuzzing using AFL++, we have leveraged LLM (Using OpenAI GPT-4) for initial input generation, followed by adding crash reuse technique to the pipline. 
This repo is for paper :  *"Fuzzing BusyBox: Leveraging LLM and Crash Reuse for Embedded Bug Unearthing", Usenix 2024*

* The automation script to perform fuzzing on a large batch of BusyBox target binaries using AFL++ is provided in *automation_src* folder. Note : *Currently it is for busybox awk applet fuzzing,
change `afl_fuzz_command`(afl_fuzz.py) in case of different applet*
* Target architecture : x86_64 and ARM_32
* Command :
`python3 fuzz_multiple_targets.py --input /path/to/binary/collection --arch ARM_32/x86_64 --corpus /path/to/corpus --output /path/for/output --afl-path path/of/afl  --run-time required_runtime --depend arm_dependecies_in_case_of_arm `
* `fuzz_multiple_targets.py` is the main script that takes in a bunch of collected BusyBox target binaries, perform fuzzing on each target using AFL++ till the runtime provided by the user. ANd after fuzzing is done, it stores the fuzzing stats (json) of all the target in the output directory.

## Dependencies
* For x86_64 based target, install [AFL++](https://github.com/AFLplusplus/AFLplusplus) in Qemu_mode
* For running arm based target on x86 machine, we need to build AFL++ in Qemu mode for ARM arch, and fix arm based dependencies. We have provided some of them in `arm_dependencies` folder. Or you can pull docker image `asmitaj08/afl-qemu-arm`

