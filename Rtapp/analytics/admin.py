from django.contrib import admin
# from .models import Students, Schools






# admin.site.register(Students)
# admin.site.register(Schools)

# @admin.register(Students)
# class StudentAdmin(admin.ModelAdmin):
    
#     fields = ('name', 'score', 'age', 'school')
#     list_display = ('id', 'name', 'age', 'score', 'school')
#     list_display_links = ('id',)
#     search_fields = ('name', 'age')
#     list_filter = ('name', 'age', 'score', 'school')
#     list_editable = ('name', 'age', 'score', 'school')


# @admin.register(Schools)
# class SchoolsAdmin(admin.ModelAdmin):
#     list_display = ('name', 'student_count')

#     def student_count(self, obj):
#         # print(type(obj))
#         # print(dir(obj))
#         count = obj.students_set.count()
#         return count
    
#     student_count.short_description = '生徒数'