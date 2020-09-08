import argparse

from iblog.api_server import ApiServer
from iblog.mq_server import MqServer
from iblog.schedule_server import ScheduleServer

parser = argparse.ArgumentParser(description='Describe your program')
parser.add_argument('-m', '--mode', type=str, default='abc', help='''
        - a 提供api供其它服务调用的方式来操作issue;
        - b 提供MQ消费者的方式来操作issue;
        - c 提供定时任务来操作issue;
        例如：-m abc;
    ''')
parser.add_argument('-t', '--target', nargs='+', default=['github'], help='''
            - github 同步github issues;
            - gitee 同步gitee issues;
            例如：-t github gitee;
    ''')
args = parser.parse_args()


def main():
    print(args)

    # 运行Flask
    ApiServer()

    # 监听RBMQ
    MqServer()

    # 定时任务
    ScheduleServer()


if __name__ == '__main__':
    main()
