from django import template

register = template.Library()


@register.filter(name='split')
def split(value, key):
    return str(value).split(key, 1)[0]  # 以 key 做為分隔符，指定第二个参数為 1，返回两个参数列表
