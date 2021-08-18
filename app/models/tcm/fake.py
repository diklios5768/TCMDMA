from .user import fake_users, init_role
from .project import fake_projects
from .dataset import fake_datasets
from .analysis import fake_analyses, init_method


def init_fake(count):
    user_count = count
    project_count = count * 5
    dataset_count = count * 8
    analysis_count = project_count * 5
    init_role()
    fake_users(user_count)
    fake_projects(project_count)
    fake_datasets(dataset_count)
    fake_analyses(analysis_count)
    init_method()
