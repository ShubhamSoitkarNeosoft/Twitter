from django.db import models
from users.models import Profile
from django.contrib.auth.models import User



class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete= models.CASCADE)
    body = models.TextField()
    liked = models.ManyToManyField(User, default = None, blank = True, related_name ='liked')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.body)[:30]

    @property
    def num_likes(self):
        return str(self.body)[:30]

    class Meta:
        ordering = ('-created',)
    
LIKE_CHOICES = (
    ('Like','Like'),
    ('Unlike','Unlike'),
)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default = 'Like',max_length=10)

    def __str__(self):
        return str(self.post)

class Comment(models.Model): 
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=255, null=True)
    body = models.TextField() 
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True) 
    active = models.BooleanField(default=True) 

    class Meta: 
        ordering = ('created',) 

    def __str__(self): 
        return 'Comment by {} on {}'.format(self.user, self.post) 

