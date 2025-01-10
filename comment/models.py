from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class Comment(models.Model):
    content = models.TextField("description")
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )  # Self-referential ForeignKey for nested replies
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, db_index=True)
    to_project = models.ForeignKey(
        "project.Project", blank=True, null=True, on_delete=models.CASCADE, related_name="comments"
    )
    total_replies = models.PositiveIntegerField(default=0)  # Cache for replies count

    def __str__(self):
        return self.content[:20]

    def update_reply_count(self):
        """
        Recursively update the total_replies count of all parent comments.
        """
        comment = self
        while comment:
            comment.total_replies = comment.replies.count()
            comment.save(update_fields=["total_replies"])
            comment = comment.parent


# Signals to update `total_replies` automatically
@receiver(post_save, sender=Comment)
def update_replies_on_save(sender, instance, created, **kwargs):
    """
    Update the reply count for the parent comment when a new comment is saved.
    """
    if created and instance.parent:
        instance.parent.update_reply_count()


@receiver(post_delete, sender=Comment)
def update_replies_on_delete(sender, instance, **kwargs):
    """
    Update the reply count for the parent comment when a comment is deleted.
    """
    if instance.parent:
        instance.parent.update_reply_count()
