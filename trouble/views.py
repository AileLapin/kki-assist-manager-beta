from datetime import datetime, date, timedelta
from django.shortcuts import render
from django.http import Http404, JsonResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin,
                                        AccessMixin)
from account.models import MyUser
from trouble.models import TroubleUser, TroubleCategory, Trouble, TroubleDateReport
from django.urls import reverse
from . import forms
from . import manager, make_trouble


class MyUserMixin:
    """アクセスしてきたユーザを格納"""
    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        return super().dispatch(request, *args, **kwargs)


class TroubleListView(LoginRequiredMixin, generic.TemplateView):
    # model = Trouble
    template_name = 'trouble/trouble_list.html'
    # queryset = Trouble.objects.exclude(is_staff=True)  # adminユーザは除外
    # context_object_name = 'troubles'
    # ordering = '-occur_date'
    # paginate_by = 10

    # 列挙する期間の日付と，その日付ごとのトラブルの数をまとめたリストを渡す
    def get_context_data(self, **kwargs):
        now = datetime.now()
        context = super().get_context_data(**kwargs)
        context['reports'] = manager.get_recent_troubles()
        context['trouble_form'] = forms.TroubleForm(initial={
            'year': now.year, 'month': now.month, 'day': now.day,
            'hour': now.hour, 'minute': now.minute})
        context['update_form'] = forms.TroubleForm
        return context


class TroubleDetailView(LoginRequiredMixin, generic.DetailView):
    # TroubleオブジェクトのCreate, Update View の基底になるView
    model = Trouble
    template_name = 'trouble/trouble_detail.html'
    context_object_name = 'trouble'


class TroubleCreateView(MyUserMixin, LoginRequiredMixin, generic.FormView):
    template_name = 'trouble/trouble_create.html'
    form_class = forms.TroubleCreateForm
    context_object_name = 'trouble'

    def form_valid(self, form):
        # postデータを組み立てて，新しいTroubleオブジェクト作成する
        trouble = form.assemble(form, self.user)
        # 新しいTroubleを発生日のTroubleDateReportに追加する
        manager.add_trouble_to_report(trouble)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('trouble:trouble_list')


class TroubleUpdateView(LoginRequiredMixin, PermissionRequiredMixin,
                        generic.detail.SingleObjectMixin, generic.FormView):
    model = Trouble
    template_name = 'trouble/trouble_update.html'
    form_class = forms.TroubleUpdateForm
    context_object_name = 'trouble'
    permission_required = ('trouble.change_trouble')

    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def has_permission(self):
        if super().has_permission():
            return True
        elif self.user == self.object.reporter or self.user == self.object.carer:
            return True
        else:
            return False

    def form_valid(self, form):
        form.assemble(form, self.user, self.object)
        return super().form_valid(form)

    def get_form_kwargs(self):
        obj = self.get_object()
        kwargs = super().get_form_kwargs()
        kwargs['trouble'] = obj
        kwargs.update({
                       'initial': {'carer': obj.carer,
                                   'occur_date': obj.occur_date,
                                   'occur_machine_type': str(obj.occur_machine)[:2],
                                   'occur_machine_num': str(obj.occur_machine)[-2:],
                                   'trouble_user_year': str(obj.trouble_user)[1:4],
                                   'trouble_user_num': str(obj.trouble_user)[-3:],
                                   'category': obj.category,
                                   'content': obj.content,
                                   'approach': obj.approach}})
        return kwargs

    def get_success_url(self):
        # return reverse('trouble:trouble_detail', kwargs={'pk': self.kwargs.get(self.pk_url_kwarg)})
        return reverse('trouble:trouble_list')


class TroubleDeleteView(LoginRequiredMixin, PermissionRequiredMixin,
                        generic.detail.SingleObjectMixin,
                        generic.edit.DeletionMixin,
                        generic.base.View):
    model = Trouble
    permission_required = ('trouble.delete_trouble')

    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def has_permission(self):
        if super().has_permission():
            return True
        elif self.user == self.object.reporter or self.user == self.object.carer:
            return True
        else:
            return False

    def delete(self, request, *args, **kwargs):
        trouble = self.get_object()
        manager.trouble_delete(trouble)
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('trouble:trouble_list')


class TroubleUserListView(LoginRequiredMixin, generic.ListView):
    '''TroubleUserの一覧表示'''
    model = TroubleUser
    template_name = 'trouble/trouble_user_list.html'
    context_object_name = 'trouble_users'
    paginate_by = 10


class TroubleUserDetailView(LoginRequiredMixin, generic.DetailView):
    model = TroubleUser
    template_name = 'trouble/trouble_user_detail.html'
    context_object_name = 'trouble_user'


class TroubleUserCreateView(LoginRequiredMixin, generic.CreateView):
    model = TroubleUser
    template_name = 'trouble/trouble_user_create.html'
    from_class = forms.TroubleUserForm
    fields = ['stu_num', 'last_name', 'first_name']

    def get_success_url(self):
        return reverse('trouble:trouble_use_list')


class TroubleUserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TroubleUser
    template_name = 'trouble/trouble_user_update.html'
    form_class = forms.TroubleUserForm
    # fields = ['stu_num', 'last_name', 'first_name'] # => いらないっぽい

    def get_success_url(self):
        return reverse('trouble:trouble_user_list')


class TroubleUserDeleteView(LoginRequiredMixin,
                            generic.detail.SingleObjectMixin,
                            generic.edit.DeletionMixin,
                            generic.base.View):
    model = TroubleUser

    def get_success_url(self):
        return reverse('trouble:trouble_user_list')


class TroubleCategoryListView(LoginRequiredMixin, generic.ListView):
    model = TroubleCategory
    template_name = 'trouble/trouble_category_list.html'
    context_object_name = 'trouble_categories'
    paginate_by = 10


class TroubleCategoryDetailView(LoginRequiredMixin, generic.DetailView):
    model = TroubleCategory
    template_name = 'trouble/trouble_category_detail.html'
    context_object_name = 'trouble_category'


class TroubleCategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin,
                                generic.CreateView):
    model = TroubleCategory
    template_name = 'trouble/trouble_category_create.html'
    from_class = forms.TroubleCategoryForm
    fields = ['title', 'content', 'approach']
    permission_required = ('trouble.add_troublecategory')

    def get_success_url(self):
        return reverse('trouble:trouble_category_list')


class TroubleCategoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin,
                                generic.UpdateView):
    model = TroubleCategory
    template_name = 'trouble/trouble_category_update.html'
    form_class = forms.TroubleCategoryForm
    permission_required = ('trouble.change_troublecategory')

    def get_success_url(self):
        return reverse('trouble:trouble_category_list')


class TroubleCategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin,
                                generic.detail.SingleObjectMixin,
                                generic.edit.DeletionMixin,
                                generic.base.View):
    model = TroubleCategory
    permission_required = ('trouble.delete_troublecategory')

    def get_success_url(self):
        return reverse('trouble:trouble_category_list')


@login_required
def get_trouble_detail_view(request):
    if request.method == "GET":
        pk = request.GET.get("pk")
        user = request.user
        permission = False
        trouble = Trouble.objects.get(pk=pk)

        if user.is_staff:
            permission = True
        elif user == trouble.reporter or user == trouble.carer:
            permission = True
        else:
            permission = False
        
        d = {
            'user': str(user),
            'permission': str(permission),
            'pk': str(trouble.pk),
            'reporter': str(trouble.reporter),
            'carer': str(trouble.carer),
            'carer_pk': str(trouble.carer.pk),
            'occur_date': trouble.occur_date.strftime("%Y/%m/%d %H:%M:%S"),
            'o_d_Y': trouble.occur_date.year,
            'o_d_m': trouble.occur_date.month,
            'o_d_d': trouble.occur_date.day,
            'o_d_H': trouble.occur_date.hour,
            'o_d_M': trouble.occur_date.minute,
            'o_d_S': trouble.occur_date.second,
            'occur_machine': trouble.occur_machine,
            'o_m_type': trouble.occur_machine[:2],
            'o_m_num': trouble.occur_machine[-2:],
            'trouble_user': str(trouble.trouble_user.stu_num),
            't_u_year': str(trouble.trouble_user.stu_num)[1:3],
            't_u_num': str(trouble.trouble_user.stu_num)[-3:],
            # 'category': str(trouble.category),
            'content': trouble.content,
            'approach': trouble.approach,
            'report_date': trouble.report_date.strftime("%Y/%m/%d %H:%M:%S"),
            }
        return JsonResponse(d)


@login_required
def auto_create_trouble_view(request):
    # sampleを追加するview
    # superuserのみ解放
    if request.user.is_superuser:
        if request.method == 'GET':
            return render(request, 'trouble/auto_create_trouble.html')
        elif request.method == 'POST':
            if request.POST.get('make_t_user'):
                make_trouble.make_trouble_user()
            
            if request.POST.get('make_trouble'):
                make_trouble.make_trouble()
            
            if request.POST.get('clear_trouble'):
                make_trouble.trouble_clear()

            if request.POST.get('make_recent_trouble'):
                make_trouble.make_recent_trouble()
                
            return HttpResponseRedirect(reverse('trouble:trouble_list'))
        else:
            return HttpResponseRedirect(reverse('trouble:trouble_list'))
    else:
        return HttpResponseRedirect(reverse('trouble:trouble_list'))
