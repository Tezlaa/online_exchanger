from django.contrib import admin

from .models import Feedbacks


class AdminFeedback(admin.ModelAdmin):
    list_display = ('feedback_text', 'send_time', )
    list_editable = ('feedback_text', )
    list_display_links = None
    

admin.site.register(Feedbacks, AdminFeedback)