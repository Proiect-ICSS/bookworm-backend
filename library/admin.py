from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User,
    Category,
    Book,
    Loan,
    Waitlist,
    Review,
    Recommendation,
    BrowsingHistory,
    News,
    InfoPage,
)

admin.site.register(User, UserAdmin)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # columns that show up in the books admin view
    list_display = ("title", "author", "category", "total_licenses", "added_date")
    list_filter = ("category",)  # adds a filter sidebar for searching by category
    search_fields = ("title", "author")  # adds a search bar


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ("book", "user", "borrowed_at", "due_date", "returned")
    list_filter = ("returned", "due_date")


@admin.register(InfoPage)
class InfoPageAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Waitlist)
admin.site.register(Review)
admin.site.register(Recommendation)
admin.site.register(BrowsingHistory)
admin.site.register(News)
