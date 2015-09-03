import json
import logging
import time

from django.conf import settings
from django.http import JsonResponse, HttpResponseNotAllowed
from hacker_news.index import index

logger = logging.getLogger(__name__)


def count(request, version, date_string):
    response = {'count': index.count(date_string)}
    return JsonResponse(response)


def popular(request, version, date_string):
    size = int(request.GET.get('size', 5))
    queries = [{'query': query, 'count': count} for query, count in index.top_queries(date_string, size)]
    response = {'queries': queries}
    return JsonResponse(response)


def build_index(request, version):
    '''
    This should be done at start-up time by overriding Django's
    AppConfig.ready method, however that is being called twice on start-up time,
    which is not ideal. So let's temporarily make it an API endpoint for
    development purposes.
    '''
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    size = request.POST.get('size')
    size = int(size) if size is not None else None

    start = time.time()
    index.build_from_scratch(size)
    end = time.time()
    delta_in_ms = int(1000 * (end - start))
    logger.warn('Index is ready. It was built in %d ms.' % delta_in_ms)

    return JsonResponse({'success': True})
