# -*- coding: utf-8 -*-
def application(env, start):
    from cgi import parse_qs
    start('200 OK', [('Content-Type', 'text/html')])

    get = parse_qs(env.get('QUERY_STRING', ''), keep_blank_values = True)
    post = parse_qs(env['wsgi.input'].read(), keep_blank_values = True)

    to_show = [
        ['GET - параметры', get],
        ['POST - параметры', post]
    ]

    output = ['<html>', '<h1>%s</h1>' % 'Привет, мир!']

    for params in to_show:
        output.append('<h3>%s (%d)</h3>'
                % (params[0], len(params[1])))
        output.append('<pre>')

        output.extend(
            [
                "%s ==> '%s' \n"
                    % (k, v.pop()) for k,v in params[1].items()
            ]        
        )

        output.append('</pre>')

    output.append('</html>')

    return output
