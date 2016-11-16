from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.safestring  import mark_safe
from markdown_deux import markdown
# Create your models here.


def upload_location(instance,filename):
    return "%s/%s" %(instance.id,filename)
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=120)
    # slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_location,null =True, blank=True,width_field="width_field",height_field="height_field")
    height_field=models.IntegerField(default=0)
    width_field=models.IntegerField(default=0)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("newsletter:detail", kwargs={"id":self.id})
        # return "/newsletter/%s/" %(self.id)


    class Meta:
        ordering = ["-timestamp","-updated"]

    def get_markdown(self):
        content = self.content
        return mark_safe(markdown(content))
