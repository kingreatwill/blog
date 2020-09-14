import inspect
import sys
from typing import List

from playhouse.db_url import connect, Database

from iblog.domain import model
from iblog.issue import Issue
from iblog.target import TargetModel


def is_base_model_subclass(obj):
    if inspect.isclass(obj):
        return obj != model.BaseModel and issubclass(obj, model.BaseModel)
    return False


models = inspect.getmembers(sys.modules[model.__name__], is_base_model_subclass)
model_classes = []

# http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#db-url
db: Database = connect(url='sqlite:///:memory')


def init(url='sqlite:///:memory'):
    global db
    db = connect(url=url)
    for name, class_ in models:
        class_.bind(db)
        model_classes.append(class_)
    db.create_tables(model_classes)


if __name__ == '__main__':
    init('mysql+pool://root:123456@lcb@127.0.0.1:3306/iblog?max_connections=300&stale_timeout=300')
    with db.connection_context():
        with db.transaction():
            basic = model.IssueBasic(blog_id=5, title='testing.')
            basic.save(force_insert=True)
            sync = model.IssueSync(basic_id=basic.id, blog_id=5, dist='github', repo='kingreatwill/blog')
            sync.save(force_insert=True)


def create(issue: Issue, targets: List[TargetModel]):
    with db.connection_context():
        with db.transaction():
            basic = model.IssueBasic(blog_id=issue.blog_id,
                                     title=issue.title,
                                     body=issue.body,
                                     labels=issue.labels
                                     )
            basic.save(force_insert=True)
            for t in targets:
                sync = model.IssueSync(basic_id=basic.id,
                                       blog_id=issue.blog_id,
                                       dist=t.dist,
                                       repo=t.repo)
                sync.save(force_insert=True)


# 更新
def update(issue: Issue):
    with db.connection_context():
        with db.transaction():
            basic = model.IssueBasic.get(model.IssueBasic.blog_id == issue.blog_id)
            if issue.title:
                basic.title = issue.title
            if issue.body:
                basic.body = issue.body
            if issue.labels:
                basic.labels = issue.labels
            if issue.state:
                basic.state = issue.state
            basic.save()
            # & / ,
            model.IssueSync.update({model.IssueSync.sync_state: 0}).where(
                (model.IssueSync.sync_state == basic.id)
                & (model.IssueSync.blog_id == issue.blog_id)
            ).execute()


# 更新同步状态
def update_sync_state(issue: Issue, targ: TargetModel):
    with db.connection_context():
        sync = model.IssueSync.get(
            (model.IssueSync.blog_id == issue.blog_id)
            & (model.IssueSync.dist == targ.dist)
            & (model.IssueSync.repo == targ.repo)
        )
        if not sync.issue_number:
            sync.issue_number = issue.number
        sync.sync_state = 1
        sync.save()
