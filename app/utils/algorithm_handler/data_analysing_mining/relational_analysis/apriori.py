from app.utils.run_handler import print_func_execute_time
# 使用Efficient-Apriori，挖掘关联规则
from efficient_apriori import apriori


# @print_func_execute_time
def apriori_analysis(data, min_support=0.5, min_confidence=0.5):
    """
    data:列表，每一行都是元组
    min_support:最小支持的
    min_confidence:最小置信度
    """
    item_sets, rules = apriori(data, min_support=min_support, min_confidence=min_confidence)
    return item_sets, rules


def single_items_sorted(single_items):
    single_items_sorted_result = sorted(single_items, key=lambda item: item['frequency'], reverse=True)
    return single_items_sorted_result


def items_sorted(items):
    items_sorted_result = sorted(items, key=lambda item: item['confidence'], reverse=True)
    return items_sorted_result


def rules_filter(rules, lhs, rhs):
    # 过滤出左边和右边固定为多少个项集的规则
    rules_filter_result = filter(lambda rule: len(rule.lhs) == lhs and len(rule.rhs) == rhs, rules)
    return rules_filter_result


def rules_sorted(rules):
    # 对结果进行排序
    rules_sorted_result = sorted(rules, key=lambda rule: rule['lift'], reverse=True)
    return rules_sorted_result
