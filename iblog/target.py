from dataclasses import dataclass


@dataclass
class TargetModel(object):
    dist: str
    token: str
    repo: str


class Target(object):
    # 分块
    def chunk(self, lst, size):
        from math import ceil
        return list(map(lambda x: lst[x * size:x * size + size], list(range(0, ceil(len(lst) / size)))))

    def set_targets(self, targets: list):
        self.targets = []
        for target in targets:
            self.targets.append(TargetModel(target[0], target[1], target[2]))

    # 同步
    def sync(self):
        ...
