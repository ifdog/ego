from django import http
from django.contrib.auth import mixins
from django.contrib.auth import views as auth_views
from django.views import generic
from main import forms, error_codes, dal, models
from main import statics
from datetime import datetime
from django.urls import resolve

# Create your views here.

# 用户登录
class LoginView(auth_views.LoginView):
    template_name = 'main/login.html'
    redirect_field_name = 'next'


# 用户登出
class LogoutView(auth_views.LogoutView):
    redirect_field_name = 'next'


# Tag自动完成
class TagJsonListView(mixins.LoginRequiredMixin, generic.View):
    raise_exception = True

    def get(self, request):
        text = request.GET.get('text')
        if text:
            tags = dal.tag_matches(text)
            tag_texts = [i.name for i in tags]
            return http.JsonResponse({'state': error_codes.SUCCESS, 'msg': 'Get success', 'tags': tag_texts})
        else:
            return http.HttpResponseBadRequest()


# Note搜索
class NoteListView(generic.ListView):
    model = models.Note
    template_name = 'main/note_list.html'
    paginate_by = 10

    def get_queryset(self):
        _key = self.request.GET.get('key')
        
        if _key:
            if self.request.user.is_authenticated:
                result = dal.note_query_all(_key)
                if not [i for i in result if i.key == _key]:
                    result = list(result)
                    result.insert(0,{'key': _key, 'markdown': statics.NULL_NOTE_TEMPLATE,'markdown_time':datetime.now(), 'tags': ['missing']})
                return result
            else:
                return dal.note_query_public(_key)
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = self.request.GET.get('key')
        return context

# Note读取
class NoteDetailView(generic.DetailView):
    model = models.Note
    template_name = 'main/note_detail.html'
    slug_field = 'key'
    slug_url_kwarg = 'key'

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except http.Http404:
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        _slug = self.kwargs.get(self.slug_url_kwarg)
        # 首先这个Note要存在,否则返回空
        if self.object:
            # 其次判断是否有正文，没有就返回空
            if self.object.markdown:
                # 然后判断是否需要登陆才能读取
                if dal.contains_tag_attr(self.object.tags, statics.SHOW_PUBLIC_TAG):
                    # 如果没有权限限制，那么什么都不做，正常显示
                    pass
                else:
                    # 然后判断是否已经登录
                    if self.request.user.is_authenticated:
                        # 如果已经登录，那么什么都不做，正常显示
                        pass
                    # 如果有权限控制，却没登录，那么返回禁止信息
                    else:
                        context['object'] = {'key': _slug, 'markdown': statics.FORBIDDEN_NOTE_TEMPLATE,
                                             'markdown_time':datetime.now(), 'tags': ['forbidden']}
            # 如果没有正文，就显示空信息
            else:
                context['object'] = {'key': self.object.key,
                                     'markdown':  statics.NULL_NOTE_TEMPLATE,
                                     'markdown_time':datetime.now(),
                                     'tags': self.object.tags}
        # 如果Note不存在，则显示空信息
        else:
            context['object'] = {'key': _slug, 'markdown': statics.NULL_NOTE_TEMPLATE,'markdown_time':datetime.now(), 'tags': ['missing']}
        return context


# Note编辑(包括提交、保存草稿、删除草稿)的GET部分
class NoteEditView(mixins.LoginRequiredMixin, generic.edit.FormView):
    template_name = 'main/note_update.html'
    form_class = forms.NoteEditForm

    login_url = '/accounts/login'

    def get_initial(self):
        _key = self.kwargs.get('key')
        self.success_url = '/' + _key
        _note = dal.note_get(_key)
        if _note and (_note.draft or _note.markdown):
            if _note.draft:
                _content = _note.draft
            else:
                _content = _note.markdown
            tags = ','.join([i.name for i in _note.tags.all()])
            return {'key': _note.key, 'content': _content, 'draft': '', 'tags': tags}
        else:
            return {'key': _key, 'content': statics.NULL_NOTE_TEMPLATE, 'draft': ''}


# Note编辑，提交的POST部分
class NoteCommitView(NoteEditView):
    def form_valid(self, form):
        _key = self.kwargs.get('key')
        _content = form.cleaned_data['content']
        _tag_text = [i.strip() for i in form.cleaned_data['tags'].split(',')]
        _tags = [dal.tag_get_or_create(i) for i in _tag_text if i]
        _note = dal.note_get(_key)
        if _note:
            _note.tags.clear()
            dal.update_markdown(_note,_content)
        else:
            _note = dal.note_add(_key,_content,"")
        for tag in _tags:
            _note.tags.add(tag)
        if _note.draft:
            dal.update_draft(_note, "")
        return http.HttpResponseRedirect(self.get_success_url())


# Note编辑，保存草稿的POST部分
class NoteSaveView(NoteEditView):
    

    def form_valid(self, form):
        _key = self.kwargs.get('key')
        _content = form.cleaned_data['content']
        _tag_text = [i.strip() for i in form.cleaned_data['tags'].split(',')]
        _tags = [dal.tag_get_or_create(i) for i in _tag_text if i]
        _note = dal.note_get(_key)
        if not _note:
            _note = dal.note_add(_key,"",_content)
            for tag in _tags:
                _note.tags.add(tag)
        else:
            dal.update_draft(_note, _content)
        self.success_url = "/"+_key+"/edit"
        return http.HttpResponseRedirect(self.get_success_url())


# Note编辑，删除草稿的POST部分
class NoteDiscardView(NoteEditView):
    def form_valid(self, form):
        _key = self.kwargs.get('key')
        _note = dal.note_get(_key)
        dal.update_draft(_note, "")
        return http.HttpResponseRedirect(self.get_success_url())
