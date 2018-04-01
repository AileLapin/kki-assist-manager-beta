from django.http import Http404
from django.urls import reverse
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from account.models import MyUser
from .forms import LoginForm


class Index(LoginRequiredMixin, generic.TemplateView):
    template_name = "account/index.html"


class MyLoginView(LoginView):
    template_name = 'account/login.html'
    form_class = LoginForm


class MyLogoutView(LogoutView):
    pass


class MyAccountUpdate(LoginRequiredMixin, generic.edit.UpdateView):
    model = MyUser
    fields = ('last_name', 'first_name', 'nickname')
    template_name = 'account/update.html'
    user = None  # ログインしているユーザオブジェクトを格納
    success_url = 'account:login'

    def get(self, request, *args, **kwargs):
        self.user = request.user  # アクセスしてきたユーザを格納
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.user = request.user  # アクセスしてきたユーザを格納
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('accout:login')

    def get_object(self, queryset=None):
        try:
            # Get the single item from the filtered queryset
            obj = self.user  # フォームの初期値はログインユーザ
        except queryset.model.DoesNotExist:
            raise Http404(("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj


class UserUpdate(LoginRequiredMixin, generic.edit.UpdateView):
    model = MyUser
    fields = ('last_name', 'first_name', 'nickname')
    queryset = MyUser.objects.all()
    template_name = 'account/update.html'

    def get_success_url(self):
        return reverse('account:index')

    def get_object(self, queryset=None):
        """
        Return the object the view is displaying.

        Require `self.queryset` and a `pk` or `slug` argument in the URLconf.
        Subclasses can override this to return any object.
        """
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()

        # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(stu_num=pk)

        # Next, try looking up by slug.
        if slug is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})

        # If none of those are defined, it's an error.
        if pk is None and slug is None:
            raise AttributeError("Generic detail view %s must be called with "
                                 "either an object pk or a slug."
                                 % self.__class__.__name__)

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj


class PasswordChangeView(PasswordChangeView):
    template_name = 'account/password_change.html'

    def get_success_url(self):
        return reverse('account:login')
