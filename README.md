# FuzzingBusyBox_LLM

We have performed fuzzing on BusyBox target extracted from firmware of real-world embedded products (Firmware database provided by [NetRise](https://www.netrise.io/)).
Apart from fuzzing using AFL++, we have leveraged LLM (Using OpenAI GPT-4) for initial input generation, followed by adding crash reuse technique to the pipline. 
This repo is for paper :  *"Fuzzing BusyBox: Leveraging LLM and Crash Reuse for Embedded Bug Unearthing", Usenix 2024*

* We provide a basic automation script to perfrom fuzzing on a large batch of target binaries using AFL++. (Folder : *automation_src*)
* Target architecture : x86_64 and ARM_32
* 
* Command :
`python3 fuzz_multiple_targets.py --input /path/to/binary/collection --arch ARM_32/x86_64 --corpus /path/to/corpus --output /path/for/output --afl-path path/of/afl  --run-time required_runtime --depend arm_dependecies_in_case_of_arm `