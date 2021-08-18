from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate, SimpleDocTemplate, NextPageTemplate, Frame
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

from app.utils.file_handler.pdf_handler.page_template import page_with_header_and_footer_template, \
    page_with_header_template, cover_page_template


# 自定义文档模板
class MyDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kw):
        self.allowSplitting = 0
        super().__init__(filename, **kw)
        frame = [Frame(3.18 * cm, 2.54 * cm, 14.64 * cm, 24.62 * cm, showBoundary=0)]
        page_with_header = page_with_header_template(frame)
        page_with_header_and_footer = page_with_header_and_footer_template(frame)
        cover_page = cover_page_template(frame)
        self.addPageTemplates(cover_page)
        self.addPageTemplates(page_with_header)
        self.addPageTemplates(page_with_header_and_footer)

    def afterFlowable(self, flowable):
        """Registers TOC entries."""
        if flowable.__class__.__name__ == 'Paragraph':
            text = flowable.getPlainText()
            style = flowable.style.name
            # if style == 'title':
            #     level = 0
            if style == 'Heading1':
                level = 1
            elif style == 'Heading2':
                level = 2
            elif style == 'Heading3':
                level = 3
            else:
                return
            each_table_of_content = [level, text, self.page]
            bn = getattr(flowable, '_bookmarkName', None)  # 得到bookmark的属性值
            print(bn)
            if bn is not None:
                each_table_of_content.append(bn)
            self.notify('TOCEntry', tuple(each_table_of_content))


# 生成报告
def generate_pdf_file(file_path, story):
    # 创建PDF文件，并设置纸张格式
    doc = MyDocTemplate(
        file_path,
        # 一般边框设置为0，不需要显示，测试的时候设置为1即可
        # showBoundary=1,
        # 设置页边距
        leftMargin=3.18 * cm,
        rightMargin=3.18 * cm,
        topMargin=2.54 * cm,
        bottomMargin=2.54 * cm,
        # 设置纸张大小
        pagesize=A4, )
    # 传入文档内容，并生成PDF文件，注意必须要用multiBuild，否则目录不会构建
    doc.multiBuild(story)
