from app.models import db
from app.models.tcm.project import Project
from app.models.tcm.analysis import Analysis
from app.viewModels.tcm.project import handle_project_completed
from app.utils.algorithm_handler.data_analysing_mining.relational_analysis import handle_homogeneous
from app.utils.algorithm_handler.complex_network.community_detection.louvain import handle_louvain
from app.utils.algorithm_handler.complex_network.community_detection.cliques import handle_find_cliques
from app.utils.algorithm_handler.complex_network.community_detection.onion_layers import handle_onion_layers
from app.utils.algorithm_handler.complex_network.backboning import handle_find_backbone
from app.utils.celery_handler import celery
from app.utils.file_handler.table_handler.csv import generate_csv_file
from app.utils.time import generate_datetime_str

"""
函数参数：需要分析的数据,方法参数字典，分析文件夹
函数返回值：树形数据，表格数据，图形数据，原始的分析结果数据，pdf报告story型的数据，excel表格数据
tree_data,table_data,graph_data,raw_result_data,pdf_stories,excel_sheets_data
"""
analysis_promise = {
    'homogeneous': handle_homogeneous,
    'louvain': handle_louvain,
    'cliques': handle_find_cliques,
    'onion_layers': handle_onion_layers,
    'backbone': handle_find_backbone,
}


@celery.task(bind=True)
def new_analysis(self, project_id, user_project_files_dir, analysis_id, method, main_data, parameters):
    project = Project.query.filter_by(id=project_id).first_or_404()
    analysis = Analysis.query.filter_by(id=analysis_id).first_or_404()
    user_project_analysis_files_dir = user_project_files_dir + str(analysis.id) + '-' + str(analysis.method) + '方法分析结果/'
    # 先把任务ID存到数据库中，并初始化
    with db.auto_commit():
        # analysis.other_result_data = {"task_id": self.id}
        analysis.other_result_data = {}
        analysis.analysis_status = 'wait to start'
    # 确认有这个方法
    if method not in analysis_promise.keys():
        with db.auto_commit():
            analysis.analysis_status = 'method error'
            analysis.remarks = '方法错误，没有这种方法'
        return '没有这种方法'
    # 根据method调用算法
    try:
        with db.auto_commit():
            analysis.analysis_status = 'analysing'
        main_result_data = analysis_promise[method](main_data, parameters, user_project_analysis_files_dir)
        # print(main_result_data)
    except Exception as e:
        with db.auto_commit():
            analysis.analysis_status = 'analysis fail'
            analysis.remarks = str(e)
        return '分析失败'
    # 分析完成后开始生成excel表格文件
    with db.auto_commit():
        analysis.analysis_status = 'generating excel file'
    # 生成表格文件
    try:
        # 用csv文件代替Excel文件
        tables_data = main_result_data['excel_sheets_data']
        for table_data in tables_data:
            csv_file_name = generate_datetime_str() + str(analysis.id) + '-' + method + '-' + table_data[
                'name'] + '分析报告.csv'
            generate_csv_file(filename=csv_file_name, table_data=table_data['data'],
                              file_dir=user_project_analysis_files_dir)
        # excel_file_name = generate_datetime_str() + str(analysis.id) + '-' + method + '-Excel分析报告.xlsx'
        # generate_xlsx_file(filename=excel_file_name, table_sheets=main_result_data['excel_sheets_data'],
        #                    file_dir=user_project_analysis_files_dir)
    except Exception as e:
        print(e)
        with db.auto_commit():
            analysis.analysis_status = 'generate excel file fail'
            analysis.remarks = str(e)
        return '生成Excel文件失败'

    # 得到分析结果并提交
    with db.auto_commit():
        analysis.main_result_data = main_result_data
        analysis.other_result_data = {"analysis_file_dir": user_project_analysis_files_dir}
        analysis.analysis_status = 'all completed'
    handle_project_completed(project, user_project_files_dir)
    return True
