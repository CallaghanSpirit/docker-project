from os import environ
import multiprocessing

bind = "0.0.0.0:" + environ.get("PORT", "8000")
workers = multiprocessing.cpu_count()
max_requests = 1000
worker_class = "gevent"
reload = True
timeout = 120

env = {
    "DJANGO_SETTINGS_MODULE": "candystore.settings",
    "DJANGO_CONFIGURATION": "Production",
}
name = "driveparts"