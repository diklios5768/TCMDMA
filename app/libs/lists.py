# -*- encoding: utf-8 -*-
"""
@File Name      :   lists.py    
@Create Time    :   2021/7/14 9:42
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

colors = ["#2ec7c9", "#b6a2de", "#5ab1ef", "#ffb980", "#d87a80", "#8d98b3",
          "#e5cf0d", "#97b552", "#95706d", "#dc69aa", "#07a2a4", "#9a7fd1", "#588dd5",
          "#f5994e", "#c05050", "#59678c", "#c9ab00", "#7eb00a", "#6f5553", "#c14089"]
colors_length = len(colors)

verification_use = ['register', 'login', 'modify password']

analysis_status = ['wait to start', 'method error', 'analysing', 'analysis fail', 'generating excel file',
                   'generate excel file fail', 'all completed']

analysis_methods = [
    {
        "name": "homogeneous",
        "chinese_name": "同质关联分析",
        "default_parameters": [
            {"name": "min_support", "type": "number", "step": 0.01, "default": 0.5, "chinese_name": "最小支持度"},
            {"name": "min_confidence", "type": "number", "step": 0.01, "default": 0.5, "chinese_name": "最小置信度"}],
        "simple_description": "",
        "detail": "",
        "description_image": "",
        "limits": {}
    },
    # {
    #     "name": "heterogeneous",
    #     "chinese_name": "异质关联分析",
    #     "default_parameters": [
    #         {"name": "min_support", "type": "number", "step": 0.01, "default": 0.5, "chinese_name": "最小支持度"},
    #         {"name": "min_confidence", "type": "number", "step": 0.01, "default": 0.5, "chinese_name": "最小置信度"}],
    #     "simple_description": "",
    #     "detail": "",
    #     "description_image": "",
    #     "limits": {}
    # },
    {
        "name": "louvain",
        "chinese_name": "louvain社团发现算法",
        "default_parameters": [{"name": "weight", "type": "bool", "default": True, "chinese_name": "是否带权重"}],
        "simple_description": "",
        "detail": "",
        "description_image": "",
        "limits": {}
    }, {
        "name": "backbone",
        "chinese_name": "骨干网发现算法",
        "default_parameters": [
            {"name": "threshold", "type": "number", "default": 0.05, "step": 0.01, "chinese_name": "阈值"},
            {"name": "weight", "type": "bool", "default": True, "chinese_name": "是否带权重"}],
        "simple_description": "",
        "detail": "",
        "description_image": "",
        "limits": {}
    }, {
        "name": "cliques",
        "chinese_name": "cliques社团发现算法",
        "default_parameters": [{"name": "weight", "type": "bool", "default": True, "chinese_name": "是否带权重"}],
        "simple_description": "",
        "detail": "",
        "description_image": "",
        "limits": {}
    }, {
        "name": "onion_layers",
        "chinese_name": "洋葱皮社团发现算法",
        "default_parameters": [{"name": "weight", "type": "bool", "default": True, "chinese_name": "是否带权重"}],
        "simple_description": "",
        "detail": "",
        "description_image": "",
        "limits": {}
    }]
