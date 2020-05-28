from django.db import models

# Create your models here.  	


class redditdata(models.Model):
	keyword = models.CharField(max_length=100, blank=True, null=True)
	title = models.TextField(blank = True,  null=True)
	all_date = models.TextField(blank = True,  null=True)
	score = models.TextField(blank = True,  null=True)
	id_id = models.TextField(blank = True,  null=True)
	url = models.TextField(blank = True,  null=True)
	created = models.TextField(blank = True,  null=True)
	body = models.TextField(blank = True,  null=True)
	
	def __str__(self):
  		return self.keyword
  		return 'Memo={0}, Tag={1}'.format(self.keyword, self.url)

