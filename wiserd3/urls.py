"""wiserd3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin, auth
from dataportal3 import views
from old import views as old_views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', views.index, name='index'),
    url(r'^index', views.index, name='index'),

    url(r'^logout', views.logout, name='logout'),
    url(r'^profile', views.profile, name='profile'),


    url(r'^file_management', views.file_management, name='file_management'),
    # url(r'^upload_shapefile_progress', views.get_upload_progress, name='upload_shapefile_progress'),
    url(r'^upload_shapefile', views.upload_shapefile, name='upload_shapefile'),
    url(r'^shapefile_list', views.shapefile_list, name='shapefile_list'),


    url(r'^tables', views.tables, name='tables'),
    url(r'^survey/(?P<survey_id>\S+)', views.survey_detail, name='survey_detail'),
    url(r'^question/(?P<question_id>\S+)', views.question, name='question_detail'),

    url(r'^map', views.map_search, name='map'),

    url(r'^blank', views.blank, name='blank'),

    # url(r'^map_search', views.map_search, name='map_search'),
    #
    # url(r'^data_autocomplete', views.data_autocomplete, name='data.autocomplete'),

    url(r'^metadata/survey/dublin_core/(?P<wiserd_id>\S+)', old_views.survey_dc_data, name='survey_dc_data'),
    url(r'^metadata/survey/questions/(?P<wiserd_id>\S+)', old_views.survey_questions, name='survey_questions'),

    url(r'^metadata/survey/question/(?P<question_id>\S+)/results', old_views.survey_questions_results, name='survey_question_results'),
    url(r'^metadata/survey/question/(?P<question_id>\S+)/result_table',
        old_views.survey_questions_results_table, name='survey_question_result_table'),

    url(r'^metadata/survey/question/(?P<question_id>\S+)', old_views.survey_question, name='survey_single_question'),
    url(r'^metadata/survey/(?P<wiserd_id>\S+)', old_views.survey_metadata, name='survey_metadata'),
    #
    url(r'^spatial_search', old_views.spatial_search, name='spatial_search'),
    url(r'^new_spatial_search', views.new_spatial_search, name='new_spatial_search'),

    url(r'^metadata/search_questions', views.search_survey_question_api, name='search_survey_question_api'),
    url(r'^search', views.search_survey_question_gui, name='search_survey_question_gui'),

    url(r'^edit_metadata', views.edit_metadata, name='edit_metadata'),

    url(r'^get_geojson', views.get_geojson, name='get_geojson'),
    url(r'^get_imported_feature', views.get_imported_feature, name='get_imported_feature'),

    # url(r'^metadata/search/survey/questions/(?P<search_terms>\S+)',
    #     views.search_survey_question, name='search_survey_question'),

    url(r'^accounts/', include('allauth.urls'))
    # url('^', include('django.contrib.auth.urls'))
]

urlpatterns += patterns(
    'djcelery.views', url(r'^task/status/(?P<task_id>.+)/$', 'task_status', name='task-status')
)
