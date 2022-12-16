from django.contrib import admin

from store.models import Author, DetailInventory, Image, Product, Promotion, PublicCompany, ReviewRating, Supplier
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    search_fields = ('product_name',)
    filter_horizontal = ('author',)
    list_display = ('product_name', 'getPriceFormatVND',
                    'quantity', 'category', 'image_tag','modified_date', 'is_available',)
    prepopulated_fields = {'slug': ('product_name', )}
    readonly_fields = ('quantity', )


class PublicCompanyAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('name',)
    list_display = ('name', )
    prepopulated_fields = {'slug': ('name', )}


class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', )
    prepopulated_fields = {'slug': ('name', )}


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', )
    prepopulated_fields = {'slug': ('name', )}


# class ImageAdmin(admin.ModelAdmin):
#     list_display = ('images', 'product')


class DetailInventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'supplier', 'amount')


class PromotionAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date', 'discount')


class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'comment', "rating")
    # prepopulated_fields = {'slug': ('rating', )}



admin.site.register(Product, ProductAdmin)
admin.site.register(PublicCompany, PublicCompanyAdmin)
admin.site.register(Author, AuthorAdmin)
# admin.site.register(Image, ImageAdmin)
admin.site.register(DetailInventory, DetailInventoryAdmin)
admin.site.register(Promotion, PromotionAdmin)
admin.site.register(ReviewRating, ReviewRatingAdmin)
admin.site.register(Supplier, SupplierAdmin)