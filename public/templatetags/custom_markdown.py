from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
import markdown
import json
register = template.Library()  #自定义filter时必须加上


@register.filter(is_safe=True)  #注册template filter
@stringfilter  #希望字符串作为参数
def custom_markdown(value):     # 格式化markdown
    return mark_safe(markdown.markdown(value,
        extensions=['markdown.extensions.fenced_code',
                    'markdown.extensions.codehilite'],
        safe_mode=True,enable_attributes=False)
    )


@register.filter(is_safe=True)  #注册template filter
@stringfilter  #希望字符串作为参数
def celery_status(value):   # 格式化celery
    if value:
        d = json.loads(value)
        s = d.get('status')
    else:
        s = 'RUNNING'
    r = {
            'FAILURE': '<p style="color:red">失败</p>',
            'SUCCESS': '<p style="color:blue">完成</p>',
            'RUNNING': '<p style="color:#d600ff">执行中</p>'
        }
    return mark_safe(r.get(s))


@register.filter(is_safe=True)
@stringfilter
def ansible_result(s):      #ansible_result
    if not s:
        return "未搜索🔍到结果"
    data = json.loads(s)
    msg = ""
    for d in data:
        if  d.get('status') in [ "failed", "unreachable" ]:
            msg += '<span style="color:red">{host} | {task} => {status}<br>        {msg}</span><br>'.format(
                host=d['host'], task=d['task'], status=d['status'], msg=d['result']['msg']
            )
            continue
        elif d['result']['changed'] == False and d['status'] != 'ignoring':
            color = 'green'
        elif d['result']['changed'] == False:
            color = 'red'
        elif d['result']['changed'] == True:
            color = 'yellow'
        msg += '''<span style="color:{color}">{host} | {task} => {status} <br>        "changed": {changed}, <br>        "{task}": {data} </span><br>'''.format(
                color=color, host=d['host'], task=d['task'], status=d.get('status', 'None'),data=d['result'].get('msg', ''), changed=d['result'].get('changed')
            )
        if d['status'] == 'skipped':
            msg += '<span style="color:rebeccapurple">......%s     [%s]</span><br>' % ('跳过上个任务', d['host'])
        elif d['status'] == 'ignoring':
            msg += '<span style="color:#337899">......%s     [%s]</span><br>' % ('忽略任务错误', d['host'])
    return mark_safe(msg)


@register.filter(is_safe=True)  
def json_format(s):
    if isinstance(s, dict):
        return json.dumps(s, indent=4)
    elif isinstance(s,str):
        return json.dumps(json.loads(s),  indent=4)
    else:
        return 'format fail'
