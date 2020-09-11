import argparse
from itertools import zip_longest

from iblog import target
from iblog.api_server import ApiServer
from iblog.mq_server import MqServer
from iblog.schedule_server import ScheduleServer

parser = argparse.ArgumentParser(description='Describe your program')
parser.add_argument('-m', '--mode', type=str, default='a', help='''
        - a 提供api供其它服务调用的方式来操作issue;
        - b 提供MQ消费者的方式来操作issue;
        - c 提供定时任务来操作issue;
        例如：-m abc;
    ''')

parser.add_argument('--ahost', type=str, default='0.0.0.0', help='api host.')
parser.add_argument('--aport', type=int, default=8080, help='api port.')
parser.add_argument('--adebug', action='store_true', help='api debug.')

parser.add_argument('-b', '--bmq', type=str, default='rabbitmq', help='MQ类型(rabbitmq, kafka).')
parser.add_argument('--bqueue', type=str, default='BlogIssueQueue', help='rabbitmq的消费队列.')
parser.add_argument('--bservers', type=str, default='', help='rabbitmq或kafka的地址, 多个逗号隔开.')
parser.add_argument('--btopic', type=str, default='BlogIssueTopic', help='kafka的topic.')
parser.add_argument('--bgroup_id', type=str, default='BlogIssueGroup', help='kafka的默认队列.')

parser.add_argument('-c', '--crontab', type=str, default='0 */1 * * *', help='默认整点执行一次.')

parser.add_argument('-t', '--target', nargs='+', default=['gitee'], help='''
            - github 同步github issues;
            - gitee 同步gitee issues;
            例如：-t github access_token gitee;
    ''')
parser.add_argument('--token', nargs='+', default=[], help='access_token 顺序与target一致.')
parser.add_argument('--repo', nargs='+', default=[], help='repo(如: kingreatwill/blog) 顺序与target一致.')

args = parser.parse_args()


# celery 分布式任务队列
def main():
    print(args)
    # 初始化目标;
    target.init(list(zip_longest(args.target, args.token, args.repo, fillvalue=None)))

    threads = []
    if args.mode.find('a') >= 0:
        # 运行Flask
        server_a = ApiServer(host=args.ahost, port=args.aport, debug=args.adebug)
        server_a.start()
        threads.append(server_a)

    if args.mode.find('b') >= 0:
        # 监听RBMQ
        server_b = MqServer(mq=args.bmq, queue=args.bqueue, servers=args.bservers, topic=args.btopic,
                            group_id=args.bgroup_id)
        server_b.start()
        threads.append(server_b)

    if args.mode.find('c') >= 0:
        # 定时任务
        server_c = ScheduleServer(crontab=args.crontab)
        server_c.start()
        threads.append(server_c)

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    main()
    print("程序运行结束.")
