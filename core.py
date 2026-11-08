"""作者：Wangyuan；日期：2026-10-29；职责：显式薪资参数的工作时间估算，不含个人工资。"""
from decimal import Decimal
from datetime import datetime,timedelta

def run(payload):
    if not isinstance(payload,dict):raise TypeError('输入必须为对象')
    salary=Decimal(str(payload['monthly_salary']));days=Decimal(str(payload['workdays']));hours=Decimal(str(payload['work_hours']))
    if not all(v.is_finite() for v in [salary,days,hours]) or salary<0 or days<=0 or hours<=0:raise ValueError('参数须有限且天数/时长为正')
    start=datetime.fromisoformat(payload['start']);now=datetime.fromisoformat(payload['now']);pause=float(payload.get('break_minutes',0))
    if not 0<=pause<=240:raise ValueError('休息时间无效')
    minutes=float(hours*60);break_at=min(max(180,minutes/2),max(0,minutes-pause))
    end=start+timedelta(minutes=minutes+pause);a=start+timedelta(minutes=break_at);b=a+timedelta(minutes=pause)
    raw=max(0,min((now-start).total_seconds(),(end-start).total_seconds()))
    rest=max(0,(min(now,end,b)-max(start,a)).total_seconds())
    effective=max(0,min(raw-rest,minutes*60));fraction=Decimal(str(effective))/Decimal(str(minutes*60))
    return {'effective_seconds':effective,'progress':float(fraction),'earned_estimate':str((salary/days*fraction).quantize(Decimal('0.01'))),'daily_estimate':str((salary/days).quantize(Decimal('0.01'))),'is_break':a<=now<b,'notice':'按输入估算，并非实发薪酬或薪酬凭据。'}
