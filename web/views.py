from django.shortcuts import render
from .models import Article
from django.utils.safestring import mark_safe

Month = {'01': "Jan", '02': "Feb", '03': "Mar", '04': "Apr", '05': "May", '06': "Jun", '07': "Jul",
         '08': "Aug", '09': "Sep", '10': "Oct", '11': "Nov", '12': "Dec"}


def recent():
    find = Article.objects.all()
    recentFind = []
    recentFind.append(find.last())
    x = find.filter(pk=find.last().pk - 1)
    if x:
        recentFind.append(find.filter(pk=find.last().pk - 1)[0])
    y = find.filter(pk=find.last().pk - 2)
    if y:
        recentFind.append(find.filter(pk=find.last().pk - 2)[0])
    for item in recentFind:
        date = item.time.strftime("%Y-%m-%d").split('-')
        if date:
            item.year = date[0]
            item.mon = Month[date[1]]
            item.day = date[2]
    return recentFind


def summary():
    allType = []
    allData = Article.objects.all()
    for item in allData:
        allType.append(item.type)
    allType = sorted(set(allType), key=allType.index)
    return allType


def Paging(page=1, find=None, articleType=None):
    pageNum = 3
    context = {}
    start = (page - 1) * pageNum
    end = page * pageNum
    data = find[start:end]
    for item in data:
        date = item.time.strftime("%Y-%m-%d").split('-')
        if date:
            item.year = date[0]
            item.mon = Month[date[1]]
            item.day = date[2]
    dataLen = len(find)

    pageCount, y = divmod(dataLen, pageNum)
    pageList = []
    if y:
        pageCount += 1

    if pageCount < pageNum:
        startIndex = 1
        endIndex = pageCount + 1
    else:
        if page <= (pageNum + 1) / 2:
            startIndex = 1
            endIndex = pageNum + 1
        else:
            startIndex = page - (pageNum - 1) / 2
            endIndex = page + (pageNum + 1) / 2
            if (page + (pageNum - 1) / 2) > pageCount:
                endIndex = pageCount + 1
                startIndex = pageCount - pageNum + 1
    if articleType:
        if page == 1:
            prev = '<li><a href="javascript:void(0);">&laquo;</a></li>'
        else:
            prev = '<li><a href="/web/blogHome/?type=%s&p=%s">&laquo;</a></li>' % (articleType, page - 1)
        pageList.append(prev)
        for i in range(int(startIndex), int(endIndex)):
            if i == page:
                temp = '<li><a class="active" href="/web/blogHome/?type=%s&p=%s">%s</a></li>' % (articleType, i, i)
            else:
                temp = '<li><a href="/web/blogHome/?type=%s&p=%s">%s</a></li>' % (articleType, i, i)
            pageList.append(temp)
        if page == pageCount:
            nex = '<li><a href="javascript:void(0);">&raquo;</a></li>'
        else:
            nex = '<li><a href="/web/blogHome/?type=%s&p=%s">&raquo;</a></li>' % (articleType, page + 1)
        pageList.append(nex)

        jump = """
            <input type="text"  class="jump" /><button class="btn btn-default" onclick='jumpTo(this, "/web/blogHome/?type=%s&p=");' id="jumpPageNum">Go</button>
            <script>
                function jumpTo(ths, base){
                    var val = ths.previousSibling.value;
                    location.href = base + val;
                }
            </script>
        """%(articleType)
        pageList.append(jump)

        pageStr = "".join(pageList)
        pageStr = mark_safe(pageStr)
        allType = summary()
        context['find'] = data
        context['pageStr'] = pageStr
        context['allType'] = allType
        return context
    else:
        if page == 1:
            prev = '<li><a href="javascript:void(0);">&laquo;</a></li>'
        else:
            prev = '<li><a href="/web/blogHome/?p=%s">&laquo;</a></li>' % (page - 1)
        pageList.append(prev)
        for i in range(int(startIndex), int(endIndex)):
            if i == page:
                temp = '<li><a class="active" href="/web/blogHome/?p=%s">%s</a></li>' % (i, i)
            else:
                temp = '<li><a href="/web/blogHome/?p=%s">%s</a></li>' % (i, i)
            pageList.append(temp)
        if page == pageCount:
            nex = '<li><a href="javascript:void(0);">&raquo;</a></li>'
        else:
            nex = '<li><a href="/web/blogHome/?p=%s">&raquo;</a></li>' % (page + 1)
        pageList.append(nex)

        jump = """
            <input type="text"  class="jump" /><button class="btn btn-default" onclick='jumpTo(this, "/web/blogHome/?p=");' id="jumpPageNum">Go</button>
            <script>
                function jumpTo(ths, base){
                    var val = ths.previousSibling.value;
                    location.href = base + val;
                }
            </script>
        """
        pageList.append(jump)

        pageStr = "".join(pageList)
        pageStr = mark_safe(pageStr)
        allType = summary()
        context['find'] = data
        context['pageStr'] = pageStr
        context['allType'] = allType
        return context


def Type(request, page=1, articleType=None):
    find = Article.objects.filter(type=articleType)
    if find:
        context = Paging(page, find, articleType)
        recentFind = recent()
        context['recentFind'] = recentFind
        return render(request, 'web/blogHome.html', context)
    else:
        return render(request, 'web/error.html')


def profile(request):
    context = {}
    find = Article.objects.all()
    newfind = recent()
    if find:
        context['find'] = newfind
        return render(request, 'web/profile.html', context)
    else:
        return render(request, 'web/error.html')


def detail(request, key):
    if request.method == 'POST':
        if request.POST.get("type"):
            return Type(request, 1, request.POST.get("type"))
    context = {}
    find = Article.objects.filter(id=key)[0]
    if find:
        date = find.time.strftime("%Y-%m-%d").split('-')
        if date:
            find.year = date[0]
            find.mon = Month[date[1]]
            find.day = date[2]
        allType = summary()
        context['allType'] = allType
        context['find'] = find
        allArticle = Article.objects.all()
        recentFind = recent()
        context['recentFind'] = recentFind
        return render(request, 'web/detail.html', context)
    else:
        return render(request, 'web/error.html')


def blogHome(request):
    context = {}
    if request.method == 'POST':
        if request.POST.get("type"):
            return Type(request, 1, request.POST.get("type"))
    if request.method == 'GET':
        if request.GET.get("s"):
            find = Article.objects.filter(title__contains=request.GET.get("s"))
            if find:
                context = Paging(1, find)
                return render(request, 'web/blogHome.html', context)
            else:
                return render(request, 'web/error.html')
        if request.GET.get("p"):
            if request.GET["type"]:
                page = int(request.GET.get("p", 1))
                print(page, request.GET["type"])
                Type(request, page, request.GET["type"])
                # context = Paging(page, find)
                # allArticle = Article.objects.all()
                # recentFind = recent()
                # context['recentFind'] = recentFind
                # return render(request, 'web/blogHome.html', context)
            else:
                page = int(request.GET.get("p", 1))
                find = Article.objects.all()
                context = Paging(page, find)
                allArticle = Article.objects.all()
                recentFind = recent()
                context['recentFind'] = recentFind
                return render(request, 'web/blogHome.html', context)
    summary()
    find = Article.objects.all()
    recentFind = recent()
    if find:
        context = Paging(1, find)
        context['recentFind'] = recentFind
        return render(request, 'web/blogHome.html', context)
    else:
        return render(request, 'web/error.html')