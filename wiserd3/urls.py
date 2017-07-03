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
from django.conf.urls.static import static
from django.contrib import admin, auth
from dataportal3 import views, urls as api_urls
from old import views as old_views
from django.conf.urls.i18n import i18n_patterns

from wiserd3 import settings

urlpatterns = [
                  url(r'^grappelli/', include('grappelli.urls')),
                  url(r'^explorer/', include('explorer.urls')),
                  url(r'^admin_tools/', include(admin.site.urls)),
                  url(r'^api/', include(api_urls, namespace='api')),

                  url(r'^map_test', views.map_test, name='map_test'),
                  url(r'^snippet_test', views.snippet_test, name='snippet_test'),
                  url(r'^d3_test/(?P<survey_id>\S+)', views.d3_test, name='d3_test'),

                  url(r'^$', views.dashboard, name='root'),
                  url(r'^index', views.dashboard, name='index'),
                  url(r'^dashboard', views.dashboard, name='dashboard'),
                  url(r'^naw_dashboard', views.naw_dashboard, name='naw_dashboard'),
                  url(r'^m4w_dashboard', views.m4w_dashboard, name='m4w_dashboard'),
                  url(r'^wmh_dashboard', views.wmh_dashboard, name='wmh_dashboard'),
                  url(r'^wiserd_projects_dashboard', views.wiserd_projects_dashboard, name='wiserd_projects_dashboard'),
                  url(r'^partner_projects_dashboard', views.partner_projects_dashboard, name='partner_projects_dashboard'),
                  url(r'^about_dashboard', views.about_dashboard, name='about_dashboard'),
                  url(r'^http_404', views.http_404_error, name='http_404'),
                  # Legacy - Because we shared this address once
                  url(r'^dataportal', views.dataportal, name='dataportal'),

                  url(r'^logout', views.logout, name='logout'),
                  url(r'^profile', views.profile, name='profile'),
                  url(r'^welcome', views.welcome, name='welcome'),
                  url(r'^help_support', views.help_support, name='help_support'),
                  url(r'^terms_conditions', views.terms_conditions, name='terms_conditions'),
                  url(r'^user_guide', views.user_guide, name='user_guide'),
                  url(r'^licence_attribution', views.licence_attribution, name='licence_attribution'),
                  url(r'^save_profile_extras', views.save_profile_extras, name='save_profile_extras'),

                  # url(r'^settings', views.user_settings, name='settings'),
                  url(r'^site_setup', views.site_setup, name='site_setup'),
                  url(r'^question_links', views.question_links, name='question_links'),

                  url(r'^admin_api', views.admin_api, name='admin_api'),

                  url(r'^remote_data_topojson', views.remote_data_topojson, name='remote_data_topojson'),
                  url(r'^data_api', views.data_api, name='data_api'),
                  url(r'^local_data_topojson', views.local_data_topojson, name='local_data_topojson'),

                  url(r'^search_layer_topojson/(?P<search_uuid>\S+)', views.get_topojson_for_uuid_view, name='search_layer_topojson'),

                  url(r'^data_and_history', views.data_and_history, name='data_and_history'),
                  url(r'^file_management', views.file_management, name='file_management'),
                  url(r'^events', views.events, name='events'),
                  url(r'^search_data/(?P<search_uuid>\S+)', views.search_data, name='search_data'),
                  url(r'^csv_viewer_data/(?P<provider>\S+)/(?P<search_uuid>\S+)', views.csv_view_data, name='csv_view_data'),
                  url(r'^download_dataset_zip', views.download_dataset_zip, name='download_dataset_zip'),

                  # url(r'^upload_shapefile_progress', views.get_upload_progress, name='upload_shapefile_progress'),
                  url(r'^upload_shapefile', views.upload_shapefile, name='upload_shapefile'),
                  url(r'^shapefile_list', views.shapefile_list, name='shapefile_list'),

                  url(r'^browse_surveys', views.browse_surveys, name='browse_surveys'),
                  url(r'^tables', views.tables, name='tables'),
                  url(r'^survey/(?P<survey_id>\S+)', views.survey_detail, name='survey_detail'),
                  url(r'^question/(?P<question_id>\S+)', views.question, name='question_detail'),
                  url(r'^qual_transcript/(?P<qual_id>\S+)', views.qual_transcript, name='qual_transcript'),

                  url(r'^map', views.map_search, name='map'),
                  url(r'gen_screenshot/(?P<search_uuid>\S+)', views.gen_screenshot, name='gen_screenshot'),

                  url(r'^wiserd_education', views.wiserd_education, name='wiserd_education'),
                  url(r'^civil_society', views.civil_society, name='civil_society'),

                  url(r'^blank', views.blank, name='blank'),

                  # url(r'^map_search', views.map_search, name='map_search'),
                  #
                  # url(r'^data_autocomplete', views.data_autocomplete, name='data.autocomplete'),

                  url(r'^metadata/qual/dublin_core/(?P<qual_id>\S+)', views.qual_dc_data, name='qual_dc_data'),
                  url(r'^metadata/qual/(?P<qual_id>\S+)', views.qual_metadata, name='qual_metadata'),

                  url(r'^metadata/survey/dublin_core/(?P<wiserd_id>\S+)', old_views.survey_dc_data, name='survey_dc_data'),
                  url(r'^metadata/survey/questions/(?P<wiserd_id>\S+)', old_views.survey_questions, name='survey_questions'),

                  url(r'^metadata/survey/question/(?P<question_id>\S+)/results', old_views.survey_questions_results, name='survey_question_results'),
                  # url(r'^metadata/survey/question/(?P<question_id>\S+)/result_table', old_views.survey_questions_results_table, name='survey_question_result_table'),

                  url(r'^metadata/survey/question/(?P<question_id>\S+)/response_table', views.response_table,
                      name='response_table'),

                  url(r'^metadata/survey/question/(?P<question_id>\S+)', old_views.survey_question, name='survey_single_question'),
                  url(r'^metadata/survey/(?P<wiserd_id>\S+)', old_views.survey_metadata, name='survey_metadata'),
                  #
                  url(r'^spatial_search', views.spatial_search, name='spatial_search'),
                  url(r'^new_spatial_search', views.new_spatial_search, name='new_spatial_search'),

                  url(r'^metadata/search_questions', views.search_survey_question_api, name='search_survey_question_api'),
                  url(r'^metadata/search_surveys', views.search_survey_api, name='search_survey_api'),
                  url(r'^search', views.search_survey_question_gui, name='search_survey_question_gui'),

                  url(r'^metadata/search_qual', views.search_qual_api, name='search_qual_api'),


                  url(r'^edit_metadata', views.edit_metadata, name='edit_metadata'),
                  url(r'^local_data', views.local_data, name='local_data'),

                  url(r'^get_geojson', views.get_geojson, name='get_geojson'),
                  url(r'^get_imported_feature', views.get_imported_feature, name='get_imported_feature'),

                  # url(r'^metadata/search/survey/questions/(?P<search_terms>\S+)',
                  #     views.search_survey_question, name='search_survey_question'),
                  url(r'^send_email_confirmation', views.send_email_confirmation_view, name='send_email_confirmation'),

                  url(r'^accounts/', include('allauth.urls')),
                  # url('^', include('django.contrib.auth.urls'))

                  url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.STATIC_ROOT}),
                  # url(r'^i18n/', include('django.conf.urls.i18n')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += patterns(
    'djcelery.views', url(r'^task/status/(?P<task_id>.+)/$', 'task_status', name='task-status')
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
                            url(r'^rosetta/', include('rosetta.urls')),
                            )

# urlpatterns += i18n_patterns(
#     url(r'^$', views.dashboard, name='home'),
#     url(r'^index', views.dashboard, name='index'),
#     url(r'^dashboard', views.dashboard, name='dashboard'),
#     # url(r'^$', views.naw_dashboard, name='naw_dashboard'),
#     url(r'^naw_dashboard', views.naw_dashboard, name='naw_dashboard'),
#     # url(r'^admin/', include(admin.site.urls)),
# )
