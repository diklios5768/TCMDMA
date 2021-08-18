from fpdf import FPDF, TitleStyle
from app.settings import basedir

# 设置全局变量
SYSTEM_TTFONTS = r'C:/WINDOWS/Fonts/'
FPDF_FONT_DIR = basedir + r'/static/fonts/'
FPDF_CACHE_DIR = basedir + r'/static/fonts/cache'


class PDF(FPDF):
    """
    orientation(方向):portrait(竖向)或者landscape(横向)
    unit(单元单位):pt(点，1/72 inch),mm(毫米),cm(厘米),in(英寸)
    format(纸张):a3, a4, a5, letter, legal,给定的元组，其中常用的A4纸为 210*297mm
    font_cache_dir(字体文件缓存目录)
    """

    def __init__(self, orientation="portrait", unit="mm", formation="A4",
                 font_cache_dir=FPDF_CACHE_DIR):
        super().__init__(orientation=orientation, unit=unit, format=formation, font_cache_dir=font_cache_dir)

    # def header(self):
    # Logo
    # self.image('logo_pb.png', 10, 8, 33)
    # # helvetica bold 15
    # self.set_font('helvetica', 'B', 15)
    # # Move to the right
    # self.cell(80)
    # # Title
    # self.cell(30, 10, 'Title', 1, 0, 'C')
    # Line break
    # self.ln(20)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # helvetica italic 8
        self.set_font('helvetica', 'I', 8)
        # Page number
        # self.cell(0, 10, 'Page ' + str(self.page_no() + 1) + '/{nb}', 0, 0, 'R')
        self.cell(0, 10, str(self.page_no() + 1), 0, 0, 'R')


# 添加段落
def p(pdf, text, **kwargs):
    pdf.set_font('song_ti', '', 10)
    pdf.set_x(20)
    pdf.multi_cell(w=pdf.epw, h=pdf.font_size, txt=text, ln=1, **kwargs)
    return pdf


# 初始化PDF
def init_pdf(font_list=[{'name': 'hei_ti', 'file_path': SYSTEM_TTFONTS + r'simhei.ttf'},
                        {'name': 'song_ti', 'file_path': SYSTEM_TTFONTS + r'simfang.ttf'},
                        {'name': 'kai_ti', 'file_path': SYSTEM_TTFONTS + r'simkai.ttf'},
                        {'name': 'ms_ya_hei', 'file_path': FPDF_FONT_DIR + r'msyh.ttf'},
                        {'name': 'li_shu', 'file_path': FPDF_FONT_DIR + r'simli.ttf'},
                        ]):
    """
    :font_list:列表，每一个元素是一个字典，字典格式:{'font_name':str,'font_path':str}
    """
    # 设置纸张
    pdf = PDF()
    pdf.set_doc_option('core_fonts_encoding', 'latin-1')
    # 添加中文字体
    for font in font_list:
        pdf.add_font(font['name'], '', font['file_path'], uni=True)
        pdf.add_font(font['name'], 'B', font['file_path'], uni=True)
        pdf.add_font(font['name'], 'I', font['file_path'], uni=True)
    # 设置边距
    pdf.set_margin(10)
    # 添加封面
    # 注意：添加页面后，焦点自动聚焦到(10,10)的位置
    pdf.add_page()

    # 设置标题字体
    pdf.set_section_title_styles(
        # Level 0 titles:
        TitleStyle(
            font_family="song_ti",
            font_style="B",
            font_size_pt=24,
            color=128,
            underline=True,
            t_margin=10,
            l_margin=10,
            b_margin=0,
        ),
        # Level 1 subtitles:
        TitleStyle(
            font_family="song_ti",
            font_style="B",
            font_size_pt=20,
            color=128,
            underline=True,
            t_margin=10,
            l_margin=20,
            b_margin=5,
        ),
    )

    # 添加目录
    pdf.insert_toc_placeholder(insert_directory)
    # 初始使用字体，注意这个size是point的尺寸，即0.35mm，而且字体是有上下边距的，包括在了size里面，所以实际上尺寸更小
    pdf.set_font('', size=24)

    return pdf


# pylint: disable=unused-argument
def insert_directory(pdf, outline):
    pdf.y += 0
    pdf.x = 20
    pdf.set_font("song_ti", "B", size=16)
    pdf.underline = True
    pdf.cell(0, 20, '目录', 0, 1, 'L')
    pdf.underline = False
    pdf.y += 10
    pdf.set_font("song_ti", "B", size=12)
    for section in outline:
        link = pdf.add_link()
        pdf.set_link(link, page=section.page_number)
        text = f'{" " * section.level * 2} {section.name}'
        text += (
            f' {"." * (60 - section.level * 2 - len(section.name))} {section.page_number}'
        )
        pdf.multi_cell(w=pdf.epw, h=pdf.font_size, txt=text, ln=1, align="C", link=link)


# 添加标题
def insert_title(pdf, title, level):
    pdf.start_section(name=title, level=level)
    return pdf


# 插入图片
def insert_picture(pdf, img_path, title, x=0, y=0, width=0, height=0, img_description=''):
    """
    :x:距离左边的距离
    :y:距离上面的距离

    """
    pdf.image(img_path, x=x, y=y, w=width, h=height, title=title, alt_text=img_description)
    return pdf


# 插入表格
def insert_table(pdf, table_data):
    """
    table_data:列表，每一个元素的一个元组，第一个元组是列名，后面的元组是行数据
    """
    pdf.set_font('hei_ti', '', 10)
    line_height = pdf.font_size * 2.5
    col_width = pdf.epw / 4  # distribute content evenly
    for row in table_data:
        for datum in row:
            pdf.multi_cell(col_width, line_height, datum, border=1, ln=3, max_line_height=pdf.font_size, align='C')
        pdf.ln(line_height)
    return pdf


def generate_pdf(pdf, name):
    pdf.output(basedir + '/static/pdf/' + name)


def generate_relation_analysis_report(tables, name='relation_analysis_report.pdf'):
    pdf = init_pdf()

    # 添加频次表
    pdf = insert_title(pdf, title='频次分析结果', level=0)
    pdf.y += 10
    p(pdf, '频次表只显示前20条最高频次的数据，更加详细的结果请查看频次结果表。')
    pdf.y += 10
    pdf = insert_table(pdf, table_data=tables[0])
    pdf.add_page()
    # 添加频繁项集表
    pdf = insert_title(pdf, title='频繁项集分析结果', level=0)
    pdf.y += 10
    p(pdf, '频繁项集表只显示前20条频繁程度最高的数据，更加详细的结果请查看频繁项集结果表。')
    pdf.y += 10
    pdf = insert_table(pdf, table_data=tables[1])
    pdf.add_page()
    # 添加关联规则表
    pdf = insert_title(pdf, title='关联规则分析结果', level=0)
    pdf.y += 10
    p(pdf, '关联规则表只显示前20条提升程度最高的数据，更加详细的结果请查看关联规则结果表。')
    pdf.y += 10
    pdf = insert_table(pdf, table_data=tables[2])
    pdf.add_page()
    # 添加网络图
    pdf = insert_title(pdf, title='网络图分析结果', level=0)
    pdf.y += 10
    p(pdf, '网络表根据关联规则只显示前20个关联程度最高的的数据，更加详细的操作请在网页部分查看，或者查看网络图JSON数据文件。')
    pdf.y += 10
    pdf.set_x(20)
    # pdf = insert_picture(pdf, img_path=basedir + '/test/image/2.png', title='relation', x=0, y=0,
    #                      img_description='image')
    generate_pdf(pdf, name)
    return True
