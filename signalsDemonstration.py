import time
import threading
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Post, UserStatistics

#Question 1:By default, Django signals are executed synchronously.
#Question 2: Django signals run in the same thread as the caller.
#Question 3: Django signals run in the same database transaction as the caller.
# The code shows how Django signals work. It's like a way to send messages between 
# different parts of your Django app. When something happens, like a new post being created,
# Django sends a signal. Other parts of your app can listen for these signals and do things in response.
# In this example, i have created two signals: one to notify the author of a new post and another to 
# update user statistics. Both signals run in the same order as the code that triggered them, 
# and they use the same database connection.

# Signal to notify the author when a new post is created
@receiver(post_save, sender=Post)
def notify_author_post_saved(sender, instance, created, **kwargs):
    if created:
        print("Signal started. Simulating delay to show synchronous behavior...")
        time.sleep(2)  # Simulating the delay

        # Check the current thread to prove signal runs in the same thread
        print(f"Signal running in thread: {threading.current_thread().name}")

        # Simulating sending an email to the author
        print(f"Sending email to {instance.author.email} about the new post '{instance.title}'.")
        # for sending actual mail
        # send_mail(
        #     'New Post Created',
        #     f"Hi {instance.author.username}, your post '{instance.title}' has been published.",
        #     'admin@blog.com',
        #     [instance.author.email],
        # )

# Signal to update user statistics when a new post is created
@receiver(post_save, sender=Post)
def update_user_statistics(sender, instance, created, **kwargs):
    if created:
        try:
            with transaction.atomic():
                print(f"Updating post count for {instance.author.username}...")

                user_stats, _ = UserStatistics.objects.get_or_create(user=instance.author)
                user_stats.post_count += 1
                user_stats.save()

                print(f"Post count updated to {user_stats.post_count} for {instance.author.username}.")
        except Exception as e:
            print(f"An error occurred: {e}. Rolling back transaction.")


#models

# from django.db import models
# from django.contrib.auth.models import User

# class Post(models.Model):
#     title = models.CharField(max_length=100)
#     content = models.TextField()
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

# class UserStatistics(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     post_count = models.IntegerField(default=0)
