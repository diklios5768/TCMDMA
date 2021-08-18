# -*- encoding: utf-8 -*-
"""
@File Name      :   onion_layers.py    
@Create Time    :   2021/8/3 17:59
@Description    :   
@Version        :   
@License        :   
@Author         :   diklios
@Contact Email  :   diklios5768@gmail.com
@Github         :   https://github.com/diklios5768
@Blog           :   
@Motto          :   All our science, measured against reality, is primitive and childlike - and yet it is the most precious thing we have.
"""
__auth__ = 'diklios'

import json
import networkx as nx
from app.libs.lists import colors, colors_length
from app.utils.algorithm_handler.common import rows_to_graph, rows_to_graph_with_weight
from app.utils.algorithm_handler.complex_network.image import generate_image_with_differentiate


def onion_layers(graph):
    return nx.onion_layers(graph)


def handle_onion_layers_result_show(graph, partition, params, user_project_analysis_files_dir, limits={}):
    fore_end_graph_limit = limits.get('fore_end_graph_limit', 500)
    fore_end_table_limit = limits.get('fore_end_table_limit', 2000)
    nodes = list(graph.nodes())
    edges = graph.edges(data=True)
    sub_nodes=nodes[0:fore_end_graph_limit]
    sub_graph = graph.subgraph(sub_nodes)
    sub_edges=sub_graph.edges(data=True)
    tree_data = [
        {'title': '节点', 'key': 'nodes', 'children': [{'title': node, 'key': node} for node in sub_nodes]}]
    edges_data = [{"source": edge[0], "target": edge[1], "label": edge[2]['weight']} for edge in sub_edges]
    combos = list(set(partition.values()))
    combos_data = [{"id": '分组' + str(combo + 1), "label": '分组' + str(combo + 1)} for combo in combos]
    nodes_data = [{"id": node[0], "comboId": '分组' + str(node[1] + 1),
                   "style": {
                       "keyshape": {
                           "fill": colors[index % colors_length],
                           "stroke": colors[index % colors_length]
                       },
                       "label": {
                           "value": node[0],
                           "position": 'top',
                           "fill": '#000000',
                           "fontSize": 16,
                           "fontFamily": 'normal',
                           "textAlign": 'center',
                           "offset": 0,
                       }
                   }} for (index, node) in enumerate(partition.items())]
    graph_data = {"nodes": nodes_data[0:fore_end_graph_limit], "edges": edges_data, "combos": combos_data}
    communities = {combo: '' for combo in combos}
    for (index, node) in enumerate(partition.items()):
        communities[node[1]] += node[0] + ','
    community_table_data = {
        "table_name": "community",
        "table_chinese_name": "社团结果",
        "columns_type": [
            {"key": 'community_number', "dataIndex": 'community_number', "title": '社团编号'},
            {"key": 'community', "dataIndex": 'community', "title": '社团结果'},
        ],
        "rows": [{'key': community[0], 'community_number': community[0], 'community': community[1]} for community in
                 communities.items()][0:fore_end_table_limit]
    }
    tables_data = [community_table_data]
    pdf_tables = [[('社团编号', '划分结果')]]
    for community in communities.items():
        pdf_tables[0].append((community[0], community[1]))
    pdf_images = {'main_image_name': '网络图', 'data': {'nodes': list(partition.items()), 'edges': edges},
                  'sub_images': [{'name': '分组' + str(community[0])} for community in communities.items()]}

    image_files_path = generate_image_with_differentiate(pdf_images['data'],
                                                         communities=communities,
                                                         image_name=pdf_images['main_image_name'],
                                                         user_project_analysis_files_dir=user_project_analysis_files_dir)

    pdf_images['main_image_file_path'] = image_files_path['main_image_file_path']
    for (index, sub_image) in enumerate(pdf_images['sub_images']):
        sub_image['sub_image_file_path'] = image_files_path['sub_images_file_path'][index]
    pdf_stories = [{'content_type': 'title', 'content': 'onion_layers社团发现分析结果'},
                   {'content_type': 'h1', 'content': '参数设置'},
                   {'content_type': 'body',
                    'content': '本次的参数设置为：附带权重' if params['weight'] == True else '本次的参数设置为：不附带权重'},
                   {'content_type': 'h1', 'content': '分析结果'},
                   {'content_type': 'h2', 'content': '社团划分结果'},
                   {'content_type': 'three_line_table', 'content': pdf_tables[0], 'table_name': '社团发现结果表'},
                   {'content_type': 'h2', 'content': '网络图展示'},
                   {'content_type': 'image', 'image_file_path': pdf_images['main_image_file_path'],
                    'image_name': pdf_images['main_image_name'], 'width': 400, 'height': 300},
                   {'content_type': 'h2', 'content': '网络图子图展示'},
                   ]
    for sub_image in pdf_images['sub_images']:
        pdf_stories.append({'content_type': 'image', 'image_file_path': sub_image['sub_image_file_path'],
                            'image_name': sub_image['name'], 'width': 400, 'height': 300})
    pdf_stories.append({'content_type': 'page_break'})
    excel_sheets_data = [{'name': '频次表', 'data': [('社团编号', '划分结果')]}]
    for community in communities.items():
        excel_sheets_data[0]['data'].append((community[0], community[1]))
    return {"tree_data": tree_data, "graph_data": graph_data, "tables_data": tables_data,
            "raw_result_data": {"community": json.dumps(list(partition.items()))}, "pdf_stories": pdf_stories,
            "excel_sheets_data": excel_sheets_data}


def handle_onion_layers(data: list, params: dict, user_project_analysis_files_dir):
    rows = [row[0] for row in data]
    weight = params.get('weight', False)
    if weight:
        graph = rows_to_graph_with_weight(rows)
    else:
        graph = rows_to_graph(rows)
    partition = onion_layers(graph)
    return handle_onion_layers_result_show(graph, partition, params, user_project_analysis_files_dir)


if __name__ == '__main__':
    handle_onion_layers([['蛇舌草,半枝莲,龙葵,石打穿,狗舌草,莪术,山慈菇,漏芦,肿节风,猫爪草,泽漆,土鳖虫,桃仁,蟾皮,砂仁'],
                         ['败酱草,椿根白皮,墓头回,生薏苡仁,冬瓜子,苦参,泽泻,红藤,仙鹤草,失笑散,太子参,枸杞'],
                         ['党参,焦白术,茯苓,炙甘草,太子参,麦冬,北沙参,仙鹤草,生薏苡仁,藤梨根,鸡血藤,泽漆,椿根白皮,夜交藤'],
                         ['党参,焦白术,茯苓,炙甘草,太子参,麦冬,北沙参,石斛,仙鹤草,生薏苡仁'],
                         ['法半夏,莱菔子,石斛,党参,焦白术,茯苓,炙甘草,太子参,麦冬,北沙参,仙鹤草,生薏苡仁,藤梨根']],
                        params={'weight': True},
                        user_project_analysis_files_dir='D:\\Coding\\Python\\databaseAPI\\app\\users\\data\\1-user0\\2021-08-02-13-30-34--104-sa\\504-homogeneous方法分析结果')
