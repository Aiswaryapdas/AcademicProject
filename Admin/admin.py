from django.contrib import admin
from .models import ReviewSchedule

@admin.register(ReviewSchedule)
class ReviewScheduleAdmin(admin.ModelAdmin):
    list_display = ('review_topic', 'review_date', 'review_time', 'review_status', 'remarks', 'created_at', 'updated_at')
    list_filter = ('review_status', 'review_date')
    search_fields = ('review_topic', 'remarks')
