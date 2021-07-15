from django import template

# 템플릿 태그를 커스터마이징 할 때 사용하는 속성 등록
register = template.Library()
# decorator : 코드를 더 꾸며주듯이 작동되는 특별한 문법

@register.filter
def sub(value,arg):
    return value-arg