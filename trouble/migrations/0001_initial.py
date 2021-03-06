# Generated by Django 2.0.2 on 2018-02-28 15:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Trouble',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('occur_date', models.DateField(verbose_name='発生日時')),
                ('occur_machine', models.CharField(max_length=4, verbose_name='発生端末')),
                ('content', models.CharField(max_length=300, verbose_name='内容')),
                ('approach', models.CharField(max_length=300, verbose_name='対処方法')),
                ('report_date', models.DateField(verbose_name='報告日時')),
                ('carer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carer_trouble_set', to=settings.AUTH_USER_MODEL, verbose_name='対処者')),
            ],
            options={
                'verbose_name': 'トラブル',
                'verbose_name_plural': 'トラブル',
            },
        ),
        migrations.CreateModel(
            name='TroubleCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='タイトル')),
                ('content', models.CharField(max_length=300, verbose_name='内容')),
                ('approach', models.CharField(max_length=300, verbose_name='対処方法')),
            ],
            options={
                'verbose_name': 'トラブルカテゴリ',
                'verbose_name_plural': 'トラブルカテゴリ',
            },
        ),
        migrations.CreateModel(
            name='TroubleUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stu_num', models.CharField(max_length=30, verbose_name='学籍番号')),
                ('last_name', models.CharField(default=None, max_length=30, null=True, verbose_name='苗字')),
                ('first_name', models.CharField(default=None, max_length=30, null=True, verbose_name='名前')),
            ],
            options={
                'verbose_name': 'トラブルユーザ',
                'verbose_name_plural': 'トラブルユーザ',
            },
        ),
        migrations.AddField(
            model_name='trouble',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='trouble.TroubleCategory', verbose_name='カテゴリ'),
        ),
        migrations.AddField(
            model_name='trouble',
            name='reporter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reporter_trouble_set', to=settings.AUTH_USER_MODEL, verbose_name='報告者'),
        ),
        migrations.AddField(
            model_name='trouble',
            name='trouble_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trouble.TroubleUser'),
        ),
    ]
