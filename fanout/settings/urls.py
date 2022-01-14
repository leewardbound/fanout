# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView
from rest_framework.routers import DefaultRouter

from fanout.apps.utils.views import healthz

api_router = DefaultRouter(trailing_slash=True)
api_router.include_root_view = settings.DEBUG
api_router.include_format_suffixes = False

urlpatterns = [
    path("api/", include(api_router.urls)),
    path("mgmt/", admin.site.urls),
    path("healthz/", healthz),
    path("graphql/", GraphQLView.as_view(graphiql=True)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
