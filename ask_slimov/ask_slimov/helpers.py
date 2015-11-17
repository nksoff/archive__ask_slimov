from django.http import HttpResponse
import json


# pagination
def paginate(objects, request, key=''):
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

    key = key + '_page'

    page = request.GET.get(key)
    p = Paginator(objects, 8)

    try:
        result = p.page(page)
    except PageNotAnInteger:
        result = p.page(1)
    except EmptyPage:
        result = p.page(1)

    result.from_left = result.number - 4
    result.from_right = result.number + 4
    result.key = key

    return result


# response ajax
class HttpResponseAjax(HttpResponse):
    def __init__(self, status='ok', **kwargs):
        kwargs['status'] = status
        super(HttpResponseAjax, self).__init__(
                content = json.dumps(kwargs),
                content_type = 'application/json',
                )


# response ajax with error
class HttpResponseAjaxError(HttpResponseAjax):
    def __init__(self, code, message):
        super(HttpResponseAjaxError, self).__init__(
                status = 'error', code = code, message = message
                )
