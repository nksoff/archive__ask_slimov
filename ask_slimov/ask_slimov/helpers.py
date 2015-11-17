from django.http import HttpResponse
import json

# pagination
def paginate(objects, request):
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

    page = request.GET.get('page')
    p = Paginator(objects, 8)

    try:
        result = p.page(page)
    except PageNotAnInteger:
        result = p.page(1)
    except EmptyPage:
        result = p.page(1)

    return result

# reponse ajax
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
