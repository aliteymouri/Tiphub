from django.contrib.contenttypes.fields import GenericRelation
from persiantools.jdatetime import JalaliDate
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from hitcount.models import HitCount
from django.utils import timezone
from django.urls import reverse
from Account.models import User
from django.db import models


class Category(models.Model):
    title = models.CharField("عنوان دسته بندی مرجع ", max_length=50, unique=True)
    created_at = models.DateTimeField("تاریخ ایجاد در ", auto_now_add=True)

    def __str__(self):
        return self.title

    def get_jalali_date(self):
        return JalaliDate(self.created_at, locale=('fa')).strftime('%c')

    get_jalali_date.short_description = 'تاریخ ایجاد در'

    class Meta:
        verbose_name = "دسته بندی مرجع"
        verbose_name_plural = "دسته بندی های مرجع "


class SubCategory(models.Model):
    category = models.ManyToManyField(Category, related_name="subcategories", verbose_name="زیرمجموعه دسته بندی ")
    title = models.CharField("عنوان دسته بندی ", max_length=50, unique=True)
    is_active = models.BooleanField("وضعیت ", default=True)
    slug = models.SlugField("آدرس اسلاگ ", unique=True, allow_unicode=True, null=True, blank=True)
    created_at = models.DateTimeField("تاریخ ایجاد در ", auto_now_add=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super(SubCategory, self).save()

    def __str__(self):
        return F"{self.title}"

    def get_jalali_date(self):
        return JalaliDate(self.created_at, locale=('fa')).strftime('%c')

    get_jalali_date.short_description = 'تاریخ ایجاد در'

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"


class Video(models.Model):
    title = models.CharField("عنوان ویدیو", max_length=100, )
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="منتشر کننده",related_name='videos')
    category = models.ManyToManyField(SubCategory, related_name='videos', verbose_name="دسته بندی ویدیو")
    video = models.FileField("آپلود ویدیو", upload_to='videos/')
    description = RichTextField("درباره ویدئو")
    video_cover = models.ImageField("بنر ویدیو", upload_to='banner')
    tags = TaggableManager('تگ ها')
    time = models.CharField("تایم ویدیو", blank=True, null=True, max_length=15)
    likes_count = models.BigIntegerField("تعداد لایک ها", default=0)
    views = GenericRelation(HitCount, object_id_field='object_pk',
                            related_query_name='hit_count_generic_relation', verbose_name='تعداد بازدید')

    slug = models.SlugField("آدرس اسلاگ", unique=True, allow_unicode=True, null=True, blank=True)
    is_active = models.BooleanField("وضعیت ", default=True)
    created_at = models.DateTimeField("تاریخ انتشار در ", auto_now_add=True)
    updated_on = models.DateTimeField("تاریخ بروزرسانی در ", auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super(Video, self).save()

    def __str__(self):
        return F" عنوان ویدیو : {self.title}"

    def get_jalali_date(self):
        return JalaliDate(self.created_at, locale=('fa')).strftime('%c')

    get_jalali_date.short_description = 'تاریخ انتشار در'

    def get_absolute_url(self):
        return reverse('video:video_detail', args=(self.slug,))

    class Meta:
        verbose_name = "ویدیو"
        verbose_name_plural = "ویدیوها"


class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments', verbose_name="ویدیو")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name="کاربر")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies',
                               verbose_name="زیرمجموعه")
    text = models.TextField("متن کامنت ", )
    is_active = models.BooleanField("وضعیت", default=True)
    created_at = models.DateTimeField("تاریخ ثبت در ", auto_now_add=True)

    def __str__(self):
        return F' نظر : {self.text[:30]} / توسط : {self.author.fullname}'

    def get_date(self):
        if self.created_at is not None:
            time = timezone.now() - self.created_at
            s = time.seconds
            if time.days > 30 or time.days < 0:
                return JalaliDate(self.created_at, locale=('fa')).strftime('%c')  # After 30 days it will be show
            elif time.days >= 1:
                return '{} روز پیش '.format(time.days)
            elif s < 60:
                return '{} ثانیه پیش '.format(s)
            elif s <= 3600:
                return '{} دقیقه پیش '.format(round(s / 60))
            else:
                return '{} ساعت پیش '.format(round(s / 3600))
        else:
            return None

    get_date.short_description = "تاریخ ثبت در"

    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"
        ordering = ('-created_at',)


class Like(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="likes", verbose_name="ویدیو")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes", verbose_name="کاربر")
    created_at = models.DateField("تاریخ ثبت در", auto_now_add=True)

    def __str__(self):
        return F'  ویدیوی  : {self.video.title} توسط  : {self.user.fullname}'

    class Meta:
        verbose_name = "لایک "
        verbose_name_plural = "لایک ها"
        ordering = ("-created_at",)


class Favorite(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="favorites", verbose_name="ویدیو")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites", verbose_name="کاربر")
    created_at = models.DateField("تاریخ ثبت در", auto_now_add=True)

    def __str__(self):
        return F'  ویدیوی  : {self.video.title} توسط  : {self.user.fullname}'

    class Meta:
        verbose_name = "علاقه مندی "
        verbose_name_plural = "علاقه مندی ها"
        ordering = ("-created_at",)
