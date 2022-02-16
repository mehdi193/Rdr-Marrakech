from django.contrib import admin

# Register your models here.

from accueil.models import blog, tags, blogTags

admin.site.register(blog)
admin.site.register(tags)
admin.site.register(blogTags)