
from django.conf.urls import include, url
from .views import ChatBotView


urlpatterns = [
                  url(r'^b33f1337d56676a51c9312421dfaf5183308fbc4848982c267/?$',ChatBotView.as_view())
]