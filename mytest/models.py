from django.db import models

# Create your models here.
from django.utils.datetime_safe import datetime


class Xie_authorManager(models.Manager):
    def get_queryset(self):
        return super(Xie_authorManager, self).get_queryset().filter(first_name='谢')


class Xie_publisherManager(models.Manager):
    def get_queryset(self):
        return super(Xie_publisherManager, self).get_queryset().filter(name='谢')


class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()
    publisher = models.Manager()
    xie = Xie_publisherManager()


class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField()
    author = models.Manager()
    xie = Xie_authorManager()

    def cherryforxie(self):
        if self.first_name == '谢':
            return self.last_name


class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    publication_date = models.DateField()


# 在模型类内部定义选择，并为每个值定义一个合适的名称的常量
class Studenta(models.Model):
    FRESHMAN = 'FR'
    SOPHOMORE = 'SO'
    JUNIOR = 'JR'
    SENIOR = 'SR'
    GRADUATE = 'GR'
    YEAR_IN_SCHOOL_CHOICES = [
        (FRESHMAN, 'Freshmana'),
        (SOPHOMORE, 'Sophomorea'),
        (JUNIOR, 'Juniora'),
        (SENIOR, 'Seniora'),
        (GRADUATE, 'Graduatea'),
    ]
    year_in_school = models.CharField(
        max_length=2,
        choices=YEAR_IN_SCHOOL_CHOICES,
        default=FRESHMAN,
    )


# Django 还提供了枚举类型，你可以通过将其子类化来简洁地定义选择
from django.utils.translation import gettext_lazy as _


class Student(models.Model):
    class YearInSchool(models.TextChoices):
        FRESHMAN = 'FR', _('Freshman')
        SOPHOMORE = 'SO', _('Sophomore')
        JUNIOR = 'JR', _('Junior')
        SENIOR = 'SR', _('Senior')
        GRADUATE = 'GR', _('Graduate')

    year_in_school = models.CharField(
        max_length=2,
        choices=YearInSchool.choices,
        default=YearInSchool.SENIOR,
    )

    def is_upperclass(self):
        return self.year_in_school in {
            self.YearInSchool.JUNIOR,
            self.YearInSchool.SENIOR,
        }


# 由于枚举值需要为整数的情况极为常见，Django 提供了一个 IntegerChoices 类
class Card(models.Model):
    cardno = models.IntegerField(db_index=True, default=1)

    class Suit(models.IntegerChoices):
        DIAMOND = 1
        SPADE = 2
        HEART = 3
        CLUB = 4

    suit = models.IntegerField(
        choices=Suit.choices,
        default=Suit.SPADE,
    )


#
# class Landdate(models.Model):
#     # date = models.DateField(auto_now=True)
#
#     class MoonLandings(datetime.date, models.Choices):
#         APOLLO_11 = 1969, 7, 20, 'Apollo 11 (Eagle)'
#         APOLLO_12 = 1969, 11, 19, 'Apollo 12 (Intrepid)'
#         APOLLO_14 = 1971, 2, 5, 'Apollo 14 (Antares)'
#         APOLLO_15 = 1971, 7, 30, 'Apollo 15 (Falcon)'
#         APOLLO_16 = 1972, 4, 21, 'Apollo 16 (Orion)'
#         APOLLO_17 = 1972, 12, 11, 'Apollo 17 (Challenger)'
#     moonland = models.DateField(choices=MoonLandings)


class Person(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through='Membership')

    def __str__(self):
        return self.name


class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)
