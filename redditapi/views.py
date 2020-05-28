from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import *
from datetime import datetime,timedelta,date
import pandas as pd
import praw
import nltk
# nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
nltk.download('vader_lexicon')
from redditapi.serializers import *

title=[]
url=[]
score=[]
created=[]
id_id=[]
all_date=[]
body=[]


class StAPIView(APIView):
	def get(self, request,format=None):
		
		all_keys = request.query_params.get('keyword',None)
		start_date = request.query_params.get('start_date',None)
		end_date = request.query_params.get('end_date',None)
		z=redditdata.objects.filter(keyword=all_keys).exists()
		if z==True:
			reddit = praw.Reddit(client_id = 'GZ4wXpp55Rzjqw',
							client_secret = 'nusWMTnlf0nLWOHWDcFcFi1RXQY',
							user_agent = 'data')
			print("fffsafasfasfsafasfasfsfasdsdasdasdasdasdsada",all_keys)
			data=redditdata.objects.filter(keyword=all_keys)
			print(data)
			global title, score, url, created, id_id, all_date, body
			for i in data:
				print("jai",i.score)
				print(i.keyword)
				print(i.all_date)
				print(i.body)
				
				title.append(i.title)
				score.append(i.score)
				url.append(i.url)
				created.append(i.created)
				id_id.append(i.id_id)
				all_date.append(i.all_date)
				body.append(i.body)

			print("scorescorescorescorescorescorescore",score,len(score),len(url),len(created),len(id_id),len(body))
			
			topics_dict={'Title':title,'Score':score,'id':id_id,'Url':url,'Created':created,'Date Time':all_date,'Body':body}
			df = pd.DataFrame(topics_dict)
			print(df)
			all_comments=[]
			
			for ids in df.id:
				# print("idsidsidsidsidsidsidsidsidsidsids",ids)
				each_subreddit_comments=[]
				for top_level_comment in reddit.submission(id=ids).comments:
					each_subreddit_comments.append(top_level_comment.body)
				all_comments.append(each_subreddit_comments)  
				each_subreddit_comments=[]
			sid = SentimentIntensityAnalyzer()
			final_sentiments_list = []
			entered = 0
			for each_ in all_comments:
				sentiments_list = []    
				for every_comment in each_:
					entered=1
					polarity_dict  = sid.polarity_scores(every_comment)
					negative = polarity_dict['neg']
					positive = polarity_dict['pos']
					neutral = polarity_dict['neu']
					if negative>positive and negative>neutral:
						sentiments_list.append('negative')
						continue
					if positive>negative and positive>neutral:
						sentiments_list.append('positive')
						continue
					if neutral>positive and neutral> positive:
						sentiments_list.append('neutral')
						continue
					if positive == negative:
						sentiments_list.append('neutral')
						continue
				final_sentiments_list.append(sentiments_list)  
			df['Comments'] = all_comments
			df['Sentiments'] = final_sentiments_list
			df2 = (df['Date Time'] > start_date) & (df['Date Time'] <= end_date)
			df2=df.loc[df2]
			print(df2)
			return Response(df2)
		else:
			print("This keyword is not exists in database please run post api")
			return Response("This keyword is not exists in database please run post api")
			









class postredditapi(APIView):
	def post(self, request, format=None):
		keyword = request.data.get('keyword',None)
		print("ffdf",keyword)
		# z=redditdata.objects.filter(keyword=keyword).exists()
		# print("zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz",z)

		reddit = praw.Reddit(client_id = 'GZ4wXpp55Rzjqw',
						client_secret = 'nusWMTnlf0nLWOHWDcFcFi1RXQY',
						user_agent = 'data')
		keywords = keyword
		title =[]
		score=[]
		id_=[]
		url=[] 
		created=[]
		body=[]
		all_date = []
		key=[]
		for submission in reddit.subreddit(keywords).top('all'):
			title.append(submission.title)
			score.append(submission.score)
			id_.append(submission.id)
			url.append(submission.url)
			created.append(submission.created)
			body.append(submission.selftext)
			all_date.append(datetime.fromtimestamp(submission.created))
		# print(title)
		for i in range(len(body)):
			key.append(keywords)

		print(len(title),len(id_),len(score),len(url),len(created),len(body),len(all_date),len(key))

		for a,b,c,d,e,f,g,h in zip(key,title,all_date,score,id_,url,created,body):
			# print(a,b,c,d,e,f,g,h)
			z=redditdata.objects.filter(id_id=e).exists()
			print(z)
			if z==True:
				print(z)
				continue
			else:
				data_save = redditdata(keyword=a,title=b,all_date=c, score=d,id_id=e,
					url=f,created=g,body=h)
				data_save.save()
				print("saved successfully")
		return Response("keyword is updated")