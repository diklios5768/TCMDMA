from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from app.settings import basedir

from app.utils.file_handler.pdf_handler.generate import generate_pdf_file
from app.utils.file_handler.pdf_handler.story import generate_test_story, generate_report_story

# 注册字体
# 字体文件夹
FONTS_DIR = basedir + r'/static/fonts/'

# 注册中文字体
# 宋体
pdfmetrics.registerFont(TTFont('simsun', FONTS_DIR + 'simsun.ttf'))
pdfmetrics.registerFont(TTFont('simsunb', FONTS_DIR + 'simsunb.ttf'))

# 楷体
pdfmetrics.registerFont(TTFont('simkai', FONTS_DIR + 'simkai.ttf'))
# 黑体
pdfmetrics.registerFont(TTFont('simhei', FONTS_DIR + 'simhei.ttf'))
# 隶书
pdfmetrics.registerFont(TTFont('simli', FONTS_DIR + 'simli.ttf'))
# 微软雅黑
pdfmetrics.registerFont(TTFont('msyh', FONTS_DIR + 'msyh.ttf'))

# 注册英文字体
# 新罗马体
pdfmetrics.registerFont(TTFont('times', FONTS_DIR + 'times/times.ttf'))
pdfmetrics.registerFont(TTFont('timesbd', FONTS_DIR + 'times/timesbd.ttf'))
pdfmetrics.registerFont(TTFont('timesi', FONTS_DIR + 'times/timesi.ttf'))
pdfmetrics.registerFont(TTFont('timesbi', FONTS_DIR + 'times/timesbi.ttf'))


# 具体的最终调用的生成函数，传入必要参数
def generate_test_pdf_file(full_file_path):
    my_story = generate_test_story()
    generate_pdf_file(full_file_path, my_story)


def generate_report_file(file_path, stories: list = []):
    my_story = generate_report_story(stories)
    generate_pdf_file(file_path, story=my_story)
    return True
