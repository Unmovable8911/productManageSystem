from django.db import models
import uuid, os

# Create your models here.
class Catagory(models.Model):
    identity = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        editable=False
    )
    title = models.CharField(
        blank=False, null=False,
        max_length=50,
        verbose_name="标题"
    )

    def __str__(self):
        return self.title


def picture_upload_dir(instance, filename):
    return f"pictures/{instance.catagory.title}/{instance.name}"

def thumnail_upload_dir(instance, filename):
    return f"thumnails/{instance.catagory.title}/{instance.name}"

class Product(models.Model):
    identity = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_comment="primary_key",
    )
    name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        db_comment="名称",
        verbose_name="名称",
        unique=True
    )
    catagory = models.ForeignKey(
        Catagory,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        db_comment="类别",
        verbose_name="类别"
    )
    purchase_price = models.DecimalField(
        max_digits=4,
        blank=True,
        null=True,
        decimal_places=1,
        db_comment="进价(元)",
        verbose_name="进价(元)"
    )
    price = models.DecimalField(
        max_digits=4,
        blank=False,
        null=False,
        decimal_places=1,
        db_comment="单价(元)",
        verbose_name="单价(元)"
    )
    unit = models.CharField(
        max_length=5,
        blank=False,
        null=False,
        db_comment="单位",
        verbose_name="单位",
        choices = [
            ("个", "个"),
            ("袋", "袋"),
            ("瓶", "瓶"),
            ("本", "本"),
            ("把", "把"),
            ("件", "件"),
            ("匝", "匝"),
            ("条", "条"),
            ("支", "支"),
            ('根', '根'),
            ('桶', '桶'),
            ('捆', '捆'),
            ('盒', '盒'),
            ('箱', '箱'),
            ('米', '米'),
            ('斤', '斤'),
            ('两', '两')
        ]
    )
    manufacture_date = models.DateField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
        db_comment="生产日期",
        verbose_name="生产日期"
    )
    shelf_life = models.SmallIntegerField(
        blank=True,
        null=True,
        db_comment="保质期",
        verbose_name="保质期单位",
    )
    shelf_life_unit = models.CharField(
        max_length=2,
        blank=True,
        null=True,
        db_comment="保质期单位",
        choices=[("月", "月"), ("天", "天")]
    )
    expire_date = models.DateField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
        db_comment="过期日期",
        verbose_name="过期日期"
    )
    picture = models.ImageField(
        upload_to=picture_upload_dir,
        null=True,
        blank=True,
        db_comment="图片",
        verbose_name="图片"
    )
    thumnail = models.ImageField(
        upload_to=thumnail_upload_dir,
        blank=True,
        null=True,
        db_comment= "小图片",
        verbose_name="图片"
    )
    remark = models.CharField(
        blank=True,
        null=True,
        max_length=200,
        db_comment="备注",
        verbose_name="备注"
    )

    def delete(self, *args, **kwargs):
        if self.picture:
            picture_path = self.picture.path
            thumnail_path = self.thumnail.path
            if os.path.exists(picture_path):
                os.remove(picture_path)
            if os.path.exists(thumnail_path):
                os.remove(thumnail_path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name
