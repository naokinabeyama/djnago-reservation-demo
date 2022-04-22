from django.db import models


class Reservations(models.Model):
    id = models.AutoField(primary_key=True)
    last_name = models.CharField(verbose_name='氏名（姓）', max_length=15)
    first_name = models.CharField(verbose_name='氏名（名）', max_length=15)
    reservation_date = models.DateTimeField(verbose_name='予約日時')
    reservation_count = models.IntegerField(verbose_name='予約人数')
    tell = models.CharField(verbose_name='電話番号', max_length=12)
    celebration_existence = models.IntegerField(verbose_name='お祝い有無')
    demand = models.TextField(verbose_name='要望',null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='登録日時')
    update_at = models.DateTimeField(verbose_name='更新日時')

    class Meta:
        db_table = 'reservations'
    
    def __str__(self):
        return self.last_name + self.first_name
