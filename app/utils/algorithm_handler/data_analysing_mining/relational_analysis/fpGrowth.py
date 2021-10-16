# 使用fpgrowth_py包，或者pyfpgrowth包
from fpgrowth_py import fpgrowth


# todo:将频繁项集和关联规则改造一下格式，暂时还不能适应现在的结果处理方式
def fp_growth_analysis(data, min_support, min_confidence):
    freq_item_set, rules = fpgrowth(data, minSupRatio=min_support, minConf=min_confidence)
    return freq_item_set, rules
