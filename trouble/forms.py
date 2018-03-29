from django.utils import timezone
from datetime import date, datetime
from django import forms
from .models import Trouble, TroubleCategory, TroubleUser
from account.models import MyUser


YEAR_CHOICES = tuple([(i, i) for i in range(2017, int(str(date.today().year))+1)])
MONTH_CHOICES = tuple([(i, i) for i in range(1, 13)])
DAY_CHOICES = tuple([(i, i) for i in range(1, 32)])
HOUR_CHOICES = tuple([(i, i) for i in range(1, 25)])
MINUTE_CHOICES = tuple([(i, i) for i in range(1, 61)])

# aw ~ kw までのタプルを生成 => ((aw, aw), (bw, bw), .... , (kw, kw))
# 学籍番号の年の部分を生成 => ((12, 12), (13, 13), .... , (18, 18))
# 学籍番号の番号の部分を生成 => ((01, 01), (02, 02), .... , (100, 100))
MACHINE_TYPE_CHOICES = tuple([(chr(i)+'w', chr(i)+'w') for i in range(97, 97+11)])
MACHINE_NUMBER_CHOICES = tuple([('{0:02d}'.format(i), '{0:02d}'.format(i)) for i in range(1, 13)])
TROUBLE_USER_YEAR_CHOICES = tuple([(i, i) for i in range(13, int(str(date.today().year)[-2:])+1)])
TROUBLE_USER_NUM_CHOICES = tuple([('{0:03d}'.format(i), '{0:03d}'.format(i)) for i in range(1, 101)])


class TroubleForm(forms.Form):
    carer = forms.ModelChoiceField(label='対処者',
                                   queryset=MyUser.objects.exclude(is_staff=True))
    year = forms.ChoiceField(label='年',
                             choices=YEAR_CHOICES)
    month = forms.ChoiceField(label='月',
                              choices=MONTH_CHOICES)
    day = forms.ChoiceField(label='日',
                            choices=DAY_CHOICES)
    hour = forms.ChoiceField(label='時',
                             choices=HOUR_CHOICES)
    minute = forms.ChoiceField(label='分',
                               choices=MINUTE_CHOICES)
    occur_machine_type = forms.ChoiceField(label='発生端末',
                                           choices=MACHINE_TYPE_CHOICES)
    occur_machine_num = forms.ChoiceField(label='',
                                          choices=MACHINE_NUMBER_CHOICES)
    trouble_user_year = forms.ChoiceField(label='使用者',
                                          choices=TROUBLE_USER_YEAR_CHOICES)
    trouble_user_num = forms.ChoiceField(label='',
                                         choices=TROUBLE_USER_NUM_CHOICES)
    category = forms.ModelChoiceField(label='カテゴリ', required=False,
                                      queryset=TroubleCategory.objects.all())
    content = forms.CharField(label='内容', widget=forms.Textarea)
    approach = forms.CharField(label='内容', widget=forms.Textarea)

    def assemble(self, form, user, obj=None):
        # セレクトボックスなどで受け取ったデータを組み立て，Troubleインスタンスを生成し保存する
        # objが渡された場合，そのオブジェクトに対して変更をする．
        # 戻り値として，作成されたTroubleオブジェクトを返す
        carer = form.cleaned_data['carer']
        year = form.cleaned_data['year']
        month = form.cleaned_data['month']
        day = form.cleaned_data['day']
        hour = form.cleaned_data['hour']
        minute = form.cleaned_data['minute']
        d_list = [year, month, day, hour, minute]
        d_time = '/'.join(d_list)
        occur_date = datetime.strptime(d_time, '%Y/%m/%d/%H/%M')
        occur_machine = form.cleaned_data['occur_machine_type'] + form.cleaned_data['occur_machine_num']
        trouble_user_num = 't' + form.cleaned_data['trouble_user_year'] + 'cs' + form.cleaned_data['trouble_user_num']

        try:
            trouble_user = TroubleUser.objects.get(stu_num=trouble_user_num)
        except:
            # 該当ユーザが存在しない場合新しく作る
            trouble_user = TroubleUser(stu_num=trouble_user_num)
            trouble_user.save()

        category = form.cleaned_data['category']
        content = form.cleaned_data['content']
        approach = form.cleaned_data['approach']

        if obj is None:
            obj = Trouble(reporter=user, carer=carer, occur_date=occur_date,
                          occur_machine=occur_machine, trouble_user=trouble_user,
                          category=category, content=content, approach=approach,
                          report_date=timezone.now())
        else:
            obj.carer = carer
            obj.occur_date = occur_date
            obj.occur_machine = occur_machine
            obj.trouble_user = trouble_user
            obj.category = category
            obj.content = content
            obj.approach = approach

        obj.save()
        return obj


class TroubleCreateForm(TroubleForm):
    pass


class TroubleUpdateForm(TroubleForm):
    def __init__(self, trouble, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TroubleUserForm(forms.ModelForm):
    class Meta:
        model = TroubleUser
        fields = ['stu_num', 'last_name', 'first_name']


class TroubleCategoryForm(forms.ModelForm):
    class Meta:
        model = TroubleCategory
        fields = ['title', 'content', 'approach']
        widgets = {'content': forms.Textarea(attrs={'cols': 60, 'rows': 5}),
                   'approach': forms.Textarea(attrs={'cols': 60, 'rows': 5})}
