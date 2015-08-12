from django.contrib import admin
from django.db.models.loading import get_models, get_app

# from dataportal3 import models
# from old import models

# Register your models here.


# class ImageSanityAdmin(admin.ModelAdmin):
#     raw_id_fields = ("image",)

# admin.site.register(Tag, ImageSanityAdmin)

for model in get_models(get_app('dataportal3')):
    try:
        admin.site.register(model)
    except:
        pass


for model in get_models(get_app('old')):
    try:
        admin.site.register(model)
    except:
        pass