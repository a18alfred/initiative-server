from django.urls import path
from .views import CategoryListView, CategoryCreateView, CategoryGetPutDeleteView, ProjectDetailView, ProjectCreateView, \
    ProjectDeleteView, ProjectUpdateView, ProjectSuperUpdateView, ProjectUserCreatedListView, ProjectApprovedListView, \
    ProjectAllListView, ProjectAttachmentUpdateDeleteView, ProjectAttachmentUploadView, ProjectLinkAddView, \
    ProjectLinkUpdateDeleteView, ProjectCommentAddView, ProjectCommentUpdateDeleteView, ProjectCommentAllListView, \
    ProjectCommentRepliesListView, ProjectLikeDislikeView, ProjectCommentLikeDislikeView

app_name = 'projects'

urlpatterns = [
    path('categories/all/', CategoryListView.as_view(), name='category_list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/update/<uuid:pk>/', CategoryGetPutDeleteView.as_view(), name='category_update_delete'),
    path('projects/details/<uuid:pk>/', ProjectDetailView.as_view(), name='project_details'),
    path('projects/create/', ProjectCreateView.as_view(), name='project_create'),
    path('projects/delete/<uuid:pk>/', ProjectDeleteView.as_view(), name='project_delete'),
    path('projects/update/<uuid:pk>/', ProjectUpdateView.as_view(), name='project_update'),
    path('projects/updatesuper/<uuid:pk>/', ProjectSuperUpdateView.as_view(), name='project_super_update'),
    path('projects/mylist/', ProjectUserCreatedListView.as_view(), name='project_user_created_list'),
    path('projects/approved/', ProjectApprovedListView.as_view(), name='project_all_approved_list'),
    path('projects/all/', ProjectAllListView.as_view(), name='project_all_list'),
    path('projects/attachment/upload/', ProjectAttachmentUploadView.as_view(), name='project_attachment_upload'),
    path('projects/attachment/update/<uuid:pk>/', ProjectAttachmentUpdateDeleteView.as_view(),
         name='project_attachment_update_delete'),
    path('projects/link/add/', ProjectLinkAddView.as_view(), name='project_link_add'),
    path('projects/link/update/<uuid:pk>/', ProjectLinkUpdateDeleteView.as_view(),
         name='project_link_update_delete'),
    path('projects/comment/add/', ProjectCommentAddView.as_view(), name='project_comment_add'),
    path('projects/comment/update/<uuid:pk>/', ProjectCommentUpdateDeleteView.as_view(),
         name='project_comment_update_delete'),
    path('projects/comment/all/<uuid:pk>/', ProjectCommentAllListView.as_view(),
         name='project_comment_all_list'),
    path('projects/comment/replies/<uuid:pk>/', ProjectCommentRepliesListView.as_view(),
         name='project_comment_replies_list'),
    path('projects/likedislike/<uuid:pk>/', ProjectLikeDislikeView.as_view(),
         name='project_like_dislike'),
    path('projects/comment/likedislike/<uuid:pk>/', ProjectCommentLikeDislikeView.as_view(),
         name='project_comment_like_dislike'),
]
