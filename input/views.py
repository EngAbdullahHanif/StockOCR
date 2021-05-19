import io
import re
import pytesseract
import xlsxwriter
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from pathlib import Path

from .forms import ItemForm
from .models import Item, Device, Project, ItemType


BASE_DIR = Path(__file__).resolve().parent.parent


def generate_ocr(items):
    for item in items:
        img= str(BASE_DIR) + str(item.mac_img.url)
        image_content = pytesseract.image_to_string(img, lang="eng")
        p4 = re.split('\n', image_content) 
        for px in p4:
            # print(px)
            # if (re.search('EQ1|E@1|EQ1|ETH|EQ@1', px)):
            if (re.search('WLAN|WO1|E09|£€1@|EQ9', px)):
                # print(cleaned_name)
                data = re.findall('WLAN:|WLAN|WO1:|WO1|E09|£€1@|EQ9', px)
                cleaned_name = px.replace(''.join(data), "").replace("|", "")
                Item.objects.filter(mac_img=item.mac_img.name).update(name=cleaned_name)

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
            project_new_obj  = Project(project_name=project_name, item_type=item_type, description=project_description)
            project_new_obj.save()
            for my_file in files:
                p = Item(mac_img=my_file, project_name=project_new_obj)
                p.save()
            messages.success(self.request, 'Successfully Saved')
            return redirect(reverse('home'))
        return redirect('home')


def list_devices(request):
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
                return render(request, 'devices.html', context)
            items = Device.objects.filter(project=project_obj).filter(created_at__gte=min_date).order_by('pk').reverse()
        context =  {
            'items':items,
            'project_objs': project_objs,
        }
        return render(request, 'devices.html', context)


def create_device(request):
    if request.method == 'GET':
        min_date = request.GET.get('min_date')
        project_name = request.GET.get('project_name')
        item_type = request.GET.get('item_type')
        project_objs = ItemType.objects.all()
        items = {}
        if (item_type is not None) and (project_name is not None):
            project_obj = Project.objects.filter(project_name=project_name)
            try: 
                items = Item.objects.filter(project_name__icontains=project_name)
                items = items.filter(item_type__icontains=item_type)
                items = items.filter(created_at__gte=min_date)
                if not items:
                    context =  {
                        'items':items,
                        'project_name': project_name,
                        'item_type': item_type,
                        'project_objs': project_objs,
                        "msg":"Data Does not exist",
                    }
                    return render(request, 'generate_ocr.html', context)
                generate_ocr(items)
            
            except Item.DoesNotExist:
                context =  {
                    'items':items,
                    'project_name': project_name,
                    'item_type': item_type,
                    'project_objs': project_objs,
                    "msg":"Exception Data Does not exist",
                }
                return render(request, 'generate_ocr.html', context)
            items = Item.objects.all()
        context =  {
            'items':items,
            'project_name': project_name,
            'item_type': item_type,
            'project_objs': project_objs,
        }
        return render(request, 'generate_ocr.html', context)
    if request.method == "POST":
        items = request.POST.dict()
        items_value = request.POST.dict().values()
        project_obj =  {}
        project_name = ""
        for item in items:
            if re.match('project_name', item):
                project_obj = Project.objects.get(pk=pk)
                continue
            if re.match('description', item):
                continue
            if re.match('csrfmiddlewaretoken', item):
                continue
            if re.match('submit', item):
                continue

            form = Device(mac=items.get(item), img_path=item, project=project_obj)        
            form.save()
            Item.objects.filter(project_name=project_obj).delete()
        
        messages.success(request, 'OCR Successfully Generated')
        return redirect('projects')


def generate_projects_list_ocr(request, pk):
    project_obj = Project.objects.get(pk=pk)
    if request.method == 'GET':
        items = Item.objects.filter(project_name=project_obj, is_processed=False)
        generate_ocr(items)
        items = Item.objects.filter(project_name=project_obj, is_processed=False)
        context =  {
            'items':items,
            'project_obj': project_obj
        }
        return render(request, 'generate_project_ocr.html', context)  
    if request.method == "POST":
        items = request.POST.dict()
        project_obj = Project.objects.get(pk=pk)
        for item in items:
            if re.match('csrfmiddlewaretoken', item):
                continue
            if re.match('submit', item):
                continue
            # cleaned_data = re.findall(re.compile(r'(?:[0-9a-fA-F]:?){12}'), items.get(item))
            # p = re.compile(r'((?<=\s).*)')
            # data = re.findall(p, items.get(item))
            data = items.get(item).replace(" ", "")
            p = re.compile(r'(?:[0-9a-fA-F]:?){12}')
            row_mac = re.findall(p,  data)
            mac = ''.join(row_mac)
            form = Device(mac=mac, img_path=item, project=project_obj)        
            form.save()
            Item.objects.filter(project_name=project_obj).update(is_processed=True)
    messages.success(request, 'OCR Generated Successfully')
    return redirect('projects')


def un_ocr_project(request):
    objects = Item.objects.filter(is_processed=False).values('project_name').distinct()
   
    projects = []
    for object in objects:
        projects.append(Project.objects.get(pk=object['project_name']))
    
    context = {
        'projects': projects
    }
    return render(request, 'un_ocr_projects_list.html', context)
        

def projects_list(request):
    projects = Project.objects.all().order_by('pk').reverse()
    page = request.GET.get('page', 1)
    paginator = Paginator(projects, 10)

    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)

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
        msg = "OCR is not generated for this project"
    context = {
        'project': project_obj,
        'devices': devices,
        'msg': msg,
    }

    return render(request, 'project_devices.html', context)


def export_excel(request, pk):
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


def handler404(request, *args, **argv):
    response = render('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response


def append_devices(request, pk):
    project_obj = Project.objects.get(pk=pk)

    if request.method == 'GET':
        context = {'project_obj': project_obj}
        return render(request, 'append_project_device.html', context)

    if request.method == "POST":
        project_obj = Project.objects.get(pk=pk)
        form = ItemForm(request.POST)
        
        print('came here')
        # if form.is_valid():
            # img = form.cleaned_data['mac_img']
        files = request.FILES.getlist('mac_img')
        for my_file in files:
            p = Item(mac_img=my_file, project_name=project_obj)
            p.save()
            # form.save()
        messages.success(request, 'Devices Appended')
        return redirect('projects')
