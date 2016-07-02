from django.contrib import admin

#from .models import User


#class UserAdmin(admin.ModelAdmin):
    #list_display = ('email', 'fullname')
    #list_filter = ('is_active', 'is_admin')
    #fields = [
        #'fullname',
        #'email',
        #'is_active',
        #'is_admin',
    #]

#admin.site.register(User, UserAdmin)

from .models import *
# Register your models here.
admin.site.register(Channel)
admin.site.register(Post)
admin.site.register(Comment)
