from django import template

register = template.Library()

forbidden_words = ['дурак']


@register.filter(name='Censor')
def Censor(arg):
    words = arg.split()
    result = []
    for word in words:
        if word in forbidden_words:
            result.append(word[0] + "*" * (len(word) - 2) + word[-1])
        else:
            result.append(word)
    return " ".join(result)
