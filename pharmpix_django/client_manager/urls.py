# client_manager/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Main Dashboard
    path('', views.dashboard, name='dashboard'),  # New dashboard view

    # Download Files (Existing)
    path('clients/', views.client_list, name='client_list'),
    path('clients/download/<int:client_id>/', views.download_files, name='download_files'),
    path('clients/download/<int:client_id>/<str:date_filter>/', views.download_files, name='download_files_with_date'),
    # path('manage/clients/<int:client_id>/details/', views.client_details, name='client_details'),
    path('clients/download/status/<int:client_id>/', views.download_status, name='download_status'),
    path('get-task-status/', views.get_task_status, name='get_task_status'),

    # Client Management
    path('manage/clients/', views.manage_clients, name='manage_clients'),
    path('manage/clients/add/', views.add_client, name='add_client'),
    path('manage/clients/edit/<int:client_id>/', views.edit_client, name='edit_client'),
    path('manage/clients/delete/<int:client_id>/', views.delete_client, name='delete_client'),
    path('manage/clients/<int:client_id>/details/', views.client_details, name='client_details'),  # New: Client details page

    # Path Management (Nested under Client)
    path('manage/clients/<int:client_id>/paths/', views.manage_paths, name='manage_paths'),
    path('manage/clients/<int:client_id>/paths/add/', views.add_path, name='add_path'),
    path('manage/clients/<int:client_id>/paths/edit/<int:path_id>/', views.edit_path, name='edit_path'),
    path('manage/clients/<int:client_id>/paths/delete/<int:path_id>/', views.delete_path, name='delete_path'),

    # Task Management
    path('manage/tasks/', views.manage_tasks, name='manage_tasks'),
    path('manage/tasks/add/', views.add_task, name='add_task'),
    path('manage/tasks/edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('manage/tasks/delete/<int:task_id>/', views.delete_task, name='delete_task'),

    # OutputConfig Management (Nested under Client)
    path('manage/clients/<int:client_id>/output-configs/', views.manage_output_configs, name='manage_output_configs'),
    path('manage/clients/<int:client_id>/output-configs/add/', views.add_output_config, name='add_output_config'),
    path('manage/clients/<int:client_id>/output-configs/edit/<int:config_id>/', views.edit_output_config, name='edit_output_config'),
    path('manage/clients/<int:client_id>/output-configs/delete/<int:config_id>/', views.delete_output_config, name='delete_output_config'),

    # FileConfig Management (Nested under Client)
    path('<int:client_id>/file-configs/add/', views.add_file_config, name='add_file_config'),
    path('file-configs/edit/<int:config_id>/', views.edit_file_config, name='edit_file_config'),
    path('file-configs/delete/<int:config_id>/', views.delete_file_config, name='delete_file_config'),

    # File Management
    path('files/view/<int:file_id>/', views.view_file, name='view_file'),
    path('files/replace/<int:file_id>/', views.replace_file, name='replace_file'),
    path('files/delete/<int:file_id>/', views.delete_file, name='delete_file'),

    #SFTP Management
    path('files/send-to-sftp/', views.send_to_sftp, name='send_to_sftp'),


    # start work for 10PM task
    # path('clients/create/', views.client_create, name='client_create'),
    # path('clients/<int:pk>/update/', views.client_update, name='client_update'),
    # path('clients/<int:pk>/delete/', views.client_delete, name='client_delete'),
    # path('clients/<int:client_id>/file-configs/', views.file_config_list, name='file_config_list'),
    # path('clients/<int:client_id>/file-configs/create/', views.file_config_create, name='file_config_create'),
    # path('file-configs/<int:pk>/update/', views.file_config_update, name='file_config_update'),
    # path('file-configs/<int:pk>/delete/', views.file_config_delete, name='file_config_delete'),
    # path('download-10pm/', views.download_10pm_files, name='download_10pm_files'),
    # path('downloaded-files/', views.downloaded_files, name='downloaded_files'),
]