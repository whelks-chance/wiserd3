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
from django.conf.urls import include, url
from django.contrib import admin
from dataportal3 import views
from old import views as old_views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', views.index, name='index'),
    url(r'^index', views.index, name='index'),

    url(r'^tables', views.tables, name='tables'),

    url(r'^map', views.map_search, name='map'),

    url(r'^blank', views.blank, name='blank'),

    # url(r'^map_search', views.map_search, name='map_search'),
    #
    # url(r'^data_autocomplete', views.data_autocomplete, name='data.autocomplete'),
    #
    # url(r'^metadata/dublin_core', views.dc_info, name='dc_info'),
    #
    # url(r'^metadata/survey/dublin_core/(?P<wiserd_id>\S+)', views.survey_dc_data, name='survey_dc_data'),
    # url(r'^metadata/survey/questions/(?P<wiserd_id>\S+)', views.survey_questions, name='survey_questions'),
    # url(r'^metadata/survey/question/(?P<question_id>\S+)/results', views.survey_questions_results, name='survey_question_results'),
    # url(r'^metadata/survey/question/(?P<question_id>\S+)/result_table', views.survey_questions_results_table, name='survey_question_result_table'),
    # url(r'^metadata/survey/(?P<wiserd_id>\S+)', views.survey_metadata, name='survey_metadata'),
    #
    url(r'^spatial_search', old_views.spatial_search, name='spatial_search'),
    # url(r'^search_survey_question_gui/(?P<search_terms>\S+)',
    #     views.search_survey_question_gui, name='search_survey_question_gui'),
    #
    # url(r'^metadata/search/survey/questions/(?P<search_terms>\S+)',
    #     views.search_survey_question, name='search_survey_question'),


]
