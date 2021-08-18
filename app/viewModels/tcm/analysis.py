from app.models.tcm.analysis import Analysis


def find_analysis(data):
    analyses = None
    project_id = data.get('project_id', 1)
    find_type = data.get('type', 'all')
    # 选择一个分析数据集，取出分析完毕后的数据
    if find_type == 'single':
        analysis = Analysis.query.filter_by(id=data['analysis_id'],
                                            status='1').first()
    # 查询正在分析的数据集
    elif find_type == 'analysing':
        analyses = Analysis.query.filter(
            Analysis.project_id == project_id,
            Analysis.analysis_status != 'analysis success',
            Analysis.status == 1).all()
    # 查看所有的历史数据集
    elif find_type == 'history':
        analyses = Analysis.query.filter_by(project_id=project_id,
                                            status=1).all()
    # 查询已经删除的数据集
    elif find_type == 'delete':
        analyses = Analysis.query.filter_by(project_id=project_id,
                                            status=0).all()
    if analyses is not None:
        analyses_dict = [dict(analysis) for analysis in analyses]
    else:
        analyses_dict = [dict(analysis)]
    return {'rows': analyses_dict, 'code': 1, 'msg': '查询成功'}
