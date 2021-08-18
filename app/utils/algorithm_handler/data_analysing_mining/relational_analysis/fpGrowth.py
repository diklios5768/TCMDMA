# 使用fpgrowth_py包，或者pyfpgrowth包
from fpgrowth_py import fpgrowth


def fp_growth_analysis(data, min_sup_ratio, min_conf):
    freq_item_set, rules = fpgrowth(data, minSupRatio=min_sup_ratio, minConf=min_conf)
    return freq_item_set, rules
