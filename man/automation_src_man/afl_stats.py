import os


def get_afl_fuzz_stats(fuzz_output_dir : str, end_fuzz: bool = False) -> dict :
    """ Dump fuzzin status after fuzzing is completed"""
    
    stats_file = os.path.join(fuzz_output_dir, 'default/fuzzer_stats')
    # print(f'Fuzzer stats file path : {stats_file}')
    stats_file_dict = {}
    if not os.path.exists(stats_file):
        print(f'Cannot find fuzzer_stats file : {stats_file}')
        return False , stats_file_dict
    
    # with open(stats_file, encoding='utf-8') as fuzz_stat_file :
    #     stats_file_lines = fuzz_stat_file.read().splitlines()
    fuzz_stat_file = open(stats_file, encoding='utf-8')
    stats_file_lines = fuzz_stat_file.read().splitlines()

    if end_fuzz == True:
          fuzz_stat_file.close()
    
    for stat_line in stats_file_lines :
        key, value = stat_line.split(': ')
        stats_file_dict[key.strip()] = value.strip()

    return True, stats_file_dict
