from django.db import models


class Feedbacks(models.Model):
    """Feadbacks, last send time feadbacks in the telegram bot"""
    
    feedback_text = models.TextField(verbose_name='Текст отзыва', null=True)
    send_time = models.DateTimeField(verbose_name='Время последней отправки', null=True, blank=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        
    def __str__(self):
        text_feedback = str(self.feedback_text)
        plural = "..." if len(text_feedback) > 15 else ""
        
        return f'Отзыв: {text_feedback[:15]}{plural}'