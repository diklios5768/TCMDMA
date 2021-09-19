# -*- encoding: utf-8 -*-
"""
@File Name      :   image.py    
@Create Time    :   2021/7/31 17:28
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

import networkx as nx
import matplotlib.pyplot as plt
from app.libs.error_exception import ParameterException
from app.libs.lists import colors, colors_length
from app.utils.file_handler import make_dir
from app.utils.file_handler.text_handler import filter_empty_text

# 解决main thread is not in main loop
# matplotlib.use('Agg')
plt.switch_backend('agg')


def generate_image_from_graph(graph, filename: str, user_project_analysis_files_dir: str):
    # pos = nx.spring_layout(graph)
    pos = nx.circular_layout(graph)
    main_figure = plt.figure(figsize=(20, 20))
    nx.draw(graph, pos, node_size=1000, node_color='#2ec7c9', arrows=True, with_labels=True, font_family='SimHei',
            font_size=10)
    file_dir = user_project_analysis_files_dir
    if make_dir(file_dir):
        png_file_path = file_dir + filename + '.png'
        main_figure.savefig(png_file_path, format="PNG")
        jpg_file_path = file_dir + filename + '.jpeg'
        main_figure.savefig(jpg_file_path, format="JPEG")
        svg_file_path = file_dir + filename + '.svg'
        main_figure.savefig(svg_file_path, format="SVG")
        plt.close(main_figure)
        return png_file_path
    else:
        raise ParameterException()


def generate_image(filename, data: dict, user_project_analysis_files_dir: str):
    nodes = data.get('nodes', None)
    edges = data.get('edges', None)
    if nodes is None:
        raise ParameterException()
    graph = nx.Graph()
    graph.add_nodes_from(nodes)
    for edge in edges:
        graph.add_edge(edge['source'], edge['target'])
    return generate_image_from_graph(graph, filename=filename,
                                     user_project_analysis_files_dir=user_project_analysis_files_dir)


def generate_image_from_graph_with_differentiate(graph, color_map, communities, image_name,
                                                 user_project_analysis_files_dir: str):
    # pos = nx.spring_layout(graph)
    pos = nx.circular_layout(graph)
    main_figure = plt.figure(figsize=(20, 20))
    nx.draw(graph, pos, node_size=1000, node_color=color_map, arrows=True, with_labels=True, font_family='SimHei',
            font_size=10)
    file_dir = user_project_analysis_files_dir
    image_files_path = {'main_image_file_path': '', 'sub_images_file_path': []}
    if make_dir(file_dir):
        png_file_path = file_dir + image_name + '.png'
        main_figure.savefig(png_file_path, format="png")
        jpg_file_path = file_dir + image_name + '.jpeg'
        main_figure.savefig(jpg_file_path, format="jpeg")
        svg_file_path = file_dir + image_name + '.svg'
        main_figure.savefig(svg_file_path, format="svg")
        image_files_path['main_image_file_path'] = png_file_path
        plt.close(main_figure)
    else:
        raise ParameterException()
    sub = 0
    # print(communities.items())
    for community in communities.items():
        sub_figure = plt.figure(figsize=(20, 20))
        nodes = filter_empty_text(community[1].split(','))
        sub_graph = graph.subgraph(nodes)
        color = colors[sub % colors_length]
        sub_pos = nx.circular_layout(sub_graph)
        nx.draw(sub_graph, sub_pos, node_size=1000, node_color=color, arrows=True, with_labels=True,
                font_family='SimHei', font_size=10)
        sub_png_file_path = file_dir + image_name + '分组' + str(community[0]) + '.png'
        sub_figure.savefig(sub_png_file_path)
        sub_jpg_file_path = file_dir + image_name + '分组' + str(community[0]) + '.jpeg'
        sub_figure.savefig(sub_jpg_file_path, format="jpeg")
        sub_svg_file_path = file_dir + image_name + '分组' + str(community[0]) + '.svg'
        sub_figure.savefig(sub_svg_file_path, format="svg")
        image_files_path['sub_images_file_path'].append(sub_png_file_path)
        sub += 1
        plt.close(sub_figure)
    return image_files_path


def generate_image_with_differentiate(data: dict, communities, image_name, user_project_analysis_files_dir: str):
    nodes = data.get('nodes', None)
    edges = data.get('edges', None)
    if nodes is None:
        raise ParameterException()
    graph = nx.Graph()
    color_map = []
    for node in nodes:
        graph.add_node(node[0])
        color_map.append(colors[node[1] % colors_length])
    graph.add_edges_from(edges)
    graph.to_undirected()
    return generate_image_from_graph_with_differentiate(graph, color_map, communities, image_name,
                                                        user_project_analysis_files_dir)
