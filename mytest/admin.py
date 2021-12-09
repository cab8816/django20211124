from django.contrib import admin

# Register your models here.
from mytest.models import Publisher, Author, Book, Student, Studenta, Card, Person, Group, Membership


#
#
class BookAdmin(admin.ModelAdmin):
    list_display = ('title','publisher', 'publication_date')
    list_filter = ('publication_date',)
    date_hierarchy = 'publication_date'
    ordering = ('-publication_date',)
    filter_horizontal = ('authors',)
    raw_id_fields = ('publisher',)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name')


class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')


admin.site.register(Publisher,PublisherAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Student)
admin.site.register(Studenta)
admin.site.register(Card)
admin.site.register(Group)
admin.site.register(Person)
admin.site.register(Membership)

