from app.utils.algorithm_handler.complex_network.image import generate_image
from app.utils.algorithm_handler.data_analysing_mining.relational_analysis.apriori import apriori_analysis, \
    single_items_sorted, items_sorted, rules_sorted
from app.utils.file_handler.text_handler.list import filter_empty_text
from app.utils.file_handler.text_handler.regex import replace_character


# from app.utils.algorithm_handler.data_analysing_mining.relational_analysis.fpGrowth import fp_growth_analysis

# 从行切分为二维表格
def rows_to_table(rows, character=','):
    data = []
    all_node_data = []
    for row in rows:
        row = replace_character(row)
        row_list = row.split(character)
        no_empty_row = list(set(filter_empty_text(row_list, method='empty')))
        data.append(tuple(no_empty_row))
        all_node_data.extend(no_empty_row)
    all_node_data = list(set(all_node_data))
    return data, all_node_data


def handle_homogeneous_result_show(item_sets, rules, params: dict = {}, user_project_analysis_files_dir: str = '',
                                   limits={}):
    fore_end_table_limit = limits.get('fore_end_table_limit', 2000)
    fore_end_graph_limit = limits.get('fore_end_graph_limit', 500)
    item_sets_rows = []
    # 绘图需要使用的数据
    if item_sets.get('1', None):
        single_items_num = len(item_sets[1])
    else:
        single_items_num = 0
    items_num = 0
    for key_num in item_sets:
        for item in item_sets[key_num]:
            value = item_sets[key_num][item]
            name = ','.join(item)
            item_sets_rows.append({
                "key": items_num,
                "items": name,
                'frequency': value,
            })
            items_num += 1
    for row in item_sets_rows:
        row['confidence'] = row['frequency'] / items_num
    item_sets_table_data = {
        "table_name": "Items",
        "table_chinese_name": "频繁项集",
        "columns_type": [
            {"key": 'items', "dataIndex": 'items', "title": 'Items'},
            {"key": 'frequency', "dataIndex": 'frequency', "title": 'Frequency'},
            {"key": 'confidence', "dataIndex": 'confidence', "title": 'Confidence'},
        ],
        "rows": item_sets_rows[0:fore_end_table_limit]
    }
    rules_rows = []
    for (index, rule) in enumerate(rules):
        rule_str = '(' + ",".join(rule.lhs) + ')-->(' + ','.join(rule.rhs) + ')'
        rule_source = ','.join(rule.lhs)
        rule_target = ','.join(rule.rhs)
        rules_rows.append({
            "key": index,
            "rules": rule_str,
            "rule_source": rule_source,
            "rule_target": rule_target,
            "support": rule.support,
            "confidence": rule.confidence,
            "lift": rule.lift
        })
    rules_table_data = {
        "table_name": "Rules",
        "table_chinese_name": "关联规则",
        "columns_type": [
            {"key": 'rules', "dataIndex": 'rules', "title": 'Rules'},
            {"key": 'support', "dataIndex": 'support', "title": 'Support'},
            {"key": 'confidence', "dataIndex": 'confidence', "title": 'Confidence'},
            {"key": 'lift', "dataIndex": 'lift', "title": 'Lift'},
        ],
        "rows": rules_rows[0:fore_end_table_limit]
    }
    tables_data = [item_sets_table_data, rules_table_data]
    edges_data = [{"source": left, "target": right} for rule in rules for left in rule.lhs for right in rule.rhs]
    edges_data = [dict(t) for t in set([tuple(d.items()) for d in edges_data])][0:fore_end_graph_limit]
    nodes_source = [edge["source"] for edge in edges_data]
    nodes_target = [edge["target"] for edge in edges_data]
    nodes = nodes_source + nodes_target
    nodes = list(set(nodes))
    # print(nodes)
    nodes_data = [{"id": node, "style": {"label": {
        "value": node,
        "position": 'top',
        "fill": '#000000',
        "fontSize": 16,
        "fontFamily": 'normal',
        "textAlign": 'center',
        "offset": 0,
    }}} for node in nodes]
    tree_data = [
        {'title': '节点', 'key': 'nodes', 'children': [{'title': node, 'key': node} for node in nodes]}]
    graph_data = {"nodes": nodes_data, "edges": edges_data}
    # PDF需要使用的数据
    # PDF表格
    pdf_table_limit = limits.get('pdf_table_limit', 20)
    pdf_tables = [
        [('名称', '频次')],
        [('频繁项集', '置信度数', '置信度')],
        [('关联规则', '置信度', '支持度', '提升度')]
    ]
    single_items_sorted_result = single_items_sorted(item_sets_rows[0:single_items_num])
    for item in single_items_sorted_result[0:pdf_table_limit]:
        pdf_tables[0].append((item['items'], str(item['frequency'])))
    items_sorted_result = items_sorted(item_sets_rows)
    for item in items_sorted_result[0:pdf_table_limit]:
        pdf_tables[1].append((item['items'], str(item['frequency']), str(item['confidence'])))
    rules_sorted_result = rules_sorted(rules_rows)
    for rule in rules_sorted_result[0:pdf_table_limit]:
        pdf_tables[2].append((rule['rules'], str(rule['support']), str(rule['confidence']), str(rule['lift'])))
    # pdf图片
    backend_rules_limit = rules_sorted_result
    backend_rules_limit_edges_data = [{"source": left, "target": right} for rule in backend_rules_limit for left in
                                      rule['rule_source'].split(',') for right in rule['rule_target'].split(',')]
    backend_rules_limit_edges_data = [dict(t) for t in set([tuple(d.items()) for d in backend_rules_limit_edges_data])]
    backend_rules_limit_nodes_source = [edge["source"] for edge in backend_rules_limit_edges_data]
    backend_rules_limit_nodes_target = [edge["target"] for edge in backend_rules_limit_edges_data]
    backend_rules_limit_nodes_data = backend_rules_limit_nodes_source + backend_rules_limit_nodes_target
    backend_rules_limit_nodes_data = list(set(backend_rules_limit_nodes_data))
    pdf_images = [{'image_name': '关联度最高的节点关系图',
                   'data': {'nodes': backend_rules_limit_nodes_data,
                            'edges': backend_rules_limit_edges_data}}]
    for pdf_image in pdf_images:
        image_file_path = generate_image(pdf_image['image_name'], pdf_image['data'], user_project_analysis_files_dir)
        pdf_image['image_file_path'] = image_file_path

    pdf_stories = [{'content_type': 'title', 'content': '关联分析结果'},
                   {'content_type': 'h1', 'content': '参数设置'},
                   {'content_type': 'body', 'content': '本次的参数设置为：最小支持度' + str(params['min_support']) + '，最小置信度' + str(
                       params['min_confidence'])},
                   {'content_type': 'h1', 'content': '分析结果'},
                   {'content_type': 'h2', 'content': '频次分析结果'},
                   {'content_type': 'three_line_table', 'content': pdf_tables[0], 'table_name': '频次表'},
                   {'content_type': 'attention', 'content': '注意：只提供了最高的前' + str(pdf_table_limit) + '个数据项'},
                   {'content_type': 'h2', 'content': '频繁项集分析结果'},
                   {'content_type': 'three_line_table', 'content': pdf_tables[1], 'table_name': '频繁项集表'},
                   {'content_type': 'attention', 'content': '注意：只提供了最高的前' + str(pdf_table_limit) + '个数据项'},
                   {'content_type': 'h2', 'content': '关联规则分析结果'},
                   {'content_type': 'three_line_table', 'content': pdf_tables[2], 'table_name': '关联规则表'},
                   {'content_type': 'attention', 'content': '注意：只提供了最高的前' + str(pdf_table_limit) + '个数据项'},
                   {'content_type': 'h2', 'content': '节点关系展示'},
                   {'content_type': 'image', 'image_file_path': pdf_images[0]['image_file_path'],
                    'image_name': pdf_images[0]['image_name'], 'width': 400, 'height': 300},
                   {'content_type': 'page_break'}
                   ]
    # excel表需要使用的数据
    excel_sheets_data = [{'name': '频次表', 'data': [('名称', '频次')]},
                         {'name': '频繁项集表', 'data': [('频繁项集', '置信度数', '置信度')]},
                         {'name': '关联规则表', 'data': [('关联规则', '置信度', '支持度', '提升度')]}]
    for item in single_items_sorted_result:
        excel_sheets_data[0]['data'].append((item['items'], item['frequency']))
    for item in items_sorted_result:
        excel_sheets_data[1]['data'].append((item['items'], item['frequency'], item['confidence']))
    for rule in rules_sorted_result:
        excel_sheets_data[2]['data'].append((rule['rules'], rule['support'], rule['confidence'], rule['lift']))

    return {"tree_data": tree_data, "graph_data": graph_data, "tables_data": tables_data,
            "raw_result_data": {"item_sets": str(item_sets), "rules": str(rules)}, "pdf_stories": pdf_stories,
            "excel_sheets_data": excel_sheets_data}


def relational_analysis(rows, min_support, min_confidence, method='homogeneous'):
    if method == 'homogeneous':
        data, all_node_data = rows_to_table(rows)
        item_sets, rules = apriori_analysis(data, min_support, min_confidence)
        return handle_homogeneous_result_show(item_sets, rules)
    elif method == 'heterogeneous':
        return False
    else:
        return False


def handle_homogeneous(data: list, params: dict, user_project_analysis_files_dir: str):
    rows = [row[0] for row in data]
    # print(rows)
    main_data, all_node_data = rows_to_table(rows)
    # print(main_data)
    item_sets, rules = apriori_analysis(main_data, min_support=params['min_support'],
                                        min_confidence=params['min_confidence'])
    # item_sets, rules =fp_growth_analysis(main_data, min_support=params['min_support'],
    #                                      min_confidence=params['min_confidence'])
    # print(item_sets)
    # print(rules)
    return handle_homogeneous_result_show(item_sets, rules, params, user_project_analysis_files_dir)


# if __name__ == '__main__':
#     handle_homogeneous([],
#         params={'min_support': 0.6, 'min_confidence': 0.6},
#         user_project_analysis_files_dir='D:\\Coding\\Python\\TCMDMA\\app\\users\\data\\1-user0\\2021-08-02-13-30-34--104-sa\\504-cliques方法分析结果')
