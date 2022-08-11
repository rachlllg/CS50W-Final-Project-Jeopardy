from django.contrib import admin

from .models import Jeopardy, Question, User, Subject, Category

# to change the display of Category model in admin
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('jeopardy', 'category')

# to add an id to each Jeopardy game
class JeopardyAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('subject', 'name', 'owner', 'date')

# to change the display of Question model in admin
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('category', 'cluevalue', "answered")

# register abstractuser with admin site
admin.site.register(User)

# register the Subject model with admin site
admin.site.register(Subject)

# register the Category model with admin site
admin.site.register(Category, CategoryAdmin)

# register the Jeopardy model with admin site
admin.site.register(Jeopardy, JeopardyAdmin)

# register the Questions model with admin site
admin.site.register(Question, QuestionAdmin)
