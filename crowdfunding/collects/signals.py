from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DonationRecord, Collect

@receiver(post_save, sender=DonationRecord)
def update_collect_on_donation(sender, instance, created, **kwargs):
    if created:
        collect = instance.collect
        collect.collected_amount += instance.amount
        collect.donors_count += 1
        collect.save()
