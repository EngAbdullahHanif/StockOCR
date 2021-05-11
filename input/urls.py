from django.urls import path

from .views import ItemsCreateView, list_devices, create_device, projects_list, project_devices, export_excel
urlpatterns = [
    path('', ItemsCreateView.as_view(), name='home'),
    path('devices', list_devices, name='devices'),
    path('device/<project_name>/<item_type>', create_device, name='device-create'),
    path('projects', projects_list, name='projects'),
    path('project/<int:pk>', project_devices, name='project'),
    path('excel/<int:pk>', export_excel, name='excel-report'),
]