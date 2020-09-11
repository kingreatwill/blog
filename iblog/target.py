from dataclasses import dataclass
from itertools import zip_longest

from iblog.api_server import model
from iblog.issue import Issue, GiteeIssue, GithubIssue


@dataclass
class TargetModel(object):
    dist: str
    token: str
    repo: str


def sync_issue(m: TargetModel):
    if m.dist == 'gitee':
        return GiteeIssue(access_token=m.token, repo=m.repo)
    else:
        return GithubIssue(access_token=m.token, repo=m.repo)


targets = []


def init(tgts: list):
    global targets
    targets = get_for(tgts)


def get_for(tgts: list):
    l = []
    for target in tgts:
        l.append(TargetModel(target[0], target[1], target[2]))
    return l


def get_targets(issue: Issue = None):
    if not issue:
        return targets
    return targets if not issue.target else get_for(
        list(zip_longest(issue.target, issue.token, issue.repo, fillvalue=None))
    )


def sync_create(issue: Issue):
    result = []
    for t in get_targets(issue):
        obj = sync_issue(t)
        result.append({'dist': t.dist, **obj.create(issue)})
    return model.Response(ok=(not result) is False, data=result)


def sync_update(issue: Issue):
    result = []
    for t in get_targets(issue):
        obj = sync_issue(t)
        obj.update(issue)
        result.append({'dist': t.dist, 'ok': True})
    return model.Response(ok=(not result) is False, data=result)


def sync_delete(issue: Issue):
    result = []
    for t in get_targets(issue):
        obj = sync_issue(t)
        obj.close(issue)
        result.append({'dist': t.dist, 'ok': True})
    return model.Response(ok=(not result) is False, data=result)
