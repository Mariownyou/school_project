from django import template


register = template.Library()


def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, '')


def cut_text(text):
    return text[::1]


def name(name):
    end_1 = 'ы'
    end_2 = 'ва'
    name = name.split(" ")
    first = list(name[0])
    second = list(name[1])
    first[-1] = end_1
    second[-1] = end_2
    f = s = ''
    for i in first:
        f += i
    for i in second:
        s += i 
    full = f'{f} {s}'

    print(full)
    return full


register.filter('cut', cut)
register.filter('cut_text', cut_text)
register.filter('name', name)