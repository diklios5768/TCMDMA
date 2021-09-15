from reportlab.platypus import PageBreak, Table, Image, TableStyle, LongTable
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.platypus.paragraph import Paragraph
from reportlab.platypus.doctemplate import NextPageTemplate

from reportlab.lib.units import cm, inch
from reportlab.lib import colors
from app.utils.file_handler.pdf_handler.style import table_of_content_title, toc_title, toc_h1, toc_h2, toc_h3, \
    picture_table_center, title, h1, h2, h3, normal, main_body, \
    table_body, red_main_body, main_body_list
from app.settings import basedir


# 生成封面
def generate_cover_page(story):
    # 封面的下一页是有页眉的
    story.append(NextPageTemplate('page_with_header_template'))
    story.append(PageBreak())


# 生成目录
def generate_toc(story):
    # 目录标题
    table_content_title = Paragraph('<b>目录</b>', table_of_content_title)
    # 创建目录
    toc = TableOfContents(dotsMinLevel=0)
    # 设置目录样式
    toc.levelStyles = [
        toc_title,
        toc_h1,
        toc_h2,
        toc_h3
    ]
    # 插入标题
    story.append(table_content_title)
    # 插入目录具体内容
    story.append(toc)
    # 生成目录之后的页面是有页码的
    story.append(NextPageTemplate('page_with_header_and_footer_template'))
    # 目录生成之后一定要到下一页
    story.append(PageBreak())


# 插入标题的时候带书签,方便目录跳转
def generate_heading(story, text, style):
    from hashlib import sha1
    # create bookmarkname
    bn = text + style.name
    # modify paragraph text to include an anchor point with name bn
    h = Paragraph(text + '<a name="%s"/>' % bn, style)
    # store the bookmark name on the flowable so afterFlowable can see this
    h._bookmarkName = bn
    story.append(h)


# 插入正文
def generate_main_body(story, content):
    body = Paragraph(content, main_body)
    story.append(body)


def generate_red_main_body(story, content):
    body = Paragraph(content, red_main_body)
    story.append(body)


def generate_main_body_list(story, content):
    body = Paragraph(content, main_body_list)
    story.append(body)


# 一般表格
def generate_normal_table(story, data, table_name=None, table_num=1):
    col_num = len(data[0])
    data = [[Paragraph(str(cell), table_body) for cell in row] for row in data]
    table = Table(data, colWidths=14.64 * cm / col_num, style=TableStyle([
        # 所有边框设置为黑色
        ('FONTNAME', (0, 0), (-1, -1), 'simsun'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGNMENT', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
    ]), splitByRow=1)
    # table._argW[1] = 10 * cm
    if table_name is not None:
        table_heading = Paragraph(
            '表' + str(table_num) + ' ' + table_name,
            picture_table_center)
        # 插入表名
        story.append(table_heading)
    # 插入表格
    story.append(table)


# 生成三线表
def generate_three_line_table(story, data, table_name=None, table_num=1):
    """
    数据是二维表，第一行是表头
    """
    col_num = len(data[0])
    data = [[Paragraph(str(cell), table_body) for cell in row] for row in data]
    # 创建三线表样式
    table = Table(data, colWidths=14.64 * cm / col_num, style=[
        ('FONTNAME', (0, 0), (-1, 0), 'simsunb'),
        ('FONTNAME', (0, 1), (-1, -1), 'simsun'),
        ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
        ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
        # 设置居中
        ('ALIGNMENT', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ],
                  # 设置能够换页
                  splitByRow=1)
    if table_name is not None:
        table_heading = Paragraph(
            '表' + str(table_num) + ' ' + table_name,
            picture_table_center)
        # 插入表名
        story.append(table_heading)
    # 插入表格
    story.append(table)


def generate_three_line_table_two_col(story, data, table_name=None, table_num=1):
    col_num = len(data[0])
    first_line = int(col_num / 2)
    data = [[Paragraph(str(cell), table_body) for cell in row] for row in data]
    # 创建三线表样式
    table = Table(data, colWidths=14.64 * cm / col_num, style=[
        ('LINEBEFORE', (first_line, 0), (first_line, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'simsunb'),
        ('FONTNAME', (0, 1), (-1, -1), 'simsun'),
        ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
        ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
        # 设置居中
        ('ALIGNMENT', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ], splitByRow=1)
    if table_name is not None:
        table_heading = Paragraph(
            '表' + str(table_num) + ' ' + table_name,
            picture_table_center)
        # 插入表名
        story.append(table_heading)
    # 插入表格
    story.append(table)


def generate_three_line_table_three_col(story, data, table_name=None, table_num=1):
    col_num = len(data[0])
    first_line = int(col_num / 3)
    second_line = int(first_line * 2)
    data = [[Paragraph(str(cell), table_body) for cell in row] for row in data]
    # 创建三线表样式
    table = Table(data, colWidths=14.64 * cm / col_num, style=[
        ('LINEBEFORE', (first_line, 0), (first_line, -1), 1, colors.black),
        ('LINEBEFORE', (second_line, 0), (second_line, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'simsunb'),
        ('FONTNAME', (0, 1), (-1, -1), 'simsun'),
        ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
        ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
        # 设置居中
        ('ALIGNMENT', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ], splitByRow=1)
    if table_name is not None:
        table_heading = Paragraph(
            '表' + str(table_num) + ' ' + table_name,
            picture_table_center)
        # 插入表名
        story.append(table_heading)
    # 插入表格
    story.append(table)


# 生成图片
def generate_image(story, image_path, image_name, width=None, height=None, picture_num=1):
    """
    注意：image_path是完整的路径，并非去掉文件名称的路径
    """
    image = Image(filename=image_path, width=width, height=height)
    image.vAlign = 'MIDDLE'
    image.hAlign = 'CENTER'
    image_heading = Paragraph(
        '图' + str(picture_num) + ' ' + image_name,
        picture_table_center)
    # 插入图片
    story.append(image)
    # 插入图名，图名在图下面，和表不一样
    story.append(image_heading)


def generate_test_story():
    # 创建内容文件
    story = []
    # 创建封面
    generate_cover_page(story)
    # 创建目录
    generate_toc(story)

    # 开始输入报告正文内容
    # 数据挖掘研究基本信息
    generate_heading(story, '数据挖掘研究基本信息', title)
    generate_normal_table(story, [['项目名称', '乳腺癌方药配伍规'],
                                  ['挖掘目的', '方药配伍'],
                                  ['数据集', '乳腺癌方药 177 例'],
                                  ['研究范围',
                                   Paragraph('综合利用 Fp-Growth、Complex Network 等方法分析数据，探索吴门医派医家治疗便秘的用药特点。', normal)],
                                  ['数据数量', '177 例（其中内服方 136 例，外用方 41 例）'],
                                  ['挖掘周期', '2017 年 10 月 29 日——201'],
                                  ['挖掘系统',
                                   'SPSS 18.0 统计软件\nXMiner V2.4 中医药数据关联分析平台\nLiquorice V3.0 复杂网络分析平台\nPython SciPy & MatplotPy'''],
                                  ['建模类型', 'Fp-Growth 模型；Complex Network 模型'],
                                  ['算法类型',
                                   Paragraph('Fp-Growth; Hierarchical Network; Multiscale backbone Network', normal)],
                                  ['数据分析', '屈丹丹、赵状、王一帆'],
                                  ['工程审核', '包钦睿、毛美清'],
                                  ['指导老师', '杨涛'],
                                  ['工作团队', '南京中医药大学信息技术学院医学信息创新工作室']
                                  ])
    story.append(PageBreak())
    # 中英文对照表
    generate_heading(story, '中英文对照表', title)
    generate_three_line_table(story, [['英文缩写', '英文全称', '中文全称'],
                                      ['Fp-Growth', 'Fp-Tree Growth', 'Algorithm 频繁模式树生长算法'],
                                      ['Complex Network', 'Complex Network', '复杂网络'],
                                      ['minSup', 'Minimal Support', 'Rate 最小支持度'],
                                      ['minConf', 'Minimal Confidence', 'Rate 最小置信度'],
                                      ['Multiscale', 'networks Multiscale', 'networks 多尺度网络'],
                                      ['Hierarchical backbone', 'Hierarchical backbone', '层次骨干网'],
                                      ['Layer Num', 'Layer Numer', '层次数目'],
                                      ['Degree', 'Degree', '节点度'],
                                      ['Already', 'Prescriptions Already', 'Prescriptions 附方'],
                                      ['Ass.', 'Association', '关联'],
                                      ['Clustering Analysis', 'Clustering Analysis', '聚类分析'],
                                      ['Confidence', 'Confidence', '置信度'],
                                      ['Distribution', 'Distribution', '分布'],
                                      ['External Association Rule', 'External Association Rule', '外关联规则'],
                                      ['Fre.', 'Frequency', '频率'],
                                      ['Internal Association Rule', 'Internal Association Rule', '内关联规则'],
                                      ['K-means Clustering Analysis', 'K-means Clustering Analysis', 'K-均值聚类分析'],
                                      ['Original Words', 'Original Words', '原生词'],
                                      ['Principle of Treatment', 'Principle of Treatment', '治则治法'],
                                      ['Pulse Condition', 'Pulse Condition', '脉象'],
                                      ['Qua.', 'Quantity', '频次'], ['Se.', 'Sequence', '序列'],
                                      ['Site Web', 'Site Web', '位点结构'],
                                      ['Sta.', 'Standard', '规范对照'],
                                      ['Standard Words', 'Standard Words', '规范词'], ['Support', 'Support', '支持度'],
                                      ['System Clustering Analysis', 'System Clustering Analysis',
                                       '系统聚类分析'],
                                      ['TCM Diagnosis', 'Tradition Chinese Medicine Diagnosis', '中医疾病诊断'],
                                      ['TCM Syndrome Diagnosis', 'Tradition Chinese Medicine Syndrome Diagnosis',
                                       '中医证候诊断'],
                                      ['Western Medicine Diagnosis', 'Western Medicine Diagnosis', '西医疾病诊断']
                                      ])
    story.append(PageBreak())
    generate_heading(story, '1 研究目的', h1)
    generate_main_body(story, '乳腺癌方药配伍规律研究')
    generate_heading(story, '2 研究方法', h1)
    generate_heading(story, '2.1 医案资料来源', h2)
    generate_main_body(story,
                       '数据来自《外科全生集》、《饲鹤亭集方》、《医方简义》、' +
                       '《外科正宗》、《金鉴》、《全国中药成药处方集》、《疡医大全》、《圣济总录》、' +
                       '《喉科心法》、《医门补要》、《医林纂要》、《外科大成》、《外科集腋》、《医部全录》、' +
                       '《千金》、《药庵医学丛书·论 医集》、《集验良方》、《内外科百病验方大全》、《理瀹》、' +
                       '《青囊秘诀》、《医门八法》、《顾氏医径》、《惠直堂方》、方出《奇方类编》、《古方汇精》、' +
                       '《揣摩有得集》、《扁鹊心书·神方》、《马培之医案》、《竹林女科》、《医事启源》、《疡科选粹》、' +
                       '《简明中医妇科学》、《疡科心得集·方汇补遗》、《仙拈集》、《玉机微义》、《外台》等。由指导老师提供。')
    generate_heading(story, '2.2 医案的预处理', h2)
    generate_main_body(story, '对原始数据进行预处理，分为“内服方剂”136 例、“外用方剂”41 例，处理过程如下：')
    list1 = ['（1） 删 除 药 物 的 非 法 字 符 ， 如 空 格 、 制 表 符 等 ， 其 中 空 格 178 个 ， 制 表 符 共 154个 ；',
             '（2）补全药物名称。内服方第 85 条记录有两个“公英”，删除 1 各，且将“公英”补充为“蒲公英”；\n',
             '（3）删除冗余信息。内服方第 55 条记录，“炙僵蚕三”改为“炙僵蚕”；\n',
             '（4）删除数字，如内服方第 48 条“海藻 1”改为“海藻”，72 条“丹参桃仁 1”拆分为“丹参”、“桃仁”，“甘草 1”改为“甘草”；78 条“天龙 3g”改为“天龙”；\n',
             '（5）删除括号等字符，如 88 条、90 条删除“先煎”，93 条“天麦东（各）”改为“天门冬、麦门冬”；\n',
             '（6）内服方剂 56 条，“川楝子各”修改为“川楝子”；57 条“莪术各”修改为“莪术”；85 条“陈皮各”修改为“陈皮”；86 条“牡蛎各”修改为“生牡蛎”；\n',
             '（7）名称统一，“天冬”统一为“天门冬”；\n',
             '（8）药物拆分，内服方第 96 条“茜草根白芥子茯苓”改为“茜草根、白芥子、茯苓”；\n',
             '（9）内服方第 128 条，“当归）”改为“当归”。']
    for i in list1:
        generate_main_body_list(story, i)

    generate_red_main_body(story, '详见“1 数据清洗：乳腺癌数据库数据收录.xlsx”中的“清洗说明”Sheet。')
    generate_heading(story, '2.3 数据分析过程', h2)
    generate_heading(story, '2.3.1 数据格式处理', h3)
    generate_main_body(story, '对“药物组成”字段进行分析，将数据转化为分析平台要求的矩阵格式。' +
                       '详见“1 数据清洗：乳腺癌数据库数据收录.xlsx”中的“内服方格式化”、“外用方格式化”的相关 sheet。')
    generate_heading(story, '2.3.2 医案信息数据挖掘方法', h3)
    generate_main_body(story,
                       '本次数据研究方法采用 Python SciPy & Matplotlib 编程实现数据整理和格式化；采用XMiner ' +
                       '进行 Fp-Growth 算法建模，进行方药数据关联分析；采用 Liquorice 进行 Complex Network 建模，进行网络分析。')
    generate_heading(story, '3 研究结果', h1)
    generate_heading(story, '3.1 描述性统计结果', h2)
    generate_heading(story, '3.1.1 内服方药物频次分布', h3)
    generate_three_line_table_two_col(story, [
        ['编号', '项集', '支持度数', '支持度', '编号', '项集', '支持度数', '支持度'],
        ['1', '白芍,当归', '22', '0.1618', '11', '人参,当归', '13', '0.0956'],
        ['2', '白术,茯苓', '19', '0.1397', '12', '肉苁蓉,莪术', '13', '0.0956'],
        ['3', '川芎,当归', '18', '0.1324', '13', '白术,当归', '13', '0.0956'],
        ['4', '甘草,当归', '18', '0.1324', '14', '淫羊藿,山茱萸', '12', '0.0882'],
        ['5', '黄芪,当归', '17', '0.125', '15', '山茱萸,白术', '12', '0.0882'],
        ['6', '茯苓,当归', '16', '0.1176', '16', '山茱萸,莪术', '12', '0.0882'],
        ['7', '肉苁蓉,淫羊藿', '14', '0.1029', '17', '白芷,当归', '12', '0.0882'],
        ['8', '淫羊藿,莪术', '14', '0.1029', '18', '肉苁蓉,山茱萸', '11', '0.0809'],
        ['9', '党参,茯苓', '14', '0.1029', '19', '柴胡,当归', '11', '0.0809'],
        ['10', '没药,乳香', '13', '0.0956', '20', '夏枯草,当归', '11', '0.0809']]
                                      , table_name='内服方药物二项频繁集（前 20 条）')
    generate_red_main_body(story, '注：详见“2 内服方-药物频次：乳腺癌数据库数据收录.xlsx”。')
    generate_heading(story, '3.1.2 外用方药物频次分布', h3)
    generate_three_line_table_three_col(story,
                                        [['药物', '频次', '药物', '频次', '药物', '频次'], ['当归', '69', '蒲公英', '19', '山慈菇', '14'],
                                         ['甘草', '33', '白芷', '18', '肉苁蓉', '14'], ['茯苓', '30', '莪术', '18', '生甘草', '13'],
                                         ['白芍', '29', '青皮', '16', '金银花', '13'], ['白术', '25', '乳香', '16', '没药', '13'],
                                         ['党参', '24', '山茱萸', '16', '生黄芪', '13'], ['黄芪', '23', '陈皮', '16', '连翘', '12'],
                                         ['川芎', '22', '川贝母', '16', '香附', '12'], ['夏枯草', '21', '淫羊藿', '15', '漏芦', '12'],
                                         ['柴胡', '19', '人参', '14', '麝香', '11']]
                                        , table_name='内服方药物频次分布（前 30 味）')
    generate_heading(story, '3.2.3 内服方依赖关系网络', h3)
    generate_image(story, basedir + '/utils/file_handler/pdf_handler/reference/1.png',
                   '依赖关系网络（minSup=0.04，minConf=0.9）', 12 * cm, 8 * cm)
    return story


def generate_report_story(stories: list = []):
    # 创建内容文件
    story = []
    # 创建封面
    generate_cover_page(story)
    # 创建目录
    generate_toc(story)
    if not isinstance(stories, list):
        generate_red_main_body(story, 'PDF内容错误')
        return story
    # 标题序号
    head1_count = 1
    head2_count = 1
    head3_count = 1
    # 图表当前数量
    picture_num = 1
    # 表格当前数量
    table_num = 1
    for each_story in stories:
        content_type = each_story['content_type']
        if content_type == 'title':
            generate_heading(story, each_story['content'], title)
        elif content_type == 'h1':
            generate_heading(story, str(head1_count) + '.' + each_story['content'], h1)
            head1_count += 1
            head2_count = 1
            head3_count = 1
        elif content_type == 'h2':
            generate_heading(story, str(head1_count - 1) + '.' + str(head2_count) + each_story['content'], h2)
            head2_count += 1
            head3_count = 1
        elif content_type == 'h3':
            generate_heading(story,
                             str(head1_count - 1) + '.' + str(head2_count - 1) + '.' + str(head3_count) + each_story[
                                 'content'],
                             h3)
            head3_count += 1
        elif content_type == 'body':
            generate_main_body(story, each_story['content'])
        elif content_type == 'attention':
            generate_red_main_body(story, each_story['content'])
        elif content_type == 'normal_table':
            generate_normal_table(story, each_story['content'], table_name=each_story['table_name'],
                                  table_num=table_num)
            table_num += 1
        elif content_type == 'three_line_table':
            generate_three_line_table(story, each_story['content'], table_name=each_story['table_name'],
                                      table_num=table_num)
            table_num += 1
        elif content_type == 'three_line_table_two_col':
            generate_three_line_table_two_col(story, each_story['content'], table_name=each_story['table_name'],
                                              table_num=table_num)
            table_num += 1
        elif content_type == 'three_line_table_three_col':
            generate_three_line_table_three_col(story, each_story['content'], table_name=each_story['table_name'],
                                                table_num=table_num)
            table_num += 1
        elif content_type == 'image':
            generate_image(story, each_story['image_file_path'], each_story['image_name'],
                           width=each_story.get('width', 12 * cm),
                           height=each_story.get('height', 8 * cm), picture_num=picture_num)
            picture_num += 1
        elif content_type == 'page_break':
            story.append(PageBreak())
        else:
            break
    return story
