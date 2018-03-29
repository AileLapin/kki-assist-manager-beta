from django.db import models
from account.models import MyUser


class TroubleUser(models.Model):
    class Meta:
        verbose_name = 'トラブルユーザ'
        verbose_name_plural = 'トラブルユーザ'

    stu_num = models.CharField(verbose_name='学籍番号', max_length=30, unique=True)
    last_name = models.CharField(verbose_name='苗字',
                                 max_length=30, default=None, null=True)
    first_name = models.CharField(verbose_name='名前',
                                  max_length=30, default=None, null=True)

    def __str__(self):
        return str(self.stu_num) + ' : ' + str(self.last_name) + ' ' + str(self.first_name)


class TroubleCategory(models.Model):
    class Meta:
        verbose_name = 'トラブルカテゴリ'
        verbose_name_plural = 'トラブルカテゴリ'

    title = models.CharField(verbose_name='タイトル', max_length=50)
    content = models.CharField(verbose_name='内容', max_length=300)
    approach = models.CharField(verbose_name='対処方法', max_length=300)

    def __str__(self):
        return str(self.title)


class Trouble(models.Model):
    class Meta:
        verbose_name = 'トラブル'
        verbose_name_plural = 'トラブル'

    reporter = models.ForeignKey(MyUser,
                                 verbose_name='報告者', on_delete=models.CASCADE,
                                 related_name='reporter_trouble_set')
    carer = models.ForeignKey(MyUser,
                              verbose_name='対処者', on_delete=models.CASCADE,
                              related_name='carer_trouble_set')

    occur_date = models.DateTimeField(verbose_name='発生日時')
    occur_machine = models.CharField(verbose_name='発生端末', max_length=4)
    trouble_user = models.ForeignKey(TroubleUser, on_delete=models.CASCADE)
    category = models.ForeignKey(TroubleCategory, verbose_name='カテゴリ',
                                 on_delete=models.CASCADE, null=True)
    content = models.CharField(verbose_name='内容', max_length=300)
    approach = models.CharField(verbose_name='対処方法', max_length=300)
    report_date = models.DateTimeField(verbose_name='報告日時')

    def __str__(self):
        return str(self.pk) + ' ' + str(self.reporter) + ' ' + str(self.content)


class TroubleDateReport(models.Model):
    # 1日に起きたトラブルを管理するモデル
    # date:日付, num:発生件数
    # troubles:その日起きたトラブル
    date = models.DateField()
    num = models.IntegerField()
    troubles = models.ManyToManyField(Trouble)

    def __str__(self):
        return str(self.date) + ' : ' + str(self.num)
