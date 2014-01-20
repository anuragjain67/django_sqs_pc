from django.conf.urls import patterns, url
from django_sqs_pc import consumer

urlpatterns = patterns('',
    url(r'^tasks', consumer.tasks),
    )