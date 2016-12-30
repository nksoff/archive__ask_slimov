from django.http import HttpResponse
import urllib2
import json


# pagination
def paginate(objects, request, key=''):
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

    key += '_page'

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
            content=json.dumps(kwargs),
            content_type='application/json',
        )


# response ajax with error
class HttpResponseAjaxError(HttpResponseAjax):
    def __init__(self, code, message):
        super(HttpResponseAjaxError, self).__init__(
            status='error', code=code, message=message
        )


# send comet messages

def comet_send_message(channel, text):
    url = 'http://nginx:8001/comet-publish/?id=' + channel
    body = json.dumps({'messages': [text]})
    request = urllib2.Request(url, body, {})
    response = urllib2.urlopen(request)
    return response


# a channel id for a question
def comet_channel_id_question(q):
    return 'q' + str(q.id)
