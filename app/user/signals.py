# from django.conf import settings
# from django.db.models.signals import pre_save, post_save
# from django.contrib.auth.signals import user_logged_in
# from django.dispatch import receiver
# from rest_framework.authtoken.models import Token


# before model is saved
# @receiver(pre_save, sender=settings.AUTH_USER_MODEL)
# def update_iuser(sender, instance=None,**kwargs):
#     # instance: an actual object
#     user = instance

#     if user.email != '':
#         user.username = user.email


# when user is created/updated
# receiver: The callback function which will be connected to this signal
# The create_auth_token func will only be called after an instance (user)
# of AUTH_USER_MODEL is saved.
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)


# # when user is logged in
# @receiver(user_logged_in, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, request, user, **kwargs):
#         Token.objects.create(user=user)
