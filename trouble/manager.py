'''
Trouble一覧の取得やそのソート，検索に使う．
'''

import datetime
from trouble.models import (TroubleUser, TroubleCategory,
                            Trouble, TroubleDateReport)


def add_trouble_to_report(trouble):
    # 渡されたTroubleを発生日のTroubleDateReportに追加する
    occur_date = trouble.occur_date.date()  # 発生日を取得

    try:
        # TroubleDateReportを取得
        date_report = TroubleDateReport.objects.get(date=occur_date)
    except TroubleDateReport.DoesNotExist:
        # 無ければ作る
        date_report = TroubleDateReport(date=occur_date, num=0)
        date_report.save()

    # 発生件数を増やす
    # 引数で渡されたtroubleを発生日のTroubleReportに追加する
    date_report.num += 1
    date_report.save()
    if not date_report.troubles.filter(pk=trouble.pk).exists():
        # トラブルがレポートに追加されていなければ追加
        date_report.troubles.add(trouble)
    else:
        # トラブルが既にレポートに存在していれば例外
        raise ValueError('trouble already exists')


def trouble_delete(trouble):
    report = trouble.troubledatereport_set.all().first()
    report.num -= 1
    report.save()


def get_recent_troubles(length=7):
    # 直近のトラブルレポートを返す
    # 引数のlengthによって取り出す期間を設定する．
    # デフォルトは直近7日
    date = datetime.date.today() - datetime.timedelta(days=length)  # 条件日時を取得
    # 直近~日のReportを取り出して，日付の最新順に並べる
    reports = TroubleDateReport.objects.filter(date__gt=date).order_by('-date')

    # Reportの中のtroublesを発生日時順にソートしてReportオブジェクトを辞書形式に．
    # 空のtroublesリストに追加していく．
    # troubles = [{'date': ~, 'num': ~, 'troubles': Trouble-queryset}, {}, ... ,{}]
    troubles = []
    for report in reports:
        dic = {'date': report.date, 'num': report.num}
        dic['troubles'] = report.troubles.order_by('-occur_date')
        troubles.append(dic)
    return troubles
