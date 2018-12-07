from django.shortcuts import render
from .models import Article

def profile(request):
    context = {}
    if request.method == 'POST':
        if request.POST.get("type"):
            find = Article.objects.filter(type=request.POST.get("type"))
            if find:
                context['find'] = find
                return render(request, 'web/profile.html', context)
            else:
                print('No Found!')
                return render(request, 'web/error.html')
    else:
        find = Article.objects.all()
        if find:
            context['find'] = find
            return render(request, 'web/profile.html', context)
        else:
            print('No Found!')
            return render(request, 'web/error.html')



def detail(request, key):
    try:
        context = {}
        find = Article.objects.filter(id=key)[0]
    except:
        return render(request, 'web/error.html')
    else:
        if find:
            context['find'] = find
            return render(request, 'web/detail.html', context)
        else:
            return render(request, 'web/error.html')

