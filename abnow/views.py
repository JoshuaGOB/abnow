# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Image
from .forms import ImageForm, Code, CodeForm, CodeCategoryForm, SubCodeForm, CodeCategory, SubCode, SearchForm
from django.db.models import Q
from django import forms



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')



def home_view(request):
    images = Image.objects.filter(uploader=request.user)
    return render(request, 'home.html', {'images': images})

@login_required
def upload_image_view(request):
    CodeFormSet = forms.formset_factory(CodeForm, extra=1, can_delete=True) 
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        code_formset = CodeFormSet(request.POST, prefix='codes')
        if form.is_valid() and code_formset.is_valid():
            image = form.save(commit=False)
            image.uploader = request.user
            image.save()

            codes = []
            for code_form in code_formset:
                if code_form.cleaned_data and not code_form.cleaned_data.get('DELETE'):  
                    code = code_form.save(commit=False)
                    code.save()  # You might need to save the code first before adding to m2m field
                    codes.append(code)
            
            image.codes.add(*codes)  # Add all codes to image's codes field
            
            return redirect('home')
    else:
        form = ImageForm()
        code_formset = CodeFormSet(prefix='codes')

    return render(request, 'upload_image.html', {'form': form, 'code_formset': code_formset})

@login_required
def view_image(request, image_id):
    image = Image.objects.get(id=image_id)
    if image.uploader == request.user:
        return render(request, 'view_image.html', {'image': image})
    else:
        return redirect('home')

@login_required
def edit_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            form.save()
            return redirect('view_image', image_id=image.id)
    else:
        form = ImageForm(instance=image)

    if image.uploader == request.user:
        return render(request, 'edit_image.html', {'form': form, 'image': image})
    else:
        return redirect('home')


@login_required
def delete_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)

    if image.uploader == request.user:
        if request.method == 'POST':
            image.delete()
            return redirect('home')
        else:
            return render(request, 'delete_image_confirm.html', {'image': image})

    return redirect('home')

@login_required
def view_code(request, code_id):
    code = get_object_or_404(Code, id=code_id)
    return render(request, 'view_code.html', {'code': code})


@login_required
def create_code_view(request):
    code = Code.objects.all()
    if request.method == 'POST':
        form = CodeForm(request.POST)
        if form.is_valid():
            code = form.save()
            return redirect('view_code', code_id=code.id)

    form = CodeForm()
    return render(request, 'create_code.html', {'form': form})

@login_required
def edit_code(request, code_id):
    code = get_object_or_404(Code, id=code_id)

    if request.method == 'POST':
        form = CodeForm(request.POST, instance=code)
        if form.is_valid():
            form.save()
            return redirect('view_code', code_id=code.id)
    else:
        form = CodeForm(instance=code)

    return render(request, 'edit_code.html', {'form': form, 'code': code})

@login_required
def create_code_category_view(request):
    code_category = CodeCategory.objects.all()
    
    if request.method == 'POST':
        form = CodeCategoryForm(request.POST)
        if form.is_valid():
            code_category = form.save()
            return redirect('view_code_category', code_category_id=code_category.id)

    form = CodeCategoryForm()
    return render(request, 'create_code_category.html', {'form': form})

@login_required
def edit_code_category(request, code_category_id):
    code_category = get_object_or_404(CodeCategory, id=code_category_id)

    if request.method == 'POST':
        form = CodeCategoryForm(request.POST, instance=code_category)
        if form.is_valid():
            form.save()
            return redirect('view_code_category', code_category_id=code_category.id)
    else:
        form = CodeCategoryForm(instance=code_category)
    
    return render(request, 'edit_code_category.html', {'form': form, 'code_category': code_category})


@login_required
def edit_sub_code(request, sub_code_id):
    sub_code = get_object_or_404(SubCode, id=sub_code_id)

    if request.method == 'POST':
        form = SubCodeForm(request.POST, instance=sub_code)
        if form.is_valid():
            form.save()
            return redirect('view_sub_code', sub_code_id=sub_code.id)
    else:
        form = SubCodeForm(instance=sub_code)

    return render(request, 'edit_sub_code.html', {'form': form, 'sub_code': sub_code})
    
@login_required
def create_sub_code_view(request):
    if request.method == 'POST':
        form = SubCodeForm(request.POST)
        if form.is_valid():
            sub_code = form.save()
            return redirect('view_sub_code', sub_code_id=sub_code.id)

    form = SubCodeForm()
    return render(request, 'create_sub_code.html', {'form': form})

@login_required
def view_code_category(request, code_category_id):
    code_category = get_object_or_404(CodeCategory, id=code_category_id)
    return render(request, 'view_code_category.html', {'code_category': code_category})

@login_required
def view_sub_code(request, sub_code_id):
    sub_code = get_object_or_404(SubCode, id=sub_code_id)
    return render(request, 'view_sub_code.html', {'sub_code': sub_code})

@login_required
def image_list_view(request):
    images = Image.objects.filter(uploader=request.user)
    return render(request, 'image_list.html', {'images': images})

def search_view(request):
    form = SearchForm(request.GET)
    images = Image.objects.none()  # Empty QuerySet
    if form.is_valid():
        q = form.cleaned_data['q']
        images = Image.objects.filter(
            Q(filename__icontains=q) | 
            Q(codes__name__icontains=q) |
            Q(sub_codes__name__icontains=q)
        ).distinct()

    return render(request, 'search_results.html', {'form': form, 'images': images})