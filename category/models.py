from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.


class Category(MPTTModel):
    category_name = models.CharField(max_length=50, unique=True, verbose_name="Thể loại")
    slug = models.SlugField(max_length=100, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children', verbose_name="Thể loại cha")

    class Meta:
        verbose_name = 'Thể loại'
        verbose_name_plural = 'Thể loại'

    def __str__(self):
        return self.category_name
