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
