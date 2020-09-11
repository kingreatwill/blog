from flask import request


def params():
    args = request.values.to_dict()
    return {**args, **(request.json if request.json else {})}
    # request.get_data() 不需要 content_type = application/json  if request.content_type.find('application/json') >= 0:
    # p = request.args.to_dict() if request.method == 'GET' else ast.literal_eval(
    #     (request.get_data() if request.content_type.find('application/json') >= 0 else request.data).decode(
    #         encoding='utf-8')
    # )
