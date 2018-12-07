from django.contrib import admin
from .models import author, article, category, comment

# Register your models here.
class authormodel(admin.ModelAdmin):
    list_display = ["__str__", "details"]
    search_fields = ["__str__"]
    class Meta:
        Model=author
admin.site.register(author, authormodel)

class categorymodel(admin.ModelAdmin):
    list_display = ["__str__"]
    search_fields = ["__str__"]
    class Meta:
        Model=category
admin.site.register(category, categorymodel)

class articlemodel(admin.ModelAdmin):
    list_display = ["__str__", "posted_on", "article_author"]
    search_fields = ["__str__", "title"]
    list_filter = ["posted_on", "category"]
    list_per_page = 15
    class Meta:
        Model=article
admin.site.register(article, articlemodel)

class commentmodel(admin.ModelAdmin):
    list_display = ["__str__", "post_comment"]
    # search_fields = ["__str__", "title"]
    # list_filter = ["posted_on", "category"]
    list_per_page = 15
    class Meta:
        Model=comment
admin.site.register(comment, commentmodel)