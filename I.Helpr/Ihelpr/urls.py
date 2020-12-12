from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
import Ihelprapp.views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', Ihelprapp.views.home, name='home'),
    url(r'^home', Ihelprapp.views.home, name='home'),
    url(r'^about', Ihelprapp.views.about, name='about'),
    url(r'^for-parents', Ihelprapp.views.for_parents, name='for_parents'),
    url(r'^for-sitters', Ihelprapp.views.for_sitters, name='for_sitters'),
    url(r'^messages', Ihelprapp.views.messages, name='messages'),
    url(r'^mypage', Ihelprapp.views.mypage, name='mypage'),
    url(r'^mypost', Ihelprapp.views.view_my_post_list, name='mypost'),
    url(r'^post-page', Ihelprapp.views.post_page, name='post_page'),
    url(r'^qna', Ihelprapp.views.qna, name='qna'),
    url(r'^review', Ihelprapp.views.review, name='review'),
    url(r'^delete-review', Ihelprapp.views.delete_review, name='delete_review'),
    url(r'^signup', Ihelprapp.views.sign_up, name='sign_up'),
    url(r'^login', Ihelprapp.views.login, name='login'),
    url(r'^logout', Ihelprapp.views.logout, name='logout'),
    url(r'^member_login', Ihelprapp.views.member_login, name='member_login'),
    url(r'^sitters-signup', Ihelprapp.views.sitters_signup, name='sitters_signup'),
    url(r'^parents-signup', Ihelprapp.views.parents_signup, name='parents_signup'),
    url(r'^ask-question', Ihelprapp.views.ask_question, name='ask_question'),
    url(r'^ask-created', Ihelprapp.views.ask_created, name='ask_created'),
    url(r'^post-job', Ihelprapp.views.post_job, name='post_job'),
    url(r'^search/(?P<post_type>\w)', Ihelprapp.views.search, name='search'),
    url(r'^edit-my-post', Ihelprapp.views.edit_my_post, name='edit_my_post'),
    url(r'^delete-my-post', Ihelprapp.views.delete_my_post, name='delete_my_post'),
    url(r'^member_update', Ihelprapp.views.member_update, name='member_update'),
    url(r'^view-question', Ihelprapp.views.view_question, name='view_question'),
    url(r'^parent_insert', Ihelprapp.views.parent_insert, name='parent_insert'),
    url(r'^sitter_insert', Ihelprapp.views.sitter_insert, name='sitter_insert'),
    url(r'^view_my_post', Ihelprapp.views.view_my_post, name='view_my_post'),
    url(r'^v1/posts', Ihelprapp.views.create_post, name='create_post'),
    url(r'^v1/view-post/(?P<post_type>\w)/(?P<post_id>\d+)$',
        Ihelprapp.views.view_post, name='view_post'),
    # url(r'^v1/posts/<user_type>/<post_id>', Ihelprapp.views.update_post, name='update_post'),
    url(r'^write_message', Ihelprapp.views.write_message, name='write_message'),
    url(r'^send-message', Ihelprapp.views.send_message, name='send_message'),
    url(r'^view_message', Ihelprapp.views.view_message, name='view_message'),
    url(r'^delete_message', Ihelprapp.views.delete_message, name='delete_message'),
    url(r'^mark_as_read', Ihelprapp.views.mark_as_read, name='mark_as_read'),
    url(r'^in-view-send-msg', Ihelprapp.views.in_view_send_msg,
        name='in_view_send_msg'),
    url(r'^write_review', Ihelprapp.views.write_review, name='write_review'),
    url(r'^application/create$', Ihelprapp.views.application, name='application'),
    url(r'^view-applicant', Ihelprapp.views.view_applicant, name='view_applicant'),
    url(r'^application/view/(?P<application_id>\d+)$',
        Ihelprapp.views.view_application, name='view_application'),
    # url(r'^application/view/create', Ihelprapp.views.create_application, name='create_application'),
    url(r'^application/select$', Ihelprapp.views.select_application,
        name='select_application'),
    url(r'^application/apply', Ihelprapp.views.apply, name='apply'),
    url(r'^cancel-apply', Ihelprapp.views.cancel_apply, name='cancel_apply'),
    url(r'^view-applied-history', Ihelprapp.views.view_applied_history,
        name='view_applied_history'),

    url(r'^delete-application', Ihelprapp.views.delete_application,
        name='delete_application'),
    url(r'^forgotpassword', Ihelprapp.views.forgotpassword, name='forgotpassword'),
    url(r'^sitter_idcheck', Ihelprapp.views.sitter_idcheck, name='sitter_idcheck'),
    url(r'^reset_password', Ihelprapp.views.reset_password, name='reset_password'),
    url(r'^parent_idcheck', Ihelprapp.views.parent_idcheck, name='parent_idcheck'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
