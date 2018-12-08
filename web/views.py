from django.shortcuts import render
from .models import Article
from django.utils.safestring import mark_safe
find = None
allType = []
Month = {'1': "Jan.", '2': "Feb.", '3': "Mar.", '4': "Apr.", '5': "May.", '6': "Jun.", '7': "Jul.",
                '8': "Aug.", '9': "Sep.", '10': "Oct.", '11': "Nov.", '12': "Dec."}


def summary():
    global allType
    allData = Article.objects.all()
    for item in allData:
        allType.append(item.type)
    allType = list(set(allType))


def Paging():
    global find, allType
    context = {}
    pageList = []
    data = find[0:5]
    for item in data:
        date = item.time.strftime("%Y-%m-%d").split('-')
        if date:
            item.year = date[0]
            item.mon = Month[date[1]]
            item.day = date[2]
    dataLen = len(find)
    count, y = divmod(dataLen, 5)
    if y:
        count += 1
    for i in range(1, count+1):
        temp = '<a href="/profile/?p=%s">%s</a>'%(i, i)
        pageList.append(temp)

    pageStr = "".join(pageList)
    pageStr = mark_safe(pageStr)

    context['pageStr'] = pageStr
    context['find'] = data
    context['allType'] = allType
    return context

def Type(request, type):
    global find
    find = Article.objects.filter(type=type)
    if find:
        context = Paging()
        return render(request, 'web/profile.html', context)
    else:
        print('No Found!')
        return render(request, 'web/error.html')


def profile(request):
    global find, allType
    context = {}
    if request.method == 'POST':
        if request.POST.get("type"):
            return Type(request, request.POST.get("type"))
    if request.method == 'GET':
        if request.GET.get("s"):
            find = Article.objects.filter(title__contains=request.GET.get("s"))
            if find:
                context = Paging()
                return render(request, 'web/profile.html', context)
            else:
                print('No Found!')
                return render(request, 'web/error.html')
        if request.GET.get("p"):
            page = int(request.GET.get("p", 1))
            start = (page-1) * 5
            end = page * 5
            data = find[start:end]
            for item in data:
                date = item.time.strftime("%Y-%m-%d").split('-')
                if date:
                    item.year = date[0]
                    item.mon = Month[date[1]]
                    item.day = date[2]
            dataLen = len(find)
            count, y = divmod(dataLen, 5)
            pageList = []
            if y:
                count += 1
            for i in range(1, count + 1):
                temp = '<a href="/profile/?p=%s">%s</a>' % (i, i)
                pageList.append(temp)

            pageStr = "".join(pageList)
            pageStr = mark_safe(pageStr)
            context['find'] = data
            context['pageStr'] = pageStr
            context['allType'] = allType
            return render(request, 'web/profile.html', context)

    summary()
    find = Article.objects.all()
    if find:
        context = Paging()
        return render(request, 'web/profile.html', context)
    else:
        print('No Found!')
        return render(request, 'web/error.html')



def detail(request, key):
    if request.method == 'POST':
        if request.POST.get("type"):
            return Type(request, request.POST.get("type"))
    context = {}
    find = Article.objects.filter(id=key)[0]
    if find:
        date = find.time.strftime("%Y-%m-%d").split('-')
        if date:
            find.year = date[0]
            find.mon = Month[date[1]]
            find.day = date[2]
        context['allType'] = allType
        context['find'] = find
        return render(request, 'web/detail.html', context)
    else:
        return render(request, 'web/error.html')

