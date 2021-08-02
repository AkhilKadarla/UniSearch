import pprint

from django.shortcuts import render
from youtubesearchpython import Search
from django.http import JsonResponse
from googlesearch import search
max_limit_queries = 10

def index(request):
    return render(request,"hello.html")


def youtube(term):
    res = []
    kee_list = ["type","title","publishedTime","link","duration"]
    resp = Search(term, limit=max_limit_queries).result()["result"]
    for i in range(len(resp)):
        temp = {}
        for j in kee_list:
            try:
                temp.update({j:resp[i][j]})
            except:
                temp.update({j:"N/A"})
        res.append(temp)
    return res

def google(term):
    return search(term,num_results=max_limit_queries)

def get_intent(sentence):
    # loading the english language small model of spacy
    return sentence

def medium(term):
    return search(term='{} "site:medium.com"'.format(term),num_results=max_limit_queries)

def search_orig(request):
    res = {}
    for i in request.GET:
        if "sources" in i and request.GET.getlist(i)[0]=="true":
            res.update({i:[]})
            for j in request.GET.getlist("query"):
                if i=="youtube":
                    res[i].extend(youtube(j))
                elif i=="google":
                    res[i].extend(google(j))
                elif i=="medium":
                    res[i].extend(medium(j))

    return JsonResponse(res,safe=False)