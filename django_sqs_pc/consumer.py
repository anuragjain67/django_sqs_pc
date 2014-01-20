import json
from sqs_exceptions import HandlerError
from django.http import HttpResponseServerError, HttpResponse
from django.conf import settings

import importlib
tasks_map_path = importlib.import_module(settings.BACKGROUND_JOBS)

def tasks(request):
    if request.method == "POST":
        if request.META["CONTENT_TYPE"] == 'application/json':
            try:
                handler_tasks(request.body)        
                return HttpResponse(content="Task Completed")
            except Exception as e:
                return HttpResponseServerError(content=e)
    
def handler_tasks(payload_as_json):
    try:
        payload = json.loads(payload_as_json)
        task_name = payload["task_name"]
        params = payload["params"]
        handler = tasks_map_path.tasks_map[str(task_name)]
        handler(**params)
    except Exception as e:
        print e
        raise HandlerError("Handler was not able to proceed")