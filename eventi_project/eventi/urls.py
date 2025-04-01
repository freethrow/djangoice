# eventi/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Read-only views
    path("", views.EventListView.as_view(), name="event_list"),
    path("evento/<int:pk>/", views.EventDetailView.as_view(), name="event_detail"),
    # User protected views
    path("evento/crea/", views.EventCreateView.as_view(), name="event_create"),
    path(
        "evento/<int:pk>/modifica/",
        views.EventUpdateView.as_view(),
        name="event_update",
    ),
    path(
        "events/<int:event_pk>/files/<int:file_pk>/download/",
        views.EventFileDownloadView.as_view(),
        name="event_file_download",
    ),
    path(
        "events/<int:pk>/delete/", views.EventDeleteView.as_view(), name="event_delete"
    ),
    path(
        "events/<int:event_pk>/files/<int:file_pk>/delete/",
        views.EventFileDeleteView.as_view(),
        name="event_file_delete",
    ),
    path(
        "events/<int:pk>/upload-file/",
        views.EventFileUploadView.as_view(),
        name="event_file_upload",
    ),
    # Report URLs
    path("report/", views.ReportSelectionView.as_view(), name="report_selection"),
    path("report/genera/", views.GenerateReportView.as_view(), name="generate_report"),
    #path("check-storage/", views.check_storage, name="check_storage"),
    path("reports/files/", views.ReportFileListView.as_view(), name="report_files"),
    path(
        "reports/files/download/",
        views.ReportFileDownloadView.as_view(),
        name="report_file_download",
    ),
    path(
        "reports/files/delete/",
        views.ReportFileDeleteView.as_view(),
        name="report_file_delete",
    ),
    path("api/events/public/", views.public_events_api, name="public_events_api"),
]
