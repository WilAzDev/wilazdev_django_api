from django.db import models

class PasswordRecoveryChoises(models.TextChoices):
    RECOVERY = 'Recovery','Password Recovery'
    CHANGE = 'Change','Password Change'