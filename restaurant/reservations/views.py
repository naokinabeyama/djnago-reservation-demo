from django.http import request
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .models import Reservations
from .forms import ReservationForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    DeleteView
)
from datetime import datetime
import datetime as dt
from django.core.paginator import (
    Paginator, EmptyPage, PageNotAnInteger
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required



# 予約登録
def ReservationView(request):
    form = ReservationForm(request.POST or None)

    if form.is_valid():
        reservation = Reservations()
        # 氏名（姓）
        reservation.last_name = form.cleaned_data['last_name']
        # 氏名（名）
        reservation.first_name = form.cleaned_data['first_name']
        # 予約日時
        reservation.reservation_date = day_time_value(form.cleaned_data['reservation_day'], form.cleaned_data['reservation_time'])
        # 予約人数
        reservation.reservation_count = form.cleaned_data['reservation_count']
        # 電話番号
        reservation.tell = form.cleaned_data['tell']
        # お祝い
        if form.cleaned_data['celebration_existence']:
            reservation.celebration_existence = 1
        else:
            reservation.celebration_existence = 0
        # お店への要望
        reservation.demand = form.cleaned_data['demand']

        # 登録
        Reservations.objects.create(
            last_name = reservation.last_name,
            first_name = reservation.first_name,
            reservation_date = reservation.reservation_date,
            reservation_count = reservation.reservation_count,
            tell = reservation.tell,
            celebration_existence = reservation.celebration_existence,
            demand = reservation.demand,
            created_at = datetime.now(),
            update_at = datetime.now(),
        )
        return redirect('users:home')
    return render(request, 'store/reservation.html', {'form': form})
    
    

# 予約一覧
class ReservationsListView(LoginRequiredMixin,    ListView):
    model = Reservations
    template_name = 'store/reservationsList.html'
    # 5件ずつ
    paginate_by = 5

    # 検索機能
    def get_queryset(self):
        query = super().get_queryset()
        # 予約ID
        reservation_id = self.request.GET.get('id', None)
        # 氏名（姓）
        last_name = self.request.GET.get('last_name', None)
        # 氏名（名）
        first_name = self.request.GET.get('first_name', None)
        # 予約日時間（先）
        start_day_time = str(self.request.GET.get('start_day', None)) + ' ' + '00:00:00'
        # 予約日時間（後）
        end_day_time = str(self.request.GET.get('end_day', None)) + ' ' + '23:59:59'
        # 予約日（先）
        start_day = self.request.GET.get('start_day', None)
        # 予約日（後）
        end_day = self.request.GET.get('end_day', None)
        # 予約人数
        reservation_count = self.request.GET.get('reservation_count', None)
        # 電話番号
        tell = self.request.GET.get('tell', None)
        # 予約受付日
        created_at = self.request.GET.get('created_at', None)
        
        # 検索フィルター
        # ID
        if reservation_id:
            query = query.filter(
                id = reservation_id
            )

        # 氏名（姓）
        if first_name:
            query = query.filter(
                first_name__contains = first_name
            )

        # 氏名（名）
        if last_name:
            query = query.filter(
                last_name__contains = last_name
            )

        # 予約日時
        if start_day and end_day:
            query = query.filter(
                reservation_date__range = [start_day_time, end_day_time]
            ).order_by('reservation_date')
        elif start_day:
            query = query.filter(
                reservation_date__gte = start_day_time
            ).order_by('reservation_date')
        elif end_day:
            query = query.filter(
                reservation_date__lte = end_day_time
            ).order_by('reservation_date')

        # 予約人数
        if reservation_count:
            query = query.filter(
                reservation_count = reservation_count
            )

        # 電話番号
        if tell:
            query = query.filter(
                tell = tell
            )

        # 予約受付日
        if created_at:
            query = query.filter(
                created_at__contains = created_at
            )
        
        # ページネーション
        paginator = Paginator(query, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            paginator.page(page)
        except PageNotAnInteger:
            paginator.page(1)
        except EmptyPage:
            paginator.page(paginator.num_pages)

        return query
    
    # template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ID
        context['id'] = self.request.GET.get('id', '')
        # 氏名（姓）
        context['last_name'] = self.request.GET.get('last_name', '')
        # 氏名（名）
        context['first_name'] = self.request.GET.get('first_name', '')
        # 予約日from
        context['start_day'] = self.request.GET.get('start_day', '')
        # 予約日to
        context['end_day'] = self.request.GET.get('end_day', '')
        # 予約人数
        context['reservation_count'] = self.request.GET.get('reservation_count', '')
        # 電話番号
        context['tell'] = self.request.GET.get('tell', '')
        # 予約受付日
        context['created_at'] = self.request.GET.get('created_at', '')
        return context



# 予約詳細
class ReservationDetailView(LoginRequiredMixin, DetailView):
    model = Reservations
    template_name = 'store/reservationDetail.html'

    # template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 予約日時
        context['time'] = time_view(self.object.reservation_date)
        # お祝い
        if self.object.celebration_existence == 0:
            context['celebration_existence'] = 'なし'
        elif self.object.celebration_existence == 1:
            context['celebration_existence'] = 'あり'

        return context



# 予約更新
@login_required
def ReservationUpdateView(request, pk):
    # 予約ID情報
    reservation_data = Reservations.objects.get(id=pk)
    # 初期表示
    if request.method == 'GET':
        # お祝い
        if reservation_data.celebration_existence == 1:
            reservation_data.celebration_existence = True
        else:
            reservation_data.celebration_existence = False
        # 予約日と予約時間
        day_time = reservation_data.reservation_date + dt.timedelta(hours=9)
        day = day_time.strftime('%Y-%m-%d')
        time = day_time.strftime('%H:%M:%S')

        item = {
            'last_name': reservation_data.last_name,
            'first_name': reservation_data.first_name,
            'reservation_day': day,
            'reservation_time': time,
            'reservation_count': reservation_data.reservation_count,
            'tell': reservation_data.tell,
            'celebration_existence': reservation_data.celebration_existence,
            'demand': reservation_data.demand
        }
        form = ReservationForm(initial=item)
    # 更新
    else:
        form = ReservationForm(request.POST or None)
        if form.is_valid():
            # 予約ID情報
            reservation = Reservations.objects.get(id=pk)
            # 氏名（姓）
            reservation.last_name = form.cleaned_data['last_name']
            # 氏名（姓）
            reservation.first_name = form.cleaned_data['first_name']
            # 予約日時
            reservation.reservation_date = day_time_value(form.cleaned_data['reservation_day'], form.cleaned_data['reservation_time'])
            # 予約人数
            reservation.reservation_count = form.cleaned_data['reservation_count']
            # 電話番号
            reservation.tell = form.cleaned_data['tell']
            # お祝い
            if form.cleaned_data['celebration_existence']:
                reservation.celebration_existence = 1
            else:
                reservation.celebration_existence = 0
            # お店への要望
            reservation.demand = form.cleaned_data['demand']
            # 保存
            reservation.save()
            return redirect('reservations:reservationDetail', pk=pk)
    return render(request, 'store/reservationUpdate.html', context = {
        'form': form,
        'reservation': reservation_data,
    })



# 予約削除
class ReservationDeleteView(LoginRequiredMixin, DeleteView):
    model = Reservations
    template_name = 'store/reservationDelete.html'
    success_url = reverse_lazy('reservations:reservationsList')
    # template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 予約日時
        context['time'] = time_view(self.object.reservation_date)
        # お祝い
        if self.object.celebration_existence == 0:
            context['celebration_existence'] = 'なし'
        elif self.object.celebration_existence == 1:
            context['celebration_existence'] = 'あり'

        return context







# ---------    メソッド    ---------


# 日と時間を足してdatetime型に変換
def day_time_value(day, time):
    day_time = day + ' ' + time
    day_time = datetime.strptime(day_time, '%Y-%m-%d %H:%M:%S')
    return day_time



# 時間の表示変換
def time_view(time):
    # プラス9時間
    time_nine = time + dt.timedelta(hours=9)
    # ％H：％Mに変換
    time_hm = str(time_nine.hour) + ':' + str(time_nine.minute) + '0'
    time_change = ''
    if time_hm == '11:00':
        time_change = str(time_hm) + ' ' + '~' + ' ' + '15:00'
    elif time_hm == '15:00':
        time_change = str(time_hm) + ' ' + '~' + ' ' + '17:00'
    elif time_hm == '17:00':
        time_change = str(time_hm) + ' ' + '~' + ' ' + '19:00'
    elif time_hm == '19:00':
        time_change = str(time_hm) + ' ' + '~' + ' ' + '21:00'
    elif time_hm == '21:00':
        time_change = str(time_hm) + ' ' + '~' + ' ' + '23:00'
    return time_change
