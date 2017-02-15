#coding=utf-8
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect,JsonResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth.admin import  User
from django.contrib.auth.hashers import make_password
from .models import UsertoUrl,UsertoTopic,Topic,UsertoWord,Word,News,Word_Detail,Word_History
from .forms import EditUserForm
import time
import json
import os



import sys

file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/static/'

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/../SearchEngine')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/../')
import search
# Create your views here.

se=search.SearchEngine()
labelabbr= {'politics':'SZ', 'society':'SH', 'finance':'CJ', 'education':'JY', 'technology':'KJ', 'fashion':'SS', 'sports':'TY'}



def getNewsPage(request):
    if request.method != 'POST':
        return JsonResponse({'errorCode': 1, 'errorMsg': u'未知错误！'})
    else:
        # 将request.body=str 反序列化为字典并保存在request.POST中，这个偷懒了
        request.POST = json.loads(request.body)  # ['username']

        if 'page' not in request.POST or 'type' not in request.POST:
            return JsonResponse({'errorCode': 1, 'errorMsg': u'未知错误！'})

        page=request.POST.get('page',1)
        type=request.POST.get('type','all')

        if request.user.is_authenticated():
            # !!!待钱巨完善
            if type=='all':
                if page > 10:
                    page = 1
                with open(file_path+'readyStream.json','r') as f:
                    stream=json.load(f)['data']
                new={}
                new['data']=stream[30*(page-1):30*page]
                new['errorCode']=0
            else:
                if page>5:
                    page=1
                with open(file_path + 'readyStream_'+labelabbr[type]+'.json', 'r') as f:
                    stream = json.load(f)['data']
                new = {}
                new['data'] = stream[30 * (page - 1):30 * page]
                new['errorCode'] = 0

            return JsonResponse(new)

        else:

            if type=='all':
                if page > 10:
                    page = 1
                with open(file_path+'readyStream.json','r') as f:
                    stream=json.load(f)['data']
                new={}
                new['data']=stream[30*(page-1):30*page]
                new['errorCode']=0
            else:
                if page>5:
                    page=1
                with open(file_path + 'readyStream_'+labelabbr[type]+'.json', 'r') as f:
                    stream = json.load(f)['data']
                new = {}
                new['data'] = stream[30 * (page - 1):30 * page]
                new['errorCode'] = 0

            return JsonResponse(new)



def getGraph(request):
    if request.method!='GET':
        return JsonResponse({'errorCode': 1, 'errorMsg': u'未知错误！'})
    else:
        with open(file_path+'graph_index.json','r') as f:
            graph=json.load(f)
        return JsonResponse({'errorCode':0,'data':graph})


def getSearchGraph(request):
    if request.method!='POST':
        return JsonResponse({'errorCode': 1, 'errorMsg': u'未知错误！'})
    else:
        request.POST = json.loads(request.body)
        graph=se.search_return_graph(request.POST['search'])
        return JsonResponse({'errorCode':0,'data':graph})

def getSearchNews(request):
    if request.method!='POST':
        return JsonResponse({'errorCode': 1, 'errorMsg': u'未知错误！'})
    else:
        request.POST = json.loads(request.body)
        newslist=se.search_return_list(request.POST['search'])
        return JsonResponse({'errorCode':0,'data':newslist})

def getHotWords(request):
    if request.method!='GET':
        return JsonResponse({'errorCode': 1, 'errorMsg': u'未知错误！'})
    else:
        with open(file_path+'words.json','r') as f:
            words = json.load(f)
        return    JsonResponse(words)

@login_required
def postUserClick(request):
    if request.method != 'POST':
        return JsonResponse({'errorCode': 1, 'errorMsg': u'未知错误！'})
    else:

        return JsonResponse({'errorCode': 1, 'errorMsg': u'未知错误！'})

