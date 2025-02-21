from celery import Celery
from compiles.pyCompile import run_py
from compiles.jsCompile import run_js
from compiles.cppCompile import run_cpp

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)


@celery_app.task
def execute_task(request):
    if request.get('language_id') == 71:
        return run_py(request)
    elif request.get('language_id') == 63:
        return run_js(request)
    elif request.get('language_id') == 54:
        return run_cpp(request)
    else:
        return {
            "output": 'language do not find',
            "status": "Error",
        }
