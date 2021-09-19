import sys
import warnings
import numpy as np
import pandas as pd
import networkx as nx
from collections import defaultdict
from scipy.stats import binom
from app.utils.algorithm_handler.common import rows_to_graph_with_weight, rows_to_graph
from app.utils.algorithm_handler.complex_network.image import generate_image_from_graph


def read(
        filename,
        column_of_interest,
        triangular_input=False,
        consider_self_loops=True,
        undirected=False,
        drop_zeroes=True,
        sep="\t"):
    """Reads a field separated input file into the internal backboning format (a Pandas Dataframe).
   The input file should have three or more columns (default separator: tab).
   The input file must have a one line header with the column names.
   There must be two columns called 'src' and 'trg', indicating the origin and destination of the interaction.
   All other columns must contain integer or floats, indicating the edge weight.
   In case of undirected network, the edges have to be present in both directions with the same weights, or set triangular_input to True.

   Args:
   filename (str): The path to the file containing the edges.
   column_of_interest (str): The column name identifying the weight that will be used for the backboning.

   KWArgs:
   triangular_input (bool): Is the network undirected and are the edges present only in one direction? default: False
   consider_self_loops (bool): Do you want to consider self loops when calculating the backbone? default: True
   undirected (bool): Is the network undirected? default: False
   drop_zeroes (bool): Do you want to keep zero weighted connections in the network? Important: it affects methods based on degree, like disparity_filter. default: False
   sep (char): The field separator of the inout file. default: tab

   Returns:
   The parsed network data, the number of nodes in the network and the number of edges.
   """
    table = pd.read_csv(filename, sep=sep)
    table = table[["src", "trg", column_of_interest]]
    table.rename(columns={column_of_interest: "nij"}, inplace=True)
    if drop_zeroes:
        table = table[table["nij"] > 0]
    if not consider_self_loops:
        table = table[table["src"] != table["trg"]]
    if triangular_input:
        table2 = table.copy()
        table2["new_src"] = table["trg"]
        table2["new_trg"] = table["src"]
        table2.drop("src", 1, inplace=True)
        table2.drop("trg", 1, inplace=True)
        table2 = table2.rename(columns={"new_src": "src", "new_trg": "trg"})
        table = pd.concat([table, table2], axis=0)
        table = table.drop_duplicates(subset=["src", "trg"])
    original_nodes = len(set(table["src"]) | set(table["trg"]))
    original_edges = table.shape[0]
    if undirected:
        return table, original_nodes, original_edges / 2
    else:
        return table, original_nodes, original_edges


def thresholding(table, threshold):
    """Reads a preprocessed edge table and returns only the edges supassing a significance threshold.

   Args:
   table (pandas.DataFrame): The edge table.
   threshold (float): The minimum significance to include the edge in the backbone.

   Returns:
   The network backbone.
   """
    table = table.copy()
    if "sdev_cij" in table:
        return table[(table["score"] - (threshold * table["sdev_cij"]))
                     > 0][["src", "trg", "nij", "score"]]
    else:
        return table[table["score"] > threshold][[
            "src", "trg", "nij", "score"]]


def write(table, network, method, folder):
    if not table.empty and "src" in table:
        table.to_csv(
            "%s/%s_%s.csv" %
            (folder,
             network,
             method),
            sep="\t",
            index=False)
    else:
        warnings.warn(
            "Incorrect/empty output. Nothing written on disk",
            RuntimeWarning)


def stability_jac(table1, table2):
    table1_edges = set(zip(table1["src"], table1["trg"]))
    table2_edges = set(zip(table2["src"], table2["trg"]))
    return float(len(table1_edges & table2_edges)) / \
           len(table1_edges | table2_edges)


def stability_corr(table1, table2, method="spearman", log=False, what="nij"):
    corr_table = table1.merge(table2, on=["src", "trg"])
    corr_table = corr_table[["%s_x" % what, "%s_y" % what]]
    if log:
        corr_table["%s_x" % what] = np.log(corr_table["%s_x" % what])
        corr_table["%s_y" % what] = np.log(corr_table["%s_y" % what])
    return corr_table["%s_x" % what].corr(
        corr_table["%s_y" % what], method=method)


def test_densities(table, start, end, step):
    if start > end:
        raise ValueError("start must be lower than end")
    steps = []
    x = start
    while x <= end:
        steps.append(x)
        x += step
    onodes = len(set(table["src"]) | set(table["trg"]))
    oedges = table.shape[0]
    oavgdeg = (2.0 * oedges) / onodes
    for s in steps:
        edge_table = thresholding(table, s)
        nodes = len(set(edge_table["src"]) | set(edge_table["trg"]))
        edges = edge_table.shape[0]
        avgdeg = (2.0 * edges) / nodes
        yield (s, nodes, (100.0 * nodes) / onodes, edges, (100.0 * edges) / oedges, avgdeg, avgdeg / oavgdeg)


def noise_corrected(
        table,
        undirected=False,
        return_self_loops=False,
        calculate_p_value=False):
    sys.stderr.write("Calculating NC score...\n")
    table = table.copy()
    src_sum = table.groupby(by="src").sum()[["nij"]]
    table = table.merge(
        src_sum,
        left_on="src",
        right_index=True,
        suffixes=(
            "",
            "_src_sum"))
    trg_sum = table.groupby(by="trg").sum()[["nij"]]
    table = table.merge(
        trg_sum,
        left_on="trg",
        right_index=True,
        suffixes=(
            "",
            "_trg_sum"))
    table.rename(
        columns={
            "nij_src_sum": "ni.",
            "nij_trg_sum": "n.j"},
        inplace=True)
    table["n.."] = table["nij"].sum()
    table["mean_prior_probability"] = (
                                              (table["ni."] * table["n.j"]) / table["n.."]) * (1 / table["n.."])
    if calculate_p_value:
        table["score"] = binom.cdf(
            table["nij"],
            table["n.."],
            table["mean_prior_probability"])
        return table[["src", "trg", "nij", "score"]]
    table["kappa"] = table["n.."] / (table["ni."] * table["n.j"])
    table["score"] = ((table["kappa"] * table["nij"]) - 1) / \
                     ((table["kappa"] * table["nij"]) + 1)
    table["var_prior_probability"] = (1 / (table["n.."] ** 2)) * (
            table["ni."] * table["n.j"] * (table["n.."] - table["ni."]) * (table["n.."] - table["n.j"])) / (
                                             (table["n.."] ** 2) * ((table["n.."] - 1)))
    table["alpha_prior"] = (
                                   ((table["mean_prior_probability"] ** 2) / table["var_prior_probability"]) * (
                                   1 - table["mean_prior_probability"])) - table["mean_prior_probability"]
    table["beta_prior"] = (table["mean_prior_probability"] / table["var_prior_probability"]) * (
            1 - (table["mean_prior_probability"] ** 2)) - (1 - table["mean_prior_probability"])
    table["alpha_post"] = table["alpha_prior"] + table["nij"]
    table["beta_post"] = table["n.."] - table["nij"] + table["beta_prior"]
    table["expected_pij"] = table["alpha_post"] / \
                            (table["alpha_post"] + table["beta_post"])
    table["variance_nij"] = table["expected_pij"] * \
                            (1 - table["expected_pij"]) * table["n.."]
    table["d"] = (1.0 / (table["ni."] * table["n.j"])) - (table["n.."] *
                                                          ((table["ni."] + table["n.j"]) / (
                                                                  (table["ni."] * table["n.j"]) ** 2)))
    table["variance_cij"] = table["variance_nij"] * (((2 * (table["kappa"] + (
            table["nij"] * table["d"]))) / (((table["kappa"] * table["nij"]) + 1) ** 2)) ** 2)
    table["sdev_cij"] = table["variance_cij"] ** .5
    if not return_self_loops:
        table = table[table["src"] != table["trg"]]
    if undirected:
        table = table[table["src"] <= table["trg"]]
    return table[["src", "trg", "nij", "score", "sdev_cij"]]


def doubly_stochastic(table, undirected=False, return_self_loops=False):
    sys.stderr.write("Calculating DST score...\n")
    table = table.copy()
    table2 = table.copy()
    original_nodes = len(set(table["src"]) | set(table["trg"]))
    table = pd.pivot_table(
        table,
        values="nij",
        index="src",
        columns="trg",
        aggfunc="sum",
        fill_value=0) + .001
    row_sums = table.sum(axis=1)
    attempts = 0
    while np.std(row_sums) > 1e-12:
        table = table.div(row_sums, axis=0)
        col_sums = table.sum(axis=0)
        table = table.div(col_sums, axis=1)
        row_sums = table.sum(axis=1)
        attempts += 1
        if attempts > 1000:
            warnings.warn(
                "Matrix could not be reduced to doubly stochastic. See Sec. 3 of Sinkhorn 1964",
                RuntimeWarning)
            return pd.DataFrame()
    table = pd.melt(table.reset_index(), id_vars="src")
    table = table[table["src"] < table["trg"]]
    table = table[table["value"] > 0].sort_values(by="value", ascending=False)
    i = 0
    if undirected:
        G = nx.Graph()
        while nx.number_connected_components(
                G) != 1 or nx.number_of_nodes(G) < original_nodes:
            edge = table.iloc[i]
            G.add_edge(edge["src"], edge["trg"], weight=edge["value"])
            i += 1
    else:
        G = nx.DiGraph()
        while nx.number_weakly_connected_components(
                G) != 1 or nx.number_of_nodes(G) < original_nodes:
            edge = table.iloc[i]
            G.add_edge(edge["src"], edge["trg"], weight=edge["value"])
            i += 1
    table = pd.melt(nx.to_pandas_adjacency(G).reset_index(), id_vars="index")
    table = table[table["value"] > 0]
    table.rename(
        columns={
            "index": "src",
            "variable": "trg",
            "value": "cij"},
        inplace=True)
    table["score"] = table["cij"]
    table = table.merge(table2[["src", "trg", "nij"]], on=["src", "trg"])
    if not return_self_loops:
        table = table[table["src"] != table["trg"]]
    if undirected:
        table = table[table["src"] <= table["trg"]]
    return table[["src", "trg", "nij", "score"]]


def disparity_filter(table, undirected=False, return_self_loops=False):
    sys.stderr.write("Calculating DF score...\n")
    table = table.copy()
    table_sum = table.groupby(table["src"]).sum().reset_index()
    table_deg = table.groupby(table["src"]).count()["trg"].reset_index()
    table = table.merge(table_sum, on="src", how="left", suffixes=("", "_sum"))
    table = table.merge(
        table_deg,
        on="src",
        how="left",
        suffixes=(
            "",
            "_count"))
    table["score"] = 1.0 - \
                     ((1.0 - (table["nij"] / table["nij_sum"])) ** (table["trg_count"] - 1))
    table["variance"] = (table["trg_count"] ** 2) * (((20 + (4.0 * table["trg_count"])) / (
            (table["trg_count"] + 1.0) * (table["trg_count"] + 2) * (table["trg_count"] + 3))) - (
                                                             (4.0) / ((table["trg_count"] + 1.0) ** 2)))
    if not return_self_loops:
        table = table[table["src"] != table["trg"]]
    if undirected:
        table["edge"] = table.apply(
            lambda x: "%s-%s" %
                      (min(
                          x["src"], x["trg"]), max(
                          x["src"], x["trg"])), axis=1)
        table_maxscore = table.groupby(by="edge")["score"].max().reset_index()
        table_minvar = table.groupby(by="edge")["variance"].min().reset_index()
        table = table.merge(table_maxscore, on="edge", suffixes=("_min", ""))
        table = table.merge(table_minvar, on="edge", suffixes=("_max", ""))
        table = table.drop_duplicates(subset=["edge"])
        table = table.drop("edge", 1)
        table = table.drop("score_min", 1)
        table = table.drop("variance_max", 1)
    return table[["src", "trg", "nij", "score", "variance"]]


def high_salience_skeleton(table, undirected=False, return_self_loops=False):
    sys.stderr.write("Calculating HSS score...\n")
    table = table.copy()
    table["distance"] = 1.0 / table["nij"]
    nodes = set(table["src"]) | set(table["trg"])
    G = nx.from_pandas_edgelist(
        table,
        source="src",
        target="trg",
        edge_attr="distance",
        create_using=nx.DiGraph())
    cs = defaultdict(float)
    for s in nodes:
        pred = defaultdict(list)
        dist = {t: float("inf") for t in nodes}
        dist[s] = 0.0
        Q = defaultdict(list)
        for w in dist:
            Q[dist[w]].append(w)
        S = []
        while len(Q) > 0:
            v = Q[min(Q.keys())].pop(0)
            S.append(v)
            for _, w, l in G.edges(nbunch=[v, ], data=True):
                new_distance = dist[v] + l["distance"]
                if dist[w] > new_distance:
                    Q[dist[w]].remove(w)
                    dist[w] = new_distance
                    Q[dist[w]].append(w)
                    pred[w] = []
                if dist[w] == new_distance:
                    pred[w].append(v)
            while len(S) > 0:
                w = S.pop()
                for v in pred[w]:
                    cs[(v, w)] += 1.0
            Q = defaultdict(list, {k: v for k, v in Q.items() if len(v) > 0})
    table["score"] = table.apply(
        lambda x: cs[(x["src"], x["trg"])] / len(nodes), axis=1)
    if not return_self_loops:
        table = table[table["src"] != table["trg"]]
    if undirected:
        table["edge"] = table.apply(
            lambda x: "%s-%s" %
                      (min(
                          x["src"], x["trg"]), max(
                          x["src"], x["trg"])), axis=1)
        table_maxscore = table.groupby(by="edge")["score"].sum().reset_index()
        table = table.merge(table_maxscore, on="edge", suffixes=("_min", ""))
        table = table.drop_duplicates(subset=["edge"])
        table = table.drop("edge", 1)
        table = table.drop("score_min", 1)
        table["score"] = table["score"] / 2.0
    return table[["src", "trg", "nij", "score"]]


def naive(table, undirected=False, return_self_loops=False):
    sys.stderr.write("Calculating Naive score...\n")
    table = table.copy()
    table["score"] = table["nij"]
    if not return_self_loops:
        table = table[table["src"] != table["trg"]]
    if undirected:
        table["edge"] = table.apply(
            lambda x: "%s-%s" %
                      (min(
                          x["src"], x["trg"]), max(
                          x["src"], x["trg"])), axis=1)
        table_maxscore = table.groupby(by="edge")["score"].sum().reset_index()
        table = table.merge(table_maxscore, on="edge", suffixes=("_min", ""))
        table = table.drop_duplicates(subset=["edge"])
        table = table.drop("edge", 1)
        table = table.drop("score_min", 1)
        table["score"] = table["score"] / 2.0
    return table[["src", "trg", "nij", "score"]]


def maximum_spanning_tree(table, undirected=False):
    sys.stderr.write("Calculating MST score...\n")
    table = table.copy()
    table["distance"] = 1.0 / table["nij"]
    G = nx.from_pandas_edgelist(
        table,
        source="src",
        target="trg",
        edge_attr=[
            "distance",
            "nij"])
    T = nx.minimum_spanning_tree(G, weight="distance")
    table2 = nx.to_pandas_edgelist(T)
    table2 = table2[table2["nij"] > 0]
    table2.rename(
        columns={
            "source": "src",
            "target": "trg",
            "nij": "score"},
        inplace=True)
    table = table.merge(table2, on=["src", "trg"])
    if undirected:
        table["edge"] = table.apply(
            lambda x: "%s-%s" %
                      (min(
                          x["src"], x["trg"]), max(
                          x["src"], x["trg"])), axis=1)
        table = table.drop_duplicates(subset=["edge"])
        table = table.drop("edge", 1)
    return table[["src", "trg", "nij", "score"]]


def find_backbone(graph, threshold_value):
    edges = graph.edges(data=True)
    source = [edge[0] for edge in edges]
    target = [edge[1] for edge in edges]
    nij = [edge[2]['weight'] for edge in edges]
    table_data = pd.DataFrame({'src': source, 'trg': target, 'nij': nij})
    noise_corrected_table = noise_corrected(table_data)
    noise_corrected_backbone = thresholding(noise_corrected_table, threshold=threshold_value)
    noise_corrected_backbone_edges = [(edge[0], edge[1], {'weight': edge[2]}) for edge in
                                      noise_corrected_backbone.values]
    backbone_graph = nx.Graph()
    backbone_graph.add_edges_from(noise_corrected_backbone_edges)
    return {'graph': backbone_graph, 'backbone_result': noise_corrected_backbone}


def handle_find_backbone_result_show(graph, backbone_result, params, user_project_analysis_files_dir, limits={}):
    fore_end_graph_limit = limits.get('fore_end_graph_limit', 500)
    fore_end_table_limit = limits.get('fore_end_table_limit', 2000)
    nodes = list(graph.nodes())
    edges = graph.edges(data=True)
    sub_nodes = nodes[0:fore_end_graph_limit]
    sub_graph = graph.subgraph(sub_nodes)
    sub_edges = sub_graph.edges(data=True)
    tree_data = [
        {'title': '节点', 'key': 'nodes', 'children': [{'title': node, 'key': node} for node in sub_nodes]}]
    edges_data = [{"source": edge[0], "target": edge[1], "label": edge[2]['weight']} for edge in sub_edges]
    nodes_data = [{"id": node, "style": {"label": {
        "value": node,
        "position": 'top',
        "fill": '#000000',
        "fontSize": 16,
        "fontFamily": 'normal',
        "textAlign": 'center',
        "offset": 0,
    }}} for node in sub_nodes]
    graph_data = {"nodes": nodes_data, "edges": edges_data}
    tables_data = [{
        "table_name": "backbone",
        "table_chinese_name": "骨干网发现结果",
        "columns_type": [
            {"key": 'edges', "dataIndex": 'edges', "title": '相关边'},
            {"key": 'weight', "dataIndex": 'weight', "title": '边权重（出现次数）'},
            {"key": 'score', "dataIndex": 'score', "title": '评分'},
        ],
        "rows": [{'key': index, 'edges': str(edge[0]) + ' -- ' + str(edge[1]), 'weight': edge[2], 'score': edge[3]} for
                 (index, edge) in enumerate(backbone_result.values)][0:fore_end_table_limit]}]
    pdf_image = {'image_name': '骨干网图'}
    pdf_image['image_file_path'] = generate_image_from_graph(graph, pdf_image['image_name'],
                                                             user_project_analysis_files_dir)
    pdf_stories = [
        {'content_type': 'title', 'content': '骨干网络发现分析结果'},
        {'content_type': 'h1', 'content': '参数设置'},
        {'content_type': 'body',
         'content': '本次的参数设置为：阈值：' + str(params['threshold']) + '附带权重' if params[
                                                                              'weight'] == True else '本次的参数设置为：不附带权重'},
        {'content_type': 'h1', 'content': '分析结果'},
        {'content_type': 'h2', 'content': '骨干网节点'},
        {'content_type': 'body', 'content': '骨干网节点为' + ','.join(nodes)},
        {'content_type': 'h2', 'content': '网络图展示'},
        {'content_type': 'image', 'image_file_path': pdf_image['image_file_path'],
         'image_name': pdf_image['image_name'], 'width': 400, 'height': 300},
        {'content_type': 'page_break'}
    ]

    excel_sheets_data = [{'name': '骨干网发现结果', 'data': [('边节点1', '边节点2', '边相关权重（出现次数）', '评分')]}]
    for edge in backbone_result.values:
        excel_sheets_data[0]['data'].append((edge[0], edge[1], edge[2], edge[3]))
    return {"tree_data": tree_data, "graph_data": graph_data, "tables_data": tables_data,
            "raw_result_data": {"backbone_result": excel_sheets_data[0]['data']}, "pdf_stories": pdf_stories,
            "excel_sheets_data": excel_sheets_data}


def handle_find_backbone(data: list, params: dict, user_project_analysis_files_dir: str):
    rows = [row[0] for row in data]
    weight = params.get('weight', False)
    if weight:
        graph = rows_to_graph_with_weight(rows)
    else:
        graph = rows_to_graph(rows)
    threshold_value = params.get('threshold', 0.05)
    result = find_backbone(graph, threshold_value)
    return handle_find_backbone_result_show(result['graph'], result['backbone_result'], params,
                                            user_project_analysis_files_dir)

# if __name__ == '__main__':
#     handle_find_backbone([['蛇舌草,半枝莲,龙葵,石打穿,狗舌草,莪术,山慈菇,漏芦,肿节风,猫爪草,泽漆,土鳖虫,桃仁,蟾皮,砂仁'],
#                           ['败酱草,椿根白皮,墓头回,生薏苡仁,冬瓜子,苦参,泽泻,红藤,仙鹤草,失笑散,太子参,枸杞'],
#                           ['党参,焦白术,茯苓,炙甘草,太子参,麦冬,北沙参,仙鹤草,生薏苡仁,藤梨根,鸡血藤,泽漆,椿根白皮,夜交藤'],
#                           ['党参,焦白术,茯苓,炙甘草,太子参,麦冬,北沙参,石斛,仙鹤草,生薏苡仁'],
#                           ['法半夏,莱菔子,石斛,党参,焦白术,茯苓,炙甘草,太子参,麦冬,北沙参,仙鹤草,生薏苡仁,藤梨根']],
#                          params={'weight': True,'threshold':0.05},
#                          user_project_analysis_files_dir='D:\\Coding\\Python\\databaseAPI\\app\\users\\data\\1-user0\\2021-08-02-13-30-34--104-sa\\504-cliques方法分析结果')
