# -*- encoding: utf-8 -*-
"""
@File Name      :   dataset.py
@Create Time    :   2021/7/15 15:43
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

import locale
from datetime import datetime
from flask import render_template
from app.libs.lists import analysis_status
from app.models import db
from app.models.tcm.project import Project
from app.utils.time import generate_datetime_str
from app.utils.file_handler.pdf_handler import generate_report_file
from app.utils.file_handler.zip_handler import zip_dir
from app.utils.celery_handler.mail import send_files_mail_sync

# 解决Value error: embedded null byte的问题
locale.setlocale(locale.LC_ALL, 'en')
locale.setlocale(locale.LC_CTYPE, 'chinese')


def find_project(data):
    projects = None
    find_type = data.get('type', 'all')
    owner_id = data.get('owner_id', 1)
    # 查看所有的历史数据集
    if find_type == 'history':
        projects = Project.query.filter_by(owner_id=owner_id,
                                           status=1).all()
    elif find_type == 'single':
        project = Project.query.filter_by(id=data['project_id'], status=1).first()
    elif find_type == 'random':
        projects = Project.query.filter_by(status=1).limit(data['count']).all()
    # 查询标星的项目
    elif find_type == 'star':
        projects = Project.query.filter_by(owner_id=owner_id,
                                           star=True,
                                           status=1).all()
    # 查询已经删除的数据集
    elif find_type == 'remove':
        projects = Project.query.filter_by(owner_id=owner_id,
                                           status=0).all()
    elif find_type == 'all':
        projects = Project.query.filter_by(status=1).all()
    if projects is not None:
        projects_dict = [dict(project) for project in projects]
    else:
        projects_dict = [dict(project)]
    return {'rows': projects_dict, 'code': 1, 'msg': '查询成功'}


def project_complete_rate(project):
    analyses = project.analyses
    all_count = len(analyses)
    count = 0
    for analysis in analyses:
        status = analysis.analysis_status
        if status == 'all completed' or 'fail' in status or 'error' in status:
            count += 1
        else:
            count += round((analysis_status.index(status) + 1) / len(analysis_status), 3)
    rate = round(count / all_count, 2)
    with db.auto_commit():
        project.finished_rate = rate
        if rate == 1:
            project.finished = True
    return rate


def handle_project_completed(project, user_project_files_dir):
    rate = project_complete_rate(project)
    # 如果方法全部完成，则进行收尾处理
    if rate == 1:
        # 生成PDF报告
        pdf_file_name = generate_datetime_str() + project.name + '项目分析报告.pdf'
        pdf_file_path = user_project_files_dir + pdf_file_name
        pdf_stories = []
        for each_analysis in project.analyses:
            # attention:注意这里使用列表合并的方法
            pdf_stories.extend(each_analysis.main_result_data.get('pdf_stories', []))
        generate_report_file(pdf_file_path, pdf_stories)
        # 打包整个文件夹
        zip_file_name = generate_datetime_str() + project.name + '项目完整分析结果数据.zip'
        zip_file_path = user_project_files_dir + '../' + zip_file_name
        zip_dir(zip_file_path, user_project_files_dir)
        with db.auto_commit():
            other_result = {'pdf_file_path': pdf_file_path, 'pdf_download_path': pdf_file_path,
                            'zip_file_path': zip_file_path, 'zip_download_path': zip_file_path}
            project.other_result = other_result
        # 发送邮件
        send_files_mail_sync.delay(subject=project.name + "项目分析报告", to=[project.user.email],
                                   body=render_template('mail/report.txt', username=project.user.username,
                                                        datetime=str(datetime.utcnow().strftime("%Y年%m月%d日"))),
                                   files=[{'path': zip_file_path, 'name': zip_file_name,
                                           'content_type': 'application/zip'}])
