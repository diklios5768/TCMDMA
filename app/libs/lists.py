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

colors = [
    "#2ec7c9",
    "#b6a2de",
    "#5ab1ef",
    "#ffb980",
    "#d87a80",
    "#8d98b3",
    "#e5cf0d",
    "#97b552",
    "#95706d",
    "#dc69aa",
    "#07a2a4",
    "#9a7fd1",
    "#588dd5",
    "#f5994e",
    "#c05050",
    "#59678c",
    "#c9ab00",
    "#7eb00a",
    "#6f5553",
    "#c14089"]
colors_length = len(colors)

verification_use = ['register', 'login', 'modify password']

analysis_status = [
    'wait to start',
    'method error',
    'analysing',
    'analysis fail',
    'generating excel file',
    'generate excel file fail',
    'all completed']

analysis_methods = [
    {
        "name": "homogeneous",
        "chinese_name": "关联分析",
        "default_parameters": [
            {"name": "min_support", "type": "number", "step": 0.01,
             "default": 0.6, "chinese_name": "最小支持度"},
            {"name": "min_confidence", "type": "number", "step": 0.01, "default": 0.6, "chinese_name": "最小置信度"}],
        "simple_description": "关联分析是一种简单、实用的分析技术，就是发现存在于大量数据集中的关联性或相关性，从而描述了一个事物中某些属性同时出现的规律和模式。",
        "detail": """关联分析是从大量数据中发现项集之间有趣的关联和相关联系。关联分析的一个典型例子是购物篮分析。该过程通过发现顾客放入其购物篮中的不同商品之间的联系，分析顾客的购买习惯。通过了解哪些商品频繁地被顾客同时购买，这种关联的发现可以帮助零售商制定营销策略。其他的应用还包括价目表设计、商品促销、商品的排放和基于购买模式的顾客划分。
可从数据库中关联分析出形如“由于某些事件的发生而引起另外一些事件的发生”之类的规则。如“67%的顾客在购买啤酒的同时也会购买尿布”，因此通过合理的啤酒和尿布的货架摆放或捆绑销售可提高超市的服务质量和效益。又如“‘C语言’课程优秀的同学，在学习‘数据结构’时为优秀的可能性达88%”，那么就可以通过强化“C语言”的学习来提高教学效果。""",
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
        "simple_description": "社团结构是复杂网络普遍存在的拓扑特性之一，社团发现是利用图拓扑结构中所蕴藏的信息从复杂网络中解析出其模块化的社团结构，对于研究整个网络的模块、功能及其演化，具有十分重要的意义。",
        "detail": """网络是一种包含节点和边的集合，通常节点代表组成该系统的个体，边代表系统个体间的相互作用关系。相对而言，复杂网络具有节点多样性、结构复杂性、连接多样性以及网络中各种复杂性的相互影响。2002年，Girvan和 Newman等人发现复杂网络中存在一种新的结构——社团结构，其特征是同一社团内节点连接紧密，不同社团间连接稀疏。
        1.非重叠社团发现算法：非重叠社团发现是指识别出的社团之间互不重叠 ，每个节点有且仅属于一个社团。典型算法有模块度优化算法、谱分析法、信息论方法、标号传播方法等。基于模块度优化的社团发现算法是目前研究最多的一类算法， 其思想是将社团发现问题定义为优化问题， 然后搜索目标值最优的社团结构。2004年，Newman等人首次给出了模块度Q的定义，用以衡量社团划分结果的好坏。基于模块度优化的社团发现法通过优化目标函数Q使模块度最大化，从而得到最优的社团划分结果。2.重叠社团发现算法：早期的社团划分算法将网络划分为多个互不重叠的社团，认为每个节点只属于一个社团。而真实世界中这种硬划分并不能真正反应节点和社团的实际关系，例如蛋白质相互作用网络中由于蛋白质功能的多样性， 单个蛋白质在不同的时空条件下参与不同的功能模中。同样的现象普遍存在于各种真实网络之中 ，如社会网络中的人属于多个集体、网络中的网页属于多个主题等。因此，重叠社团发现更符合真实世界的社团组织规律，成为近几年社团发现研究的新热点，涌现出许多新颖算法。""",
        "description_image": "",
        "limits": {}
    }, {
        "name": "backbone",
        "chinese_name": "骨干网络",
        "default_parameters": [
            {"name": "threshold", "type": "number", "default": 0.05, "step": 0.01, "chinese_name": "阈值"},
            {"name": "weight", "type": "bool", "default": True, "chinese_name": "是否带权重"}],
        "simple_description": "复杂网络中重要节点的影响力度量是网络信息挖掘中的关键问题，少数的初始节点就能影响绝大部分节点，通过抽取网络骨干结构能够帮助我们更好地理解网络的结构",
        "detail": """现实生活中产生的数据往往呈现指数增长，海量数据的涌现使得我们必须要处理大量现实世界的复杂信息。复杂网络的节点和边的数量不断增加，这为复杂网络的研究、分析、可视化带来了不小的挑战。如何找到复杂网络中重要的、有影响力的组成部分，抽取出重要的核心骨干结构以简化网络有待解决。
与节点和边相比，骨干是网络中更高阶的组织结构，是复杂网络的基本构成单元。骨干结构在简化网络的同时又保留了网络的主体功能，帮助我们更好地理解网络的功能结构。
现有的网络骨干抽取方法主要由两类，一类是粗糙过滤，根据网络中节点或边的性质，定义一个全局阈值进行剪枝，仅保留权值超出阈值的节点和边得到骨干结构，如K-shell方法等。另一类方法是根据网络中局部的权重分布设置零假设，保留具有统计显著性的边，过滤掉不显著的边。
在寻找网络中重要节点的过程中需要选取评价标准。评价重要节点的标准具有多样性，不同的需求导致不同的评价标准。没有一个普适性的指标能完美地衡量出节点的重要性。常见的衡量节点重要性的方法大多基于网络的拓扑结构特性，如依赖网络中节点之间的路径信息、基于网络邻接矩阵的特征向量计算等。""",
        "description_image": "",
        "limits": {}
    }, {
        "name": "cliques",
        "chinese_name": "最大子网",
        "default_parameters": [{"name": "weight", "type": "bool", "default": True, "chinese_name": "是否带权重"}],
        "simple_description": "在无向图中查找最大团（Maximum Clique Problem, MCP），是图论中经典的组合优化问题，也是一类NP完全问题。国内对于MCP问题的研究还处于起步阶段",
        "detail": """复杂网络分析的一项重要任务就是揭示网络中的子结构,其中凝聚子群是一种典型的网络结构,完全连接的最大团结构就是紧密度最高的凝聚子群。寻找社团网络中的最大团是目前复杂网络分析的研究热点之一。
        通俗点讲就是在一个无向图中找出一个点数最多的完全图，即最大完全子图""",
        "description_image": "",
        "limits": {}
    }, {
        "name": "onion_layers",
        "chinese_name": "层次网络",
        "default_parameters": [{"name": "weight", "type": "bool", "default": True, "chinese_name": "是否带权重"}],
        "simple_description": "社团内节点层次结构探测在理解社团结构中具有重要意义。它反应了社团成员内部的关系以及节点在社团内的重要性。",
        "detail": """在社团内节点中，一些节点只具有该社团内节点的性质，其中一些节点在社团中发挥着重要作用。另外一些节点则由于本身度小、邻居节点度小、具有少部分其他社团性质等原因发挥的作用较小。社团中的每一个节点都有一个体现节点在社团归属程度的归属系数(belonging coefficients)。具有不同归属系数的节点处于社团的不同层次中，从而探测社团内部节点之间的层次结构关系。""",
        "description_image": "",
        "limits": {}
    }]
