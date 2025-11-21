from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Q
from datetime import datetime, timedelta
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from .models import Devotee, Sabha, Attendance
import pandas as pd
from collections import defaultdict

@login_required
@user_passes_test(lambda u: u.is_superuser)
def reports_dashboard(request):
    """Main reports dashboard - admin only"""
    context = {
        'sabha_types': [('bal', 'Bal Sabha'), ('yuvak', 'Yuvak Sabha'), 
                       ('mahila', 'Mahila Sabha'), ('sanyukt', 'Sanyukt Sabha')],
        'title': 'Reports & Analytics Dashboard'
    }
    return render(request, 'attendance/reports_dashboard.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def sabha_wise_report(request):
    """Sabha-wise attendance analytics"""
    sabha_type = request.GET.get('sabha_type')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    # Build query
    query = {}
    if sabha_type:
        query['sabha_type'] = sabha_type
    if date_from:
        query.setdefault('date', {})['$gte'] = date_from
    if date_to:
        query.setdefault('date', {})['$lte'] = date_to
    
    # Get sabhas using Django ORM
    sabhas_query = Sabha.objects.all().order_by('-date')
    if sabha_type:
        sabhas_query = sabhas_query.filter(sabha_type=sabha_type)
    if date_from:
        sabhas_query = sabhas_query.filter(date__gte=date_from)
    if date_to:
        sabhas_query = sabhas_query.filter(date__lte=date_to)
    
    sabha_stats = []
    for sabha in sabhas_query:
        attendance_records = Attendance.objects.filter(sabha=sabha)
        
        total = attendance_records.count()
        present = attendance_records.filter(status='present').count()
        absent = attendance_records.filter(status='absent').count()
        late = attendance_records.filter(status='late').count()
        
        sabha_stats.append({
            'sabha': sabha,
            'total': total,
            'present': present,
            'absent': absent,
            'late': late,
            'attendance_rate': round((present / total * 100) if total > 0 else 0, 1)
        })
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'sabha_stats': sabha_stats})
    
    context = {
        'sabha_stats': sabha_stats,
        'filters': {'sabha_type': sabha_type, 'date_from': date_from, 'date_to': date_to},
        'sabha_types': [('bal', 'Bal Sabha'), ('yuvak', 'Yuvak Sabha'), 
                       ('mahila', 'Mahila Sabha'), ('sanyukt', 'Sanyukt Sabha')]
    }
    return render(request, 'attendance/sabha_wise_report.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def mandal_wise_report(request):
    """Mandal-wise attendance summary"""
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    # Build sabha query
    query = {}
    if date_from:
        query.setdefault('date', {})['$gte'] = date_from
    if date_to:
        query.setdefault('date', {})['$lte'] = date_to
    
    sabhas_query = Sabha.objects.all()
    if date_from:
        sabhas_query = sabhas_query.filter(date__gte=date_from)
    if date_to:
        sabhas_query = sabhas_query.filter(date__lte=date_to)
    
    mandal_stats = defaultdict(lambda: {'total': 0, 'present': 0, 'absent': 0, 'late': 0, 'sabhas': 0})
    
    for sabha in sabhas_query:
        mandal = sabha.mandal or 'Unknown'
        attendance_records = Attendance.objects.filter(sabha=sabha)
        
        mandal_stats[mandal]['sabhas'] += 1
        mandal_stats[mandal]['total'] += attendance_records.count()
        mandal_stats[mandal]['present'] += attendance_records.filter(status='present').count()
        mandal_stats[mandal]['absent'] += attendance_records.filter(status='absent').count()
        mandal_stats[mandal]['late'] += attendance_records.filter(status='late').count()
    
    # Calculate attendance rates
    for mandal, stats in mandal_stats.items():
        if stats['total'] > 0:
            stats['attendance_rate'] = round((stats['present'] / stats['total'] * 100), 1)
        else:
            stats['attendance_rate'] = 0
    
    context = {
        'mandal_stats': dict(mandal_stats),
        'filters': {'date_from': date_from, 'date_to': date_to}
    }
    return render(request, 'attendance/mandal_wise_report.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def xetra_wise_report(request):
    """Xetra-wise attendance summary"""
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    # Build sabha query
    query = {}
    if date_from:
        query.setdefault('date', {})['$gte'] = date_from
    if date_to:
        query.setdefault('date', {})['$lte'] = date_to
    
    sabhas_query = Sabha.objects.all()
    if date_from:
        sabhas_query = sabhas_query.filter(date__gte=date_from)
    if date_to:
        sabhas_query = sabhas_query.filter(date__lte=date_to)
    
    xetra_stats = defaultdict(lambda: {'total': 0, 'present': 0, 'absent': 0, 'late': 0, 'sabhas': 0})
    
    for sabha in sabhas_query:
        xetra = sabha.xetra or 'Unknown'
        attendance_records = Attendance.objects.filter(sabha=sabha)
        
        xetra_stats[xetra]['sabhas'] += 1
        xetra_stats[xetra]['total'] += attendance_records.count()
        xetra_stats[xetra]['present'] += attendance_records.filter(status='present').count()
        xetra_stats[xetra]['absent'] += attendance_records.filter(status='absent').count()
        xetra_stats[xetra]['late'] += attendance_records.filter(status='late').count()
    
    # Calculate attendance rates
    for xetra, stats in xetra_stats.items():
        if stats['total'] > 0:
            stats['attendance_rate'] = round((stats['present'] / stats['total'] * 100), 1)
        else:
            stats['attendance_rate'] = 0
    
    context = {
        'xetra_stats': dict(xetra_stats),
        'filters': {'date_from': date_from, 'date_to': date_to}
    }
    return render(request, 'attendance/xetra_wise_report.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def attendance_trends(request):
    """Weekly/Monthly attendance trends with charts"""
    period = request.GET.get('period', 'weekly')  # weekly or monthly
    sabha_type = request.GET.get('sabha_type')
    
    # Get data for last 12 weeks or 12 months
    today = datetime.now().date()
    trends = []
    
    if period == 'weekly':
        for i in range(12):
            week_start = today - timedelta(weeks=i+1)
            week_end = today - timedelta(weeks=i)
            
            # Get sabhas in this week
            sabhas_query = Sabha.objects.filter(date__gte=week_start, date__lte=week_end)
            if sabha_type:
                sabhas_query = sabhas_query.filter(sabha_type=sabha_type)
            
            if sabhas_query.exists():
                attendance_records = Attendance.objects.filter(sabha__in=sabhas_query)
                present_count = attendance_records.filter(status='present').count()
                total_count = attendance_records.count()
            else:
                present_count = 0
                total_count = 0
            
            trends.append({
                'period': f"Week {week_start.strftime('%m/%d')}",
                'present': present_count,
                'total': total_count,
                'rate': round((present_count / total_count * 100) if total_count > 0 else 0, 1)
            })
    
    trends.reverse()  # Show oldest to newest
    
    # Generate chart
    chart_data = generate_trend_chart(trends, period)
    
    context = {
        'trends': trends,
        'chart_data': chart_data,
        'period': period,
        'sabha_type': sabha_type,
        'sabha_types': [('bal', 'Bal Sabha'), ('yuvak', 'Yuvak Sabha'), 
                       ('mahila', 'Mahila Sabha'), ('sanyukt', 'Sanyukt Sabha')]
    }
    return render(request, 'attendance/attendance_trends.html', context)

def generate_trend_chart(trends, period):
    """Generate matplotlib chart for attendance trends"""
    if not trends:
        return None
    
    periods = [t['period'] for t in trends]
    rates = [t['rate'] for t in trends]
    
    plt.figure(figsize=(12, 6))
    plt.plot(periods, rates, marker='o', linewidth=2, markersize=6)
    plt.title(f'{period.title()} Attendance Trends', fontsize=16, fontweight='bold')
    plt.xlabel('Period', fontsize=12)
    plt.ylabel('Attendance Rate (%)', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Convert to base64 string
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    buffer.seek(0)
    chart_data = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    
    return chart_data

@login_required
@user_passes_test(lambda u: u.is_superuser)
def devotee_attendance_history(request):
    """Individual devotee attendance history"""
    devotee_id = request.GET.get('devotee_id')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    if not devotee_id:
        return render(request, 'attendance/devotee_history_search.html')
    
    # Get devotee info
    try:
        devotee = Devotee.objects.get(devotee_id=devotee_id)
    except Devotee.DoesNotExist:
        return render(request, 'attendance/devotee_history_search.html', 
                     {'error': 'Devotee not found'})
    
    # Build attendance query
    attendance_query = Attendance.objects.filter(devotee=devotee)
    if date_from:
        attendance_query = attendance_query.filter(sabha__date__gte=date_from)
    if date_to:
        attendance_query = attendance_query.filter(sabha__date__lte=date_to)
    
    # Get attendance records
    attendance_records = attendance_query.select_related('sabha').order_by('-marked_at')
    
    # Calculate stats
    total_records = attendance_records.count()
    present_count = attendance_records.filter(status='present').count()
    attendance_rate = round((present_count / total_records * 100) if total_records > 0 else 0, 1)
    
    context = {
        'devotee': devotee,
        'attendance_records': attendance_records,
        'stats': {
            'total': total_records,
            'present': present_count,
            'absent': attendance_records.filter(status='absent').count(),
            'late': attendance_records.filter(status='late').count(),
            'attendance_rate': attendance_rate
        },
        'filters': {'date_from': date_from, 'date_to': date_to}
    }
    return render(request, 'attendance/devotee_attendance_history.html', context)