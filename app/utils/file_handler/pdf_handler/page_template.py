from reportlab.platypus import PageTemplate, Paragraph, Image
from reportlab.lib.units import cm
from app.utils.file_handler.pdf_handler.style import page_header, page_footer, cover_page_brackets, \
    cover_page_header_chinese, cover_page_header_english, cover_page_footer_chinese, \
    cover_page_footer_english
from functools import partial  # 当header和footer有额外参数的时候可以使用
from app.settings import basedir


def header(canvas, doc):
    """
    设置页眉
    :param canvas:Canvas类型  pdf画布
    :param doc:doc类型     整个pdf文件
    """
    canvas.saveState()
    # 插入页眉图片
    # p = Paragraph("<img src='%s' width='%d' height='%d'/>" % (img_address, header_img_width, header_img_height),
    #               normal)  # 使用一个Paragraph Flowable存放图片
    # w, h = p.wrap(doc.width, doc.bottomMargin)
    # p.drawOn(canvas, doc.leftMargin, doc.topMargin + doc.height - 0.5 * cm)
    # # 放置图片

    # 插入页眉内容
    space = ''
    for i in range(20):
        space += '&nbsp;&nbsp;&nbsp;'
    p = Paragraph("中医药数据挖掘分析报告 V1.0 " + space + "医学信息创新工作室", page_header)
    w, h = p.wrap(doc.width, doc.bottomMargin)
    p.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h + 1 * cm)
    canvas.line(
        doc.leftMargin,
        doc.bottomMargin +
        doc.height +
        0.5 *
        cm,
        doc.leftMargin +
        doc.width,
        doc.bottomMargin +
        doc.height +
        0.5 *
        cm)  # 画一条横线
    canvas.restoreState()


def footer(canvas, doc):
    """
    设置页脚
    :param canvas:Canvas类型  pdf画布
    :param doc:doc类型   整个pdf文件
    """
    canvas.saveState()  # 先保存当前的画布状态
    page_number = ("%s" % canvas.getPageNumber())  # 获取当前的页码
    p = Paragraph(page_number, page_footer)

    # 指定一个地点
    # w, h = p.wrap(1 * cm, 1 * cm)  # 申请一块1cm大小的空间，返回值是实际使用的空间
    # p.drawOn(canvas, foot_coordinate_x, foot_coordinate_y)  # 将页码放在指示坐标处
    # 指定页脚位置
    # 整个下方区域
    w, h = p.wrap(doc.width, doc.bottomMargin)
    p.drawOn(canvas, doc.width + doc.leftMargin, h)
    canvas.restoreState()


def cover_page_footer(canvas, doc):
    canvas.saveState()  # 先保存当前的画布状态
    brackets_left = Paragraph('[', cover_page_brackets)
    brackets_left_w, brackets_left_h = brackets_left.wrap(doc.width, doc.bottomMargin)
    brackets_left.drawOn(canvas, doc.leftMargin + 0.5 * cm, doc.bottomMargin + doc.height - 1.8 * cm)
    brackets_right = Paragraph(']', cover_page_brackets)
    brackets_right_w, brackets_right_h = brackets_right.wrap(doc.width, doc.bottomMargin)
    brackets_right.drawOn(canvas, doc.leftMargin + doc.width - 1.5 * cm, doc.bottomMargin + doc.height - 1.8 * cm)
    header_chinese = Paragraph('数据挖掘分析报告', cover_page_header_chinese)
    header_chinese_w, header_chinese_h = header_chinese.wrap(doc.width, doc.bottomMargin)
    header_chinese.drawOn(canvas, doc.leftMargin, doc.bottomMargin + doc.height - 3 * cm)
    header_english = Paragraph('DATA MINING REPORT', cover_page_header_english)
    header_english_w, header_english_h = header_english.wrap(doc.width, doc.bottomMargin)
    header_english.drawOn(canvas, doc.leftMargin, doc.bottomMargin + doc.height - 5 * cm)

    image = Image(basedir + r'/utils/file_handler/pdf_handler/reference/cover_page.png', 268, 270)
    image.drawOn(canvas, doc.leftMargin + 2.5 * cm, doc.bottomMargin + 5 * cm)

    footer_chinese = Paragraph('南京中医药大学信息技术学院医学信息创新工作室', cover_page_footer_chinese)
    footer_chinese_w, footer_chinese_h = footer_chinese.wrap(doc.width, doc.bottomMargin)
    footer_chinese.drawOn(canvas, doc.leftMargin, doc.bottomMargin + 1 * cm + footer_chinese_h)
    canvas.line(
        doc.leftMargin,
        doc.bottomMargin + 1 * cm,
        doc.leftMargin +
        doc.width,
        doc.bottomMargin + 1 * cm)  # 画一条横线
    footer_english = Paragraph('MEDICAL  INFORMATICS INNOVATION STUDIO IN INSTITUTE OF  INFORMATION & TECHNOLOGY',
                               cover_page_footer_english)
    footer_english_w, footer_english_h = footer_english.wrap(doc.width, doc.bottomMargin)
    footer_english.drawOn(canvas, doc.leftMargin, doc.bottomMargin + 1 * cm - footer_english_h)
    canvas.restoreState()


def cover_page_template(frame):
    template = PageTemplate(
        id='cover_page_template',
        frames=frame,
        onPage=cover_page_footer)
    return template


def page_with_header_template(frame):
    template = PageTemplate(
        id='page_with_header_template',
        frames=frame,
        onPage=header)
    return template


def page_with_header_and_footer_template(frame):
    template = PageTemplate(
        id='page_with_header_and_footer_template',
        frames=frame,
        onPage=header,
        onPageEnd=footer)
    return template
