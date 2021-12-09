from django.contrib import admin
from polls.models import Question, Choice


# Register your models here.
class ChoiceInline(admin.TabularInline):
# class ChoiceInline(admin.StackedInline):
    model = Choice
    extra=3
    fieldsets = [
        ('选择内容', {'fields': ['choice_text']}),

    ]


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text',  'pub_date','was_published_recently')
    fieldsets = [
        ('问题内容',{'fields':['question_text']}),
        ('日期信息',{'fields':['pub_date'],'classes':['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_filter = ['pub_date']

# class ChoiceAdmin(admin.ModelAdmin):
#     list_display = ('qestion', 'choice_text', 'votes')


admin.site.register(Question,QuestionAdmin)
# admin.site.register(Choice,ChoiceAdmin)
