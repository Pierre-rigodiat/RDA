################################################################################
#
# File Name: urls.py
# Application: explore
# Purpose:   
#
# Author: Sharief Youssef
#         sharief.youssef@nist.gov
#
#         Guillaume Sousa Amaral
#         guillaume.sousa@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################

from django.conf.urls import patterns, url

from explore import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^select-template', views.index),
    url(r'^customize-template$', 'explore.views.explore_customize_template', name='expore-customize-template'),
    url(r'^perform-search$', 'explore.views.explore_perform_search', name='explore-perform-search'),
    url(r'^results$', 'explore.views.explore_results', name='explore-results'),
    url(r'^results/download-results/$', 'explore.views.explore_download_results', name='explore-download-results'),
    url(r'^sparqlresults$', 'explore.views.explore_sparqlresults', name='explore-sparqlresults'),
    url(r'^results/download-sparqlresults/$', 'explore.views.explore_download_sparqlresults', name='explore-download-sparqlresults'),
    url(r'^redirect_explore_tabs', 'explore.ajax.redirect_explore_tabs'),
    url(r'^set_current_template', 'explore.ajax.set_current_template'),
    url(r'^set_current_user_template', 'explore.ajax.set_current_user_template'),
    url(r'^update_user_inputs', 'explore.ajax.update_user_inputs'),
    url(r'^verify_template_is_selected', 'explore.ajax.verify_template_is_selected'),
    url(r'^generate_xsd_tree_for_querying_data', 'explore.ajax.generate_xsd_tree_for_querying_data'),
    url(r'^switch_explore_tab', 'explore.ajax.switch_explore_tab'),
    url(r'^save_custom_data', 'explore.ajax.save_custom_data'),
    url(r'^get_custom_form', 'explore.ajax.get_custom_form'),
    url(r'^set_current_criteria', 'explore.ajax.set_current_criteria'),
    url(r'^select_element', 'explore.ajax.select_element'),
    url(r'^execute_query', 'explore.ajax.execute_query'),
    url(r'^get_results_by_instance', 'explore.ajax.get_results_by_instance'),    
    url(r'^get_sparql_results_by_instance', 'explore.ajax.get_sparql_results_by_instance'),
    url(r'^add_field', 'explore.ajax.add_field'),
    url(r'^remove_field', 'explore.ajax.remove_field'),
    url(r'^save_query', 'explore.ajax.save_query'), 
    url(r'^add_saved_query_to_form', 'explore.ajax.add_saved_query_to_form'),
    url(r'^delete_query', 'explore.ajax.delete_query'),
    url(r'^clear_criterias', 'explore.ajax.clear_criterias'),  
    url(r'^clear_queries', 'explore.ajax.clear_queries'),  
    url(r'^download_results', 'explore.ajax.download_results'),  
    url(r'^redirect_explore', 'explore.ajax.redirect_explore'),  
    url(r'^execute_sparql_query', 'explore.ajax.execute_sparql_query'),  
    url(r'^download_sparql_results', 'explore.ajax.download_sparql_results'),  
    url(r'^insert_sub_element_query', 'explore.ajax.insert_sub_element_query'),  
    url(r'^prepare_sub_element_query', 'explore.ajax.prepare_sub_element_query'),  
    url(r'^back_to_query', 'explore.ajax.back_to_query'),  
    url(r'^get_results', 'explore.ajax.get_results'),  
    url(r'^get_sparql_results', 'explore.ajax.get_sparql_results'),  
)
