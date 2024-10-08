# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from .models import HomogenousProduct, HeterogenousProduct, CompanyRevenue

# @receiver(post_save, sender=HomogenousProduct)
# @receiver(post_delete, sender=HomogenousProduct)
# @receiver(post_save, sender=HeterogenousProduct)
# @receiver(post_delete, sender=HeterogenousProduct)
# def update_company_revenue(sender, instance, **kwargs):
#     company_revenue, created = CompanyRevenue.objects.get_or_create(company_id=instance.company_id)
#     company_revenue.save()
