import datetime

from peewee import *


class BaseModel(Model):
    # http://docs.peewee-orm.com/en/latest/peewee/models.html#model-options-and-table-metadata
    class Meta:
        legacy_table_names = False


class IssueBasic(BaseModel):
    id = BigAutoField(primary_key=True, help_text='主键id')
    tenant_id = BigIntegerField(default=1, constraints=[Check('tenant_id > 0')], help_text='租户id')
    blog_id = BigIntegerField(default=0, constraints=[Check('blog_id > 0')], help_text='blog id')
    title = CharField(default='', max_length=50, help_text='issue title')
    body = TextField(default='', help_text='issue body')
    labels = CharField(default='', max_length=50, help_text='issue labels')
    state = CharField(default='open', max_length=50, help_text='issue state')
    create_at = DateTimeField(default=datetime.datetime.now, help_text='创建时间')

    class Meta(object):
        ...
        # primary_key = CompositeKey('tenant_id', 'blog_id')
        # indexes = (
        #     # create a unique on tenant_id/blog_id
        #     (('tenant_id', 'blog_id'), True)
        # )


class IssueSync(BaseModel):
    id = BigAutoField(primary_key=True, help_text='主键id')
    basic_id = BigIntegerField(default=0, constraints=[Check('basic_id > 0')], help_text='basic id')
    tenant_id = BigIntegerField(default=1, constraints=[Check('tenant_id > 0')], help_text='租户id')
    blog_id = BigIntegerField(default=0, constraints=[Check('blog_id > 0')], help_text='blog id')
    dist = CharField(default='', max_length=50, help_text='同步目标')
    repo = CharField(default='', max_length=50, help_text='同步仓库')
    issue_number = CharField(default='', max_length=50, help_text='issue number')
    sync_state = IntegerField(default=0, help_text='同步状态(0:未同步;1:同步成功;)')
    update_at = DateTimeField(default=datetime.datetime.now, help_text='更新时间')

    class Meta(object):
        ...
        # primary_key = CompositeKey('tenant_id', 'dist', 'blog_id')
        # indexes = (
        #     # create a unique on tenant_id/tenant_id/dist/repo
        #     (('tenant_id', 'blog_id', 'dist', 'repo'), True)
        # )
