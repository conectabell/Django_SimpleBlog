from django.shortcuts import render
from django.template import RequestContext
from django.utils import timezone
from .models import Post
from .forms import PostForm, KeyCheckForm
from .libs import crypt
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import hashlib
#import markdown

INI = {"title": "Titulo de la entrada.", "key": "Password", "rekey": "Repita la Password"}

@login_required(login_url='django.contrib.auth.views.login')
def post_list(request):
    posts = Post.objects.filter(published_date__lte=
        timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


@login_required(login_url='django.contrib.auth.views.login')
def post_new(request):
    posts = Post.objects.filter(published_date__lte=
    timezone.now()).order_by('published_date')
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if post.crypt == True:
                cifr = crypt.AESCipher(post.key)
                txt_enc = cifr.encrypt(post.text)
                post.text = txt_enc
                hash_object = hashlib.sha256(post.key)
                hex_dig = hash_object.hexdigest()
                post.key = hex_dig
                post.rekey = hex_dig
            post.save()
            return post_list(request)
    else:
        form = PostForm(initial=INI)
    return render(request, 'blog/post_edit.html', {'form': form, 'posts': posts})


@login_required(login_url='django.contrib.auth.views.login')
def post_edit(request, pk, form=None):
    try:
        print "REQ---"
        print request
        posts = Post.objects.filter(published_date__lte=
        timezone.now()).order_by('published_date')
        post = get_object_or_404(Post, pk=pk)
        print "POST:---" + str(post)

        if post.crypt is True:
            print "post.crypt TRUE"
            return redirect('blog.views.key_check_edit', pk=pk)
        else:
            print "post.crypt FALSE"
        print "METHOD: " + str(request.method)
        if request.method == "POST":
            form2 = PostForm(request.POST)
            #form2 = form
            #form = request.POST
            post2 = form2.save(commit=False)
            print "__POST2_CRYPT: "
            print post2.crypt
            if form2.is_valid():
                if post2.crypt is True:
                    print "POST2 IS TRUE"
                    cifr = crypt.AESCipher(post2.key)
                    txt_enc = cifr.encrypt(post2.text)
                    post2.text = txt_enc
                    hash_object = hashlib.sha256(post2.key)
                    hex_dig = hash_object.hexdigest()
                    post2.key = hex_dig
                    post2.rekey = hex_dig
                post2.author = request.user
                post2.save()
                return post_detail(request, pk=post2.pk)
            else:
                print "Formulario No Valido"
                return render(request, 'blog/post_edit.html', {'form': form, 'posts': posts})
        else:
            print "Paso por ELSE"
            form = PostForm(instance=post)
        #return redirect('blog.views.post_edit', pk=post.pk, form=)
        return render(request, 'blog/post_edit.html', {'form': form, 'posts': posts},)
    except Exception as e:
        print "ERROR post_edit: " + str(e)


@login_required(login_url='django.contrib.auth.views.login')
def post_detail(request, pk):
    try:
        posts = Post.objects.filter(published_date__lte=
        timezone.now()).order_by('published_date')
        post = get_object_or_404(Post, pk=pk)
        if post.crypt is True:
            return redirect('blog.views.key_check', pk=post.pk)
        else:
            return render(request, 'blog/post_detail.html', {'post': post,
                                                    'posts': posts})
        #txt = markdown.markdown(post.text)
        #pst = {'author': post.author, 'title': post.title, 'text': txt,
                #'published_date': post.published_date,}
    except Exception as e:
        print e


@login_required(login_url='django.contrib.auth.views.login')
def key_check(request, pk):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = KeyCheckForm(request.POST)
        if form.is_valid():
            p = form.cleaned_data['passw']
            hash_object = hashlib.sha256(p)
            hex_dig = hash_object.hexdigest()
            #print "POSTKEY:" + post.key
            #print "POSTKEY:" + hex_dig
            if post.key == hex_dig:
                cifr = crypt.AESCipher(p)
                txt_dec = cifr.decrypt(post.text)
                post.text = txt_dec
                return render(request, 'blog/post_detail.html', {'post': post ,
                                                    'posts': posts})
    form = KeyCheckForm()
    return render(request, 'blog/key_check.html', {'form': form ,
                                                    'posts': posts})


@login_required(login_url='django.contrib.auth.views.login')
def key_check_edit(request, pk):
    try:
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
        post = get_object_or_404(Post, pk=pk)
        if request.method == "POST":
            form = KeyCheckForm(request.POST)
            if form.is_valid():
                p = form.cleaned_data['passw']
                hash_object = hashlib.sha256(p)
                hex_dig = hash_object.hexdigest()
                print "POSTKEY:" + post.key
                print "POSTKEY:" + hex_dig
                if post.key == hex_dig:
                    cifr = crypt.AESCipher(p)
                    t = post.text
                    #print cifr.decrypt(t)
                    txt_dec = cifr.decrypt(t)
                    print post.text
                    print "P= " + p
                    print "TEXT-DEC-----"
                    print txt_dec
                    post.text = txt_dec
                    post.crypt = False
                    print post.crypt
                    form2 = PostForm(instance=post)
                    form2.text = txt_dec
                    form2.crypt = False
                    print form2
                    #form2.save()
                    #return post_edit(request, pk)
                    #return redirect('blog.views.post_edit', pk=pk, form=form2, context=RequestContext(request))
                    #return post_edit(pk=post.pk, form=form2)
                    return render(request, 'blog/post_edit.html', {'form': form2, 'posts': posts})
                    #return post_edit(request, )
        form = KeyCheckForm()
        return render(request, 'blog/key_check.html', {'form': form ,
                                                        'posts': posts})
    except Exception as e:
        print "ERROR: " + str(e)