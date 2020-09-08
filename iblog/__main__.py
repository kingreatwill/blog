from iblog.api_server import ApiServer
from iblog.mq_server import MqServer
from iblog.schedule_server import ScheduleServer

if __name__ == '__main__':
    # 运行Flask
    ApiServer()

    # 监听RBMQ
    MqServer()

    # 定时任务
    ScheduleServer()
