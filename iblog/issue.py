from abc import abstractmethod, ABCMeta
from dataclasses import dataclass, field
from typing import List

import gitee
from github import Github


@dataclass
class Issue(object):
    id: int = field(default=0)  # issue id
    blog_id: int = field(default=0)  # blog id
    number: str = field(default='')  # issue number
    html_url: str = field(default='')  # issue url
    state: str = field(default='')  # issue state  open（开启的）, progressing(进行中), closed（关闭的）, rejected（拒绝的）
    title: str = field(default='')  # issue title
    body: str = field(default='')  # issue body
    labels: str = field(default='')  # 用逗号分开的标签，名称要求长度在 2-20 之间且非特殊字符。如: bug,performance
    target: List[str] = field(default_factory=list)  # 如:github or gitee
    repo: List[str] = field(default_factory=list)  # 如：openjw/blog
    token: List[str] = field(default_factory=list)  # access_token


class SyncIssue(metaclass=ABCMeta):
    @abstractmethod
    def create(self, issue: Issue):
        pass

    @abstractmethod
    def update(self, issue: Issue):
        pass

    @abstractmethod
    def close(self, issue: Issue):
        pass


class GithubIssue(SyncIssue):
    def __init__(self, access_token=None, repo=None):
        self.access_token = access_token
        self.repo = repo
        self.github = Github(self.access_token, user_agent='openjw')

    def create(self, issue: Issue):
        repo = self.github.get_repo(self.repo)
        new_issue = repo.create_issue(title=issue.title, body=issue.body, labels=issue.labels.split(","))
        return {'number': new_issue.number, 'html_url': new_issue.html_url}

    def update(self, issue: Issue):
        post_params = {}
        if issue.title:
            post_params['title'] = issue.title
        if issue.body:
            post_params['body'] = issue.body
        if issue.labels:
            post_params['labels'] = issue.labels.split(",")

        repo = self.github.get_repo(self.repo)
        update_issue = repo.get_issue(number=int(issue.number))
        update_issue.edit(**post_params)

    def close(self, issue: Issue):
        repo = self.github.get_repo(self.repo)
        update_issue = repo.get_issue(number=int(issue.number))
        update_issue.edit(state='closed')


class GiteeIssue(SyncIssue):
    def __init__(self, access_token=None, repo=''):
        self.access_token = access_token
        self.owner = ''
        self.repo = ''
        if repo:
            self.owner = repo.split('/')[0]
            self.repo = repo.split('/')[1]

        self.gitee = gitee.IssuesApi()

    def create(self, issue: Issue):
        post_params = {}
        if self.access_token:
            post_params['access_token'] = self.access_token
        body = gitee.Body6(repo=self.repo,
                           title=issue.title, body=issue.body,
                           labels=issue.labels,
                           **post_params)
        new_issue = self.gitee.post_v5_repos_owner_issues(owner=self.owner, body=body)
        return {'number': new_issue.number, 'html_url': new_issue.html_url}

    def update(self, issue: Issue):
        post_params = {}
        if issue.title:
            post_params['title'] = issue.title
        if issue.body:
            post_params['body'] = issue.body
        if issue.labels:
            post_params['labels'] = issue.labels
        if self.access_token:
            post_params['access_token'] = self.access_token
        self.gitee.patch_v5_repos_owner_issues_number(owner=self.owner, repo=self.repo, number=issue.number,
                                                      **post_params)

    def close(self, issue: Issue):
        post_params = {}
        if self.access_token:
            post_params['access_token'] = self.access_token
        self.gitee.patch_v5_repos_owner_issues_number(owner=self.owner, repo=self.repo, number=issue.number,
                                                      state="closed",
                                                      **post_params)
