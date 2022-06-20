from django.db import models
from django.contrib.auth.models import User



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, related_name= "following", blank= True)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    bio = models.TextField(default='.....')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def profiles_posts(self):
        return self.post_set.all()   #We can use related name or model_set

    def __str__(self):
        return str(self.user.username)

    class Meta:
        ordering = ('-created',)


