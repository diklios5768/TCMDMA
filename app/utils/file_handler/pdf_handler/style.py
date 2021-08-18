from reportlab.platypus.tableofcontents import delta
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle

cover_page_brackets = ParagraphStyle(name='cover_page_brackets', fontName='times', fontSize=108, textColor='grey', )
cover_page_header_chinese = ParagraphStyle(name='cover_page_header_chinese', fontName='simhei', fontSize=36,
                                           alignment=1, textColor='grey', )
cover_page_header_english = ParagraphStyle(name='cover_page_header_english', fontName='times', fontSize=26, alignment=1,
                                           textColor='grey', )
cover_page_footer_chinese = ParagraphStyle(name='cover_page_footer_chinese', fontName='simhei', fontSize=16,
                                           alignment=1, )
cover_page_footer_english = ParagraphStyle(name='cover_page_footer_english', fontName='times', fontSize=14,
                                           alignment=1, )

# 页眉和页脚
page_header = ParagraphStyle(name='page_header', fontName='simsun', fontSize=7.5)
page_footer = ParagraphStyle(name='page_footer', fontName='timesi', fontSize=10.5)
# 目录大标题的样式
table_of_content_title = ParagraphStyle(name='table_of_content_title',
                                        fontName='simsun',
                                        fontSize=30,
                                        leading=16,
                                        alignment=1,
                                        spaceAfter=20)

# 目录内使用的标题样式
toc_title = ParagraphStyle(
    name='TOCTitle',
    fontName='simsun',
    fontSize=12,
    leading=20,
    leftIndent=0 * delta
)
toc_h1 = ParagraphStyle(
    name='TOCHeading1',
    fontName='simsun',
    fontSize=12,
    leading=20,
    leftIndent=0.5 * delta
)
toc_h2 = ParagraphStyle(
    name='TOCHeading2',
    fontName='simsun',
    fontSize=12,
    leading=20,
    leftIndent=delta
)
toc_h3 = ParagraphStyle(
    name='TOCHeading3',
    fontName='simsun',
    fontSize=12,
    leading=20,
    leftIndent=1.5 * delta
)

# 正文使用的标题样式
# 一级标题要居中
title = ParagraphStyle(name='title',
                       fontName='simsunb',
                       fontSize=16,
                       leading=12,
                       alignment=TA_CENTER,
                       spaceBefore=10,
                       spaceAfter=30
                       )
h1 = ParagraphStyle(name='Heading1',
                    fontName='simsunb',
                    fontSize=14,
                    leading=12,
                    spaceBefore=10,
                    spaceAfter=10
                    )
h2 = ParagraphStyle(name='Heading2',
                    fontName='simsunb',
                    fontSize=13,
                    leading=11,
                    spaceBefore=10,
                    spaceAfter=10
                    )
h3 = ParagraphStyle(name='Heading3',
                    fontName='simsunb',
                    fontSize=12,
                    leading=10,
                    spaceBefore=10,
                    spaceAfter=10
                    )

# 图片和表格使用的居中样式
picture_table_center = ParagraphStyle(
    name='picture_table_center',
    fontName='simsun',
    fontSize=12,
    alignment=TA_CENTER,
    spaceBefore=10,
    spaceAfter=10,
    wordWrap='CJK')

# 正文样式
normal = ParagraphStyle(
    name='normal',
    fontName='simsun',
    fontSize=10,
    leading=20,
    # CJK用于中文分词换行
    wordWrap='CJK'
)
main_body = ParagraphStyle(
    name='main_body',
    fontName='simsun',
    fontSize=10,
    # 行距
    leading=20,
    # 首行缩进
    firstLineIndent=20,
    wordWrap='CJK'
)
table_body=ParagraphStyle(
    name='main_body',
    fontName='simsun',
    fontSize=10,
    leading=20,
    wordWrap='CJK'
)
# 红色标注的注释
red_main_body = ParagraphStyle(name='red_main_body',
                               fontName='simsun',
                               fontSize=10,
                               leading=20,
                               textColor='red',
                               firstLineIndent=20,
                               wordWrap='CJK')

main_body_list = ParagraphStyle(
    name='main_body_list',
    fontName='simsun',
    fontSize=10,
    leading=20,
    firstLineIndent=20,
    wordWrap='CJK'
)
