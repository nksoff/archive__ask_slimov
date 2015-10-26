# -*- coding: utf-8 -*-
from django.http import HttpResponse

def info(request):
    to_show = [
        ['GET - параметры', request.GET],
        ['POST - параметры', request.POST]
    ]

    output = ['<html>', '<h1>%s</h1>' % 'Привет, мир!']

    for params in to_show:
        output.append('<h3>%s (%d)</h3>'
                % (params[0], len(params[1])))
        output.append('<pre>')

        output.extend(
            [
                "%s ==> '%s' \n"
                    % (k, v) for k,v in params[1].items()
            ]        
        )

        output.append('</pre>')

    output.append('</html>')

    output.append('</html>')
    return HttpResponse(output)
