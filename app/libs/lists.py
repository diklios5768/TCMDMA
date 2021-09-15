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
        "chinese_name": "关联分析",
        "default_parameters": [
            {"name": "min_support", "type": "number", "step": 0.01, "default": 0.5, "chinese_name": "最小支持度"},
            {"name": "min_confidence", "type": "number", "step": 0.01, "default": 0.5, "chinese_name": "最小置信度"}],
        "simple_description": "关联分析是一种简单、实用的分析技术，就是发现存在于大量数据集中的关联性或相关性，从而描述了一个事物中某些属性同时出现的规律和模式。",
        "detail": """关联分析是一种简单、实用的分析技术，就是发现存在于大量数据集中的关联性或相关性，从而描述了一个事物中某些属性同时出现的规律和模式。
关联分析是从大量数据中发现项集之间有趣的关联和相关联系。关联分析的一个典型例子是购物篮分析。该过程通过发现顾客放入其购物篮中的不同商品之间的联系，分析顾客的购买习惯。通过了解哪些商品频繁地被顾客同时购买，这种关联的发现可以帮助零售商制定营销策略。其他的应用还包括价目表设计、商品促销、商品的排放和基于购买模式的顾客划分。
可从数据库中关联分析出形如“由于某些事件的发生而引起另外一些事件的发生”之类的规则。如“67%的顾客在购买啤酒的同时也会购买尿布”，因此通过合理的啤酒和尿布的货架摆放或捆绑销售可提高超市的服务质量和效益。又如“‘C语言’课程优秀的同学，在学习‘数据结构’时为优秀的可能性达88%”，那么就可以通过强化“C语言”的学习来提高教学效果。
""",
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
        "chinese_name": "社团发现",
        "default_parameters": [{"name": "weight", "type": "bool", "default": True, "chinese_name": "是否带权重"}],
        "simple_description": "有效地检测复杂网络中的社团结构（即稠密的模块结构）的一类方法。",
        "detail": "一般意义上讲，一个社团也可以被称为群、聚类或模块，是网络中一群阶段或边的集合，其内部的节点间连接较为紧密，而社团间的连接却相对稀疏。",
        "description_image": "",
        "limits": {}
    }, {
        "name": "backbone",
        "chinese_name": "骨干网络",
        "default_parameters": [
            {"name": "threshold", "type": "number", "default": 0.05, "step": 0.01, "chinese_name": "阈值"},
            {"name": "weight", "type": "bool", "default": True, "chinese_name": "是否带权重"}],
        "simple_description": "骨干网络是网络中最核心的节点集合",
        "detail": "",
        "description_image": "",
        "limits": {}
    }, {
        "name": "cliques",
        "chinese_name": "最大子网",
        "default_parameters": [{"name": "weight", "type": "bool", "default": True, "chinese_name": "是否带权重"}],
        "simple_description": "最大子网是复杂网络中最大的社团",
        "detail": "",
        "description_image": "",
        "limits": {}
    }, {
        "name": "onion_layers",
        "chinese_name": "层次网络",
        "default_parameters": [{"name": "weight", "type": "bool", "default": True, "chinese_name": "是否带权重"}],
        "simple_description": "复杂网络中的层次结构，复杂网络中的社团结构往往具有层次性",
        "detail": "",
        "description_image": "",
        "limits": {}
    }]
