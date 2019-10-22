from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from main import views

urlpatterns = [
    # 首页
    path('', views.NoteDetailView.as_view(), {'key': 'meta'}, name='note-root'),

    # 内容页
    path('<str:key>', views.NoteDetailView.as_view(), name='note-detail'),
    path('<str:key>/edit', views.NoteEditView.as_view(), name='note-edit'),
    path('<str:key>/commit', views.NoteCommitView.as_view(), name='note-commit'),
    path('<str:key>/save', views.NoteSaveView.as_view(), name='note-save'),
    path('<str:key>/discard', views.NoteDiscardView.as_view(), name='note-discard'),

    # 查询页
    path('tags/query', views.TagJsonListView.as_view(), name='tags-query'),
    path('notes/query', views.NoteListView.as_view(), name='notes-query'),

    # 管理页
    path('admin/', admin.site.urls, name='admin'),
    path('accounts/login', views.LoginView.as_view(), name='login'),
    path('accounts/logout', views.LogoutView.as_view(), name='logout'),
]