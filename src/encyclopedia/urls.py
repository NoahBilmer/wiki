from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search",views.search, name="search"),
    path("submitPage",views.submitPage, name="submitPage"),
    path("editPage",views.editPage, name="editPage"),
    path("editor",views.editor, name="editor"),
    path("submitEditedPage",views.submitEditedPage, name="submitEditedPage"),
    path("random",views.random,name="random"),
    path("wiki/<str:title>", views.showEntry, name="showEntry"),
    path("<str:title>", views.showEntry, name="showEntry"),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
