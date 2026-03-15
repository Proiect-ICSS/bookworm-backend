from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta


class User(AbstractUser):
    address = models.CharField(
        max_length=255, help_text="Stable address in the city required."
    )
    is_approved = models.BooleanField(
        default=False, help_text="Admin must approve address."
    )

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="books"
    )
    description = models.TextField()
    book_file = models.FileField(upload_to="secure_books/")
    total_licenses = models.PositiveIntegerField(
        default=5, help_text="Max simultaneous readers"
    )
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def is_available(self):
        # calculates if there are copies left to borrow right now
        active_loans = self.loans.filter(returned=False).count()
        return active_loans < self.total_licenses


class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loans")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="loans")
    borrowed_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    returned = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id:
            # on creation, automatically set due date
            # for the book loan to two weeks from now
            self.due_date = timezone.now() + timedelta(days=14)
        super().save(*args, **kwargs)


class Waitlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="waitlist")
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["joined_at"]  # waitlist queue - first in, first out ordering


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 6)]
    )  # 1 to 5 stars
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Recommendation(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_recs")
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_recs"
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)


class BrowsingHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="history")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Browsing Histories"


class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "News"


class InfoPage(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)  # e.g., 'faq', 'terms'
    content = models.TextField()
