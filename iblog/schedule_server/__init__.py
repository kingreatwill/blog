# https://tool.lu/crontab/
# 默认是内存存储，如果是分布式可以使用
# RDBMS 数据库，
# MongoDB
#
# Redis
#
# RethinkDB
#
# ZooKeeper
import threading

from iblog.target import Target


class ScheduleServer(threading.Thread,Target):
    def __init__(self, crontab):
        super().__init__()
        from apscheduler.schedulers.background import BackgroundScheduler
        from apscheduler.schedulers.blocking import BlockingScheduler
        from apscheduler.triggers.cron import CronTrigger
        # 默认整点执行一次
        self.crontab = crontab
        # 后期支持分布式
        self.scheduler = BlockingScheduler()
        self.scheduler.add_job(self.sync, CronTrigger.from_crontab(self.crontab))

    def sync(self):
        # 同步api
        # 同步数据库
        ...

    def run(self):
        self.scheduler.start()
