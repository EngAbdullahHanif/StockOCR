from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy, reverse
from django.http import FileResponse

import re
from PIL import Image
import pytesseract

import csv

import io
import xlsxwriter


from .forms import ItemForm, MacForm, MacFormSet
from .models import Item, Device, Project, ItemType



def is_valid_query_param(param):
    return param != "" and param is not None


def generate_ocr(items):
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
    for item in items:
        img= 'E:/projects/macOCR'+str(item.mac_img.url)
        image_content = pytesseract.image_to_string(img, lang="eng")
        # p = re.compile(r'(?:[0-9a-zA-Z]:?){12}')
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
                # p = re.compile(r'(?:[0-9a-zA-Z]:?){12}')
                # print('*******************************')
                # print(re.findall(re.compile(r'(?:[0-9a-zA-Z]:?){12}'), px))
                Item.objects.filter(mac_img=item.mac_img.name).update(name=px)
                # new_item = Device(mac=px, img_path=item.mac_img.name)
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
        project_objs = ItemType.objects.all()
        context = {'project_objs': project_objs}
        return render(self.request, 'home.html', context)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            project_name = request.POST['project_name']
            project_description = request.POST['project_description']
            item_type = request.POST['item_type']
            files = request.FILES.getlist('mac_img')
            project_new_obj, created  = Project.objects.get_or_create(project_name=project_name, item_type=item_type)
            if created: 
                project_new_obj.description=project_description
                project_new_obj.save()
            print(created)
            # Project( project_name=project_name, item_type=item_type, description=description).save()
            for my_file in files:
                p = Item(mac_img=my_file, project_name=project_name, project_description=project_description, item_type=item_type)
                p.save()
            items = Item.objects.all()
            generate_ocr(items)

            # items = Item.objects.all()
            # context =  {
            #     'items':items,
            #     'project_name': project_name,
            #     'item_type': item_type,
            # }
            # # messages.success(self.request, 'Successfully Saved')
            # # return render(request, 'form.html', context)
            # return redirect('list/?project_name='+project_name+'&item_type='+item_type)
            # ?min_date=2021-05-08&project_name=LHG&item_type=HLG
            # return redirect('list', context)
            return redirect(reverse('list', kwargs={"project_name": project_name, "item_type":item_type}))
            # return redirect('list', project_name=project_name, item_type='item_type')

        return redirect('home')


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
        project_name = request.GET.get('project_name')
        item_type = request.GET.get('item_type')
        project_objs = ItemType.objects.all()
        items = Device.objects.all().order_by('pk').reverse()
        if (min_date is not None) and (project_name is not None):
            try: 
                project_obj = Project.objects.filter(project_name=project_name).get(item_type=item_type)
            except Project.DoesNotExist:
                context = {
                    "msg":"Data Does not exist",
                    'project_objs': project_objs,
                }
                return render(request, 'mac_list.html', context)
            items = Device.objects.filter(project=project_obj).filter(created_at__gte=min_date).order_by('pk').reverse()
        context =  {
            'items':items,
            'project_objs': project_objs,
        }
        return render(request, 'mac_list.html', context)


def form_create(request, project_name, item_type):
    if request.method == 'GET':
        min_date = request.GET.get('min_date')
        project_name = request.GET.get('project_name')
        item_type = request.GET.get('item_type')
        project_objs = ItemType.objects.all()
        # print(min_date)
        # print(project)
        items = {}
        if (item_type is not None) and (project_name is not None):
            print('came here')
            project_obj = Project.objects.filter(project_name=project)
            # items = Item.objects.filter(project_name=project_name).filter(item_type=item_type).filter(created_at__gte=min_date)
            try: 
                items = Item.objects.filter(project_name=project_name)
                print(items)
                items = items.filter(item_type=item_type)
                items = items.filter(created_at__gte=min_date)
        # items = Item.objects.all()
        # item_type = item_type
        # project_name = project_name
        # print(item_type)
            if not items:
                context =  {
                    'items':items,
                    'project_name': project_name,
                    'item_type': item_type,
                    'project_objs': project_objs,
                    "msg":"Data Does not exist",
                }
                return render(request, 'form.html', context)
            # print(items)
            generate_ocr(items)
            # items = Item.objects.filter(project_name=project_name).filter(item_type=item_type).filter(created_at__gte=min_date)
            # items = Item.objects.filter(project_name=project_name)
            # items = items.filter(item_type=item_type)
            # items = items.filter(created_at__gte=min_date)
        except Item.DoesNotExist:
            context =  {
                'items':items,
                'project_name': project_name,
                'item_type': item_type,
                'project_objs': project_objs,
                "msg":"Data Does not exist",
            }
            return render(request, 'form.html', context)
            # items = Item.objects.all()
        context =  {
            'items':items,
            'project_name': project_name,
            'item_type': item_type,
            # 'project_objs': project_objs
        }
        return render(request, 'form.html', context)
    if request.method == "POST":
        items = request.POST.dict()
        items_value = request.POST.dict().values()
        # print(items)
        project_obj =  {}
        project_name = ""
        for item in items:
            if re.match('project_name', item):
                # print(items.get(item))
                project_obj = Project.objects.filter(project_name=items.get(item))
                project_name = project_name=items.get(item)
                # Item.objects.filter(project_name=items.get(item)).delete()
                # print(items.get(item))
                # project_obj = Project(project_name=items.get(item))
                # project_obj.save()
                # print(project_obj)
                continue
            if re.match('item_type', item):
                project_obj = project_obj.filter(item_type=items.get(item))[0]
                # print(items.get(item))
                continue
            if re.match('description', item):
                continue
            if re.match('csrfmiddlewaretoken', item):
                continue
            if re.match('submit', item):
                continue

            # cleand_mac = re.findall(re.compile(r'(?:[0-9a-zA-Z]:?){12}'), items.get(item))
            # pattern = r"(\[.*?\])"
            # print("&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            # print(re.sub(pattern, '', str(cleand_mac)))

            form = Device(mac=items.get(item), img_path=item, project=project_obj)        
            form.save()
        

        return redirect('projects')


class FormListCreateView(CreateView):
    model = Device
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


def projects_list(request):
    projects = Project.objects.all().order_by('pk').reverse()

    context = {
        'projects': projects
    }
    return render(request, 'projects_list.html', context)       
 

def project_devices(request, pk):
    id = pk
    print(id)
    project_obj = Project.objects.get(pk=id)
    devices = Device.objects.filter(project=project_obj)
    msg = ""
    if not devices:
        msg = "Devices for this project does not exist"
    
    context = {
        'project': project_obj,
        'devices': devices,
        'msg': msg,
    }

    return render(request, 'project_devices.html', context)





def excelreport(request, pk):
    project_obj = Project.objects.get(pk=pk)
    devices = Device.objects.filter(project=project_obj)
    print(devices)
    buffer = io.BytesIO()
    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet()
    for index, data in enumerate(devices):
        worksheet.write(index, 0, data.mac)
    workbook.close()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename=project_obj.project_name+'.xlsx')