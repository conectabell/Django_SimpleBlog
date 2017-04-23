from django.shortcuts import render
#from django.template import RequestContext
from django.utils import timezone
from .models import Post
from .forms import PostForm, KeyCheckForm
from .libs import crypt
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import hashlib, sys
#import markdown
reload(sys)
sys.setdefaultencoding('utf-8')

INI = {"title": "Titulo de la entrada.", "key": "Password", "rekey": "Repita la Password"}

@login_required(login_url='django.contrib.auth.views.login')
def post_list(request):
    posts = Post.objects.filter(published_date__lte=
        timezone.now()).order_by('-published_date')
    if "keytmp" in request.session:
        del request.session['keytmp']
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
            if post.crypt == "1":
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
def post_edit(request, pk, key=None):
    try:
        print "REQ---"
        print request
        posts = Post.objects.filter(published_date__lte=
        timezone.now()).order_by('published_date')
        post = get_object_or_404(Post, pk=pk)
        print "POST:---" + str(post)
        #if post.crypt is True:
            #print "post.crypt TRUE"
            #return redirect('blog.views.key_check_edit', pk=pk)
        #else:
            #print "post.crypt FALSE"
        print "METHOD: " + str(request.method)
        if request.method == "POST":
            #form2 = PostForm(form)
            form = PostForm(request.POST)
            #form2 = form
            #form = request.POST
            post = form.save(commit=False)
            print "__POST2_CRYPT: "
            #print form.cleaned_data['crypt']
            if form.is_valid():
                if form.cleaned_data['crypt'] == "1":
                    print "CRYPT IS TRUE"
                    cifr = crypt.AESCipher(form.cleaned_data['key'])
                    txt_enc = cifr.encrypt(form.cleaned_data['text'])
                    post.text = txt_enc
                    hash_object = hashlib.sha256(form.cleaned_data['key'])
                    hex_dig = hash_object.hexdigest()
                    post.key = hex_dig
                    post.rekey = hex_dig
                    post.pk = pk
                    post.author = request.user
                    post.save()
                    return post_detail(request, pk=pk)
                else:
                    print "CRYPT IS FALSE"
                    post.pk = pk
                    post.author = request.user
                    print "post PK: " + post.pk
                    try:
                        if post.save():
                            print "post supuestamente salvado"
                        else:
                            print "aqui ha pasado algo, en el save"
                    except Exception as e:
                        print "ERROR_SAVE: " + str(e)
                    return post_detail(request, pk=pk)
            else:
                print "Post-Edit: Formulario No Valido"
                return render(request, 'blog/post_edit.html', {'form': form, 'posts': posts})
        else:
            print "Post-Edit: No es un metodo POST- Devuelve Formulario con post extraido de la pk"
            if post.crypt == "1":
                if "keytmp" in request.session:
                    print "KEYTMP: " + request.session['keytmp']
                    cifr = crypt.AESCipher(request.session['keytmp'])
                    txt_dec = cifr.decrypt(post.text)
                    post.text = txt_dec
                    form = PostForm(instance=post)
                else:
                    print "KEYTMP: NO HAY"
                    return redirect('blog.views.key_check_edit', pk=post.pk)
            else:
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
        if post.crypt == "1":
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
def post_delete(request, pk):
    posts = Post.objects.filter(published_date__lte=
        timezone.now()).order_by('published_date')
    Post.objects.filter(id=pk).delete()
    if "keytmp" in request.session:
        del request.session['keytmp']
    msg = "Post Eliminado"
    return render(request, 'blog/post_list.html', {'posts': posts, 'msg': msg})


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
                request.session['keytmp'] = p
                return render(request, 'blog/post_detail.html', {'post': post ,
                                                    'posts': posts})
            else:
                msg = str("Password Incorrecto, introduzca uno valido.").decode('utf-8')
                form = KeyCheckForm()
                return render(request, 'blog/key_check.html', {'form': form ,
                                                            'posts': posts,
                                                            'msg': msg})
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
                    post.crypt = "0"
                    print post.crypt
                    form2 = PostForm(instance=post)
                    form2.text = txt_dec
                    form2.crypt = "0"
                    print form2
                    request.session['keytmp'] = p
                    #form2.save()
                    #return post_edit(request, pk)
                    #return redirect('blog.views.post_edit', pk=pk, key=p)
                    #return post_edit(request, pk=post.pk, key=p)
                    return render(request, 'blog/post_edit.html', {'form': form2, 'posts': posts})
                    #return post_edit(request, )
                else:
                    print "Pass Incorrecto"
                    form = KeyCheckForm()
                    msg = "Password Incorrecto"
                    return render(request, 'blog/key_check.html', {'form': form,
                                                        'posts': posts,
                                                        'msg': msg})
        form = KeyCheckForm()
        return render(request, 'blog/key_check.html', {'form': form ,
                                                        'posts': posts})
    except Exception as e:
        print "ERROR: " + str(e)
