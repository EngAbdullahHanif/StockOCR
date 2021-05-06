from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy, reverse

import re
from PIL import Image
import pytesseract

import csv


from .forms import ItemForm, MacForm, MacFormSet
from .models import Item, macItem, Project

def is_valid_query_param(param):
    return param != "" and param is not None

def ocr(items):
    # items = Item.objects.filter(created_at__gte=min_date)
    # print(items)
    # if is_valid_query_param(min_date):
    #     items = items.filter(created_at__gte=min_date)
    # if len(items) == 0:
    #     return redirect(reverse('home'))
    # print('*******************')
    # print(items)
    # if self.is_valid_query_param(max_date):
    #     items = items.filter(created_at__lte=max_date)

    # mq = dict()
    new_items = {}
    for item in items:
        img= 'E:/projects/macOCR'+str(item.mac_img.url)
        image_content = pytesseract.image_to_string(img, lang="eng")
        # p = re.compile(r'(?:[0-9a-fA-F]:?){12}')
        # P2 = re.compile(r'(?:[0-9a-fA-F]:?){12}', image_content)
        # p3 = re.search('EQ1|E@1|EQ1|ETH', image_content)
        p4 = re.split('\n', image_content)    
        for px in p4:
            # print('****')
            # for findding the first latter
            # if item.mac_img.name == 'images/new2.jpg':
                # print('the image is loaded')
                # print(px)
            if (re.search('EQ1|E@1|EQ1|ETH|EQ@1', px)):
                # print('##################################')
                # mq.append(re.findall(re.compile(r'(?:[0-9a-fA-F]:?){12}'), px))
                # mq.append(px)
                # if item.mac_img.name == img_path :
                # p = re.compile(r'(?:[0-9a-fA-F]:?){12}')
                # print(re.findall(p, px))
                Item.objects.filter(mac_img=item.mac_img.name).update(name=px)
                # new_item = macItem(mac=px, img_path=item.mac_img.name)
                # new_item.save()

                # mq[item.mac_img.name] = px
                # print(px)
        # test_str = image_content

        # print(item.mac_img)
        # print(re.findall(p, test_str))
        # print(re.findall(P2, test_str))
        # print(p4)
        # print(image_content)
        # print('##################################')
    # print(mq)
    # return redirect('mac-list')

        

class ItemsCreateView(CreateView):
    model = Item
    template_name = 'home.html'
    form_class = ItemForm
    success_url = reverse_lazy('home')

    def get(self, *args, **kwargs):
        project_objs = Project.objects.all()
        context = {'project_objs': project_objs}
        return render(self.request, 'home.html', context)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            project_name = request.POST['project_name']
            files = request.FILES.getlist('mac_img')
            for my_file in files:
                p = Item(mac_img=my_file, project_name=project_name)
                p.save()
        #     return self.form_valid(form)
        # else:
        #     return self.form_invalid(form)
        # form = ItemForm(self.request.POST, self.request.FILES)        
        # if form.is_valid():
        #     # project_name = form.cleaned_data.get('project_name')
        #     # description = form.cleaned_data.get('description')
        #     for fo in form:
        #         print(fo)

        #     mac_img = form.cleaned_data.get('mac_img')
        #     # print(mac_img)
        #     # source = 'E:/projects/macOCR/'+str(mac_img)
        #     # print(source)
        #     item = Item(mac_img=mac_img)
        #     item.save()
        #     messages.success(self.request, 'Successfully Saved')
        #     # image_content = pytesseract.image_to_string(source, lang="eng")
        #     return redirect('list')

        messages.success(self.request, 'Failed to Saved')
        return redirect('home')


# class ItemsListView(ListView):
#     model = Item
#     template_name = 'items_list.html'
#     context_object_name = 'items'
#     def get(self, *args, **kwargs):

#     ocr()

def items_list(request):
    if request.method == 'GET':
        min_date = request.GET.get('min_date')
        max_date = request.GET.get('max_date')
        items = {}
        if min_date is not None:
            ocr(min_date, max_date)
            items = Item.objects.all()
        
        context =  {
            'items':items,
        }
        return render(request, 'items_list.html', context)
    if request.method == 'POST':
        # form = MacForm(request.POST)
        # print('#########################')
        # print(request.POST)
        # items = list(request.POST.items())
        # items = request.POST.getlist('submit')
        items = request.POST.dict().values()
        # print(items)
        # print(form.errors)
        # with open('mac.csv', 'w', newline='') as file:
        #     writer = csv.writer(file)
            # writer.writerow(['LHG'])
        mac_items = Item.objects.filter(is_processed=False)
        # for mac_item in mac_items:
        for index, item in enumerate(items): 
            if index == 0:
                continue
            if re.search('submit', item):
                continue        
            
            # Item.objects.filter(mac_img=mac_item.mac_img.name).update(name=item)
            # if (Item.objects.filter(mac_img=mac_item.mac_img.name)):
            Item.objects.update(name=item, is_processed=True)
                # break

                # writer.writerow([item])
                # p = re.compile(r'(?:[0-9a-fA-F]:?){12}')
                # cleaned_mac = re.findall(p, item)
                # print('***********************')
                # print(cleaned_mac)
                # print(mac_item)
                # print(mac_item.mac_img.name)
                # print(item)
        # return redirect(reverse('mac-list'))
        # if form.is_valid():
        #     obj = form.save(commit=False)
        #     print('***************')
        #     # mac = form.cleaned_data.get()
        #     print(obj)
        #     # p = re.compile(r'(?:[0-9a-fA-F]:?){12}')
        #     # print(re.findall(p, mac))
        return redirect(reverse('mac-list'))
        # return render(request, 'home.html')
    


def list_mac_address(request):
   if request.method == 'GET':
        min_date = request.GET.get('min_date')
        project = request.GET.get('project')
        project_objs = Project.objects.all()
        items = macItem.objects.all()
        if (min_date is not None) and (project is not None):
            project_obj = Project.objects.get(project_name=project)
            items = macItem.objects.filter(project=project_obj).filter(created_at__gte=min_date)
        context =  {
            'items':items,
            'project_objs': project_objs,
        }
        return render(request, 'mac_list.html', context)


def form_create(request):
    if request.method == 'GET':
        min_date = request.GET.get('min_date')
        project = request.GET.get('project')
        project_objs = Project.objects.all()
        print(min_date)
        print(project)
        items = {}
        if (min_date is not None) and (project is not None):
            # project_obj = Project.objects.filter(project_name=project)
            items = Item.objects.filter(project_name=project).filter(created_at__gte=min_date)
            items = ocr(items)
            items = Item.objects.filter(project_name=project).filter(created_at__gte=min_date)
            # items = Item.objects.all()
        context =  {
            'items':items,
            'project_name': project,
            'project_objs': project_objs
        }
        return render(request, 'form.html', context)
    if request.method == "POST":
        items = request.POST.dict()
        items_value = request.POST.dict().values()
        # print(items)
        project_obj =  {}
        for item in items:
            if re.match('project_name', item):
                project_obj = Project(project_name=items.get(item))
                project_obj.save()
                print(project_obj)
                continue
            if re.match('description', item):
                continue
            if re.match('csrfmiddlewaretoken', item):
                continue
            if re.match('submit', item):
                continue
            
            form = macItem(mac=items.get(item), img_path=item, project=project_obj)        
            form.save()
            print(items.get(item))

        return redirect('mac-list')

class FormListCreateView(CreateView):
    model = macItem
    form_class = MacForm
    template_name = 'form.html'
    success_url = reverse_lazy('home')

    def post(self, *args, **kwargs):
        form = ItemForm(self.request.POST, self.request.FILES)        
        if form.is_valid():
            project_name = form.cleaned_data.get('project_name')
            description = form.cleaned_data.get('description')
            mac_img = form.cleaned_data.get('mac_img')
            # print(mac_img)
            # source = 'E:/projects/macOCR/'+str(mac_img)
            # print(source)
            item = Item(project_name=project_name, description=description, mac_img=mac_img)
            item.save()
            messages.success(self.request, 'Successfully Saved')
            # image_content = pytesseract.image_to_string(source, lang="eng")
            return redirect('home')

        messages.success(self.request, 'Failed to Saved')
        return redirect('home')
        if request.method == "POST":
            formset = MacFormSet(request.POST)
            for form in formset.forms:
                print ("You've picked {0}".format(form.cleaned_data['mac']))
        else:
            formset = ColorFormSet()
        return redirect('home')

        