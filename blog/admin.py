from django.contrib import admin
from .models import Post,Tag,Category

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'create_time', 'modified_time', 'category', 'author']


admin.site.register(Post,PostAdmin)
admin.site.register(Tag)
admin.site.register(Category)
