from datetime import datetime, date, timedelta
from django.utils import timezone
import pytz
from account.models import MyUser
from trouble.models import (TroubleUser, TroubleCategory,
                            Trouble, TroubleDateReport)
from . import manager


def make_trouble_user():
    for i in range(1, 65):
        TroubleUser.objects.create(
            stu_num='t13cs{0:03d}'.format(i),
            last_name='hoge{}'.format(i),
            first_name='fuge{}'.format(i)
            )
    print('success!')


def time():
    time = datetime.now()-datetime.timedelta(days=1, hours=(1+3) % 12)
    print(time)


def make_trouble():
    reporter = MyUser.objects.exclude(is_staff=True)
    machine = ['aw', 'bw', 'cw']
    i = -1
    for t_user in TroubleUser.objects.all():
        i += 1
        for j in range(0, 3):
            time = datetime.now()-timedelta(days=i, hours=(i*j) % 12)
            trouble = Trouble(
                reporter=reporter[j],
                carer=reporter[j],
                occur_date=time,
                occur_machine='{0}0{1}'.format(machine[j], j),
                trouble_user=t_user,
                content='sample',
                approach='sample',
                report_date=datetime.now()
                )
            trouble.save()
            manager.add_trouble_to_report(trouble)
            print(trouble)

    print('success!')


def make_recent_trouble(length=7):
    reporter = MyUser.objects.exclude(is_staff=True)
    machine = ['dw', 'ew', 'fw']
    for i in range(0, length):
        t_user = TroubleUser.objects.all()[i]
        for j in range(0, 3):
            time = datetime.now()-timedelta(days=i, hours=j*3)
            trouble = Trouble(
                reporter=reporter[j],
                carer=reporter[(i % 2)],
                occur_date=time,
                occur_machine='{0}0{1}'.format(machine[j], (i+1)),
                trouble_user=t_user,
                content='sample',
                approach='sample',
                report_date=datetime.now()-timedelta(days=i)
                )
            trouble.save()
            manager.add_trouble_to_report(trouble)
            print(trouble)

    print('success!')


def trouble_user_clear():
    for user in TroubleUser.objects.all():
        user.delete()
    print('success!')


def trouble_clear():
    for trouble in Trouble.objects.all():
        print(trouble)
        manager.trouble_delete(trouble)
    print('success!')


def report_clear():
    for report in TroubleDateReport.objects.all():
        report.delete()
    print('success!')


def main():
    make_trouble()
    print('success!')


if __name__ == '__main__':
    main()
