from rest_framework.generics import (UpdateAPIView, RetrieveAPIView, ListAPIView, DestroyAPIView, CreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.views import APIView
from django.contrib.contenttypes.models import ContentType
from .serializers import CategorySerializer, AttachmentSerializer, LinkSerializer, ProjectSerializer, \
    ProjectShortSerializer, AttachmentUpdateSerializer, LinkShortSerializer, \
    CommentSerializer, CommentUpdateSerializer, VoteTypeSerializer, ProjectSuperUpdateSerializer
from .models import Category, Project, Attachment, Link, LikeDislike, Comment
from core.apps.accounts.permissions import IsSuperUserOrModeratorUser, IsSuperUser, IsActive, IsPhoneConfirmed, IsOwner, \
    IsOwnerOrSuperUser, IsAccountOwnerOrSuperUser, IsOwnerOrSuperUserOrModerator, IsAccountOwnerOrSuperUserOrModerator, \
    IsUploadsOwnerOrSuperUserOrModerator
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings
from django_filters import rest_framework as filters
from .service import ProjectFilter, CommentFilter
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.http import Http404
from django.core.exceptions import ValidationError


@method_decorator(cache_page(60 * 60, cache='category_cache'), name='dispatch')
class CategoryListView(ListAPIView):
    """
    Класс для получения списка всех категорий
    """
    permission_classes = [AllowAny]
    pagination_class = None
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryCreateView(CreateAPIView):
    """
    Класс для создания новой категории
    """
    permission_classes = [IsSuperUser, ]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryGetPutDeleteView(RetrieveUpdateDestroyAPIView):
    """
    Класс для удаления и изменения категории
    """
    permission_classes = [IsSuperUser, ]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProjectDetailView(RetrieveAPIView):
    """
    Класс для получения детальной информации по проекту
    """
    permission_classes = [AllowAny]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectCreateView(CreateAPIView):
    """
    Класс для создания новой проблемы.
    Проект может создать любой зарегистрированный активный пользователь с подтверждённым номером телефона
    """
    permission_classes = [IsActive, IsPhoneConfirmed]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        serializer.save(account=self.request.user)


class ProjectDeleteView(DestroyAPIView):
    """
    Класс для удаления проекта
    """
    permission_classes = [IsOwnerOrSuperUserOrModerator, IsActive, IsPhoneConfirmed]
    queryset = Project.objects.all()
    serializer_class = ProjectShortSerializer


class ProjectUpdateView(UpdateAPIView):
    """
    Класс для обновления проекта
    """
    permission_classes = [IsOwnerOrSuperUserOrModerator, IsActive, IsPhoneConfirmed]
    queryset = Project.objects.all()
    serializer_class = ProjectShortSerializer

    def put(self, request, *args, **kwargs):
        return Response({"detail": "Метод \"PUT\" не разрешен."},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ProjectSuperUpdateView(UpdateAPIView):
    """
    Класс для обновления статуса проекта
    """
    permission_classes = [IsSuperUserOrModeratorUser, IsActive, IsPhoneConfirmed]
    queryset = Project.objects.all()
    serializer_class = ProjectSuperUpdateSerializer

    def put(self, request, *args, **kwargs):
        return Response({"detail": "Метод \"PUT\" не разрешен."},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ProjectUserCreatedListView(ListAPIView):
    """
    Класс для получения списка всех проектов созданных пользователем
    """
    permission_classes = [IsActive, IsPhoneConfirmed]
    serializer_class = ProjectSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProjectFilter

    def get_queryset(self):
        return self.request.user.account_projects.all()


@method_decorator(cache_page(60 * 60, cache='project_cache'), name='dispatch')
class ProjectApprovedListView(ListAPIView):
    """
    Класс для получения списка всех опубликованных проектов
    """
    permission_classes = [AllowAny]
    serializer_class = ProjectSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProjectFilter

    def get_queryset(self):
        return Project.objects.filter(is_approved=True)


@method_decorator(cache_page(60 * 60, cache='project_cache'), name='dispatch')
class ProjectAllListView(ListAPIView):
    """
    Класс для получения списка всех проектов
    """
    permission_classes = [IsSuperUserOrModeratorUser, IsActive, IsPhoneConfirmed]
    serializer_class = ProjectSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProjectFilter

    def get_queryset(self):
        return Project.objects.all()


class ProjectAttachmentUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """
    Класс для удаления и изменения файлов проекта
    """
    permission_classes = [IsUploadsOwnerOrSuperUserOrModerator, IsActive, IsPhoneConfirmed]
    queryset = Attachment.objects.all()
    serializer_class = AttachmentUpdateSerializer

    def put(self, request, *args, **kwargs):
        return Response({"detail": "Метод \"PUT\" не разрешен."},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ProjectAttachmentUploadView(CreateAPIView, IsOwnerOrSuperUserOrModerator):
    """
    Класс загрузки файлов к проекту
    """
    permission_classes = [IsActive, IsPhoneConfirmed]
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer

    def create(self, request, *args, **kwargs):
        """
        Перед загрузкой проверяем, что пользователю принадлежит проект
        400 если превышено максимальное количество файлов
        403 если недостаточно прав для загрузки фото для данной проблемы
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not self.has_object_permission(request=request, view=self,
                                          obj=serializer.validated_data['project']):
            return Response({"account": "Недостаточно прав для выполнения данного действия"},
                            status=status.HTTP_403_FORBIDDEN)

        if Attachment.objects.filter(
                project=serializer.validated_data['project']).count() >= settings.MAX_NUMBER_OF_ATTACHMENTS_PER_PROJECT:
            return Response(
                {
                    "attachment": "Превышено максимально число файлов: %s" % settings.MAX_NUMBER_OF_ATTACHMENTS_PER_PROJECT},
                status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ProjectLinkUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """
    Класс для удаления и изменения ссылок проекта
    """
    permission_classes = [IsUploadsOwnerOrSuperUserOrModerator, IsActive, IsPhoneConfirmed]
    queryset = Link.objects.all()
    serializer_class = LinkShortSerializer

    def put(self, request, *args, **kwargs):
        return Response({"detail": "Метод \"PUT\" не разрешен."},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ProjectLinkAddView(CreateAPIView, IsOwnerOrSuperUserOrModerator):
    """
    Класс добавления ссылок к проекту
    """
    permission_classes = [IsActive, IsPhoneConfirmed]
    queryset = Link.objects.all()
    serializer_class = LinkSerializer

    def create(self, request, *args, **kwargs):
        """
        Перед добавлением проверяем, что пользователю принадлежит проект
        400 если превышено максимальное количество файлов
        403 если недостаточно прав для загрузки фото для данной проблемы
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not self.has_object_permission(request=request, view=self,
                                          obj=serializer.validated_data['project']):
            return Response({"account": "Недостаточно прав для выполнения данного действия"},
                            status=status.HTTP_403_FORBIDDEN)

        if Link.objects.filter(
                project=serializer.validated_data['project']).count() >= settings.MAX_NUMBER_OF_LINKS_PER_PROJECT:
            return Response(
                {
                    "link": "Превышено максимально число ссылок: %s" % settings.MAX_NUMBER_OF_LINKS_PER_PROJECT},
                status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ProjectCommentAddView(CreateAPIView):
    permission_classes = [IsActive, IsPhoneConfirmed]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        """
        Перед добавлением проверяем, что пользователю принадлежит проект
        400 если превышено максимальное количество файлов
        403 если недостаточно прав для загрузки фото для данной проблемы
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if 'parent' in serializer.validated_data:
            if serializer.validated_data['parent'].project != serializer.validated_data['project']:
                return Response({"comment": "Проект родителя должен совпадать с проектом комментария"},
                                status=status.HTTP_400_BAD_REQUEST)
            if serializer.validated_data['parent'].parent is not None:
                return Response({"comment": "Глубина ответов превышена"}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(account=self.request.user)


class ProjectCommentUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrSuperUserOrModerator, IsActive, IsPhoneConfirmed]
    queryset = Comment.objects.all()
    serializer_class = CommentUpdateSerializer

    def put(self, request, *args, **kwargs):
        return Response({"detail": "Метод \"PUT\" не разрешен."},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ProjectCommentAllListView(ListAPIView):
    """
    Класс для получения списка всех комментариев для проекта
    """
    permission_classes = [AllowAny]
    serializer_class = CommentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CommentFilter

    def get_queryset(self):
        pk = self.kwargs['pk']
        try:
            project = Project.objects.get(pk=pk)
            return project.project_comments.filter(parent=None)
        except Project.DoesNotExist:
            raise Http404


class ProjectCommentRepliesListView(ListAPIView):
    """
    Класс для получения списка всех ответов на комментарий
    """
    permission_classes = [AllowAny]
    serializer_class = CommentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CommentFilter

    def get_queryset(self):
        pk = self.kwargs['pk']
        try:
            parent = Comment.objects.get(pk=pk)
            return Comment.objects.filter(parent=parent)
        except Comment.DoesNotExist:
            raise Http404


class ProjectLikeDislikeView(APIView):
    """
    Класс для установки лайка на проект
    """
    permission_classes = [IsActive, IsPhoneConfirmed]

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        is_liked = 0
        try:
            project = Project.objects.get(pk=pk)
            serializer = VoteTypeSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            vote_type = serializer.validated_data.get('vote_type')
            like_dislike = LikeDislike.objects.get(content_type=ContentType.objects.get_for_model(project),
                                                   object_id=project.id,
                                                   account=request.user)
            if like_dislike.vote is not vote_type:
                like_dislike.vote = vote_type
                like_dislike.save(update_fields=['vote'])
                is_liked = vote_type
            else:
                like_dislike.delete()
                is_liked = 0
        except Project.DoesNotExist:
            raise Http404
        except LikeDislike.DoesNotExist:
            project.votes.create(account=request.user, vote=vote_type)
            is_liked = vote_type

        project = Project.objects.get(pk=pk)
        return Response(
            {"project_id": project.id,
             "is_liked": is_liked,
             "likes_count": project.likes_count,
             "dislikes_count": project.dislikes_count,
             "rating": project.rating,
             }, status=status.HTTP_200_OK
        )


class ProjectCommentLikeDislikeView(APIView):
    """
    Класс для установки лайка на комментарий
    """
    permission_classes = [IsActive, IsPhoneConfirmed]

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        is_liked = 0
        try:
            comment = Comment.objects.get(pk=pk)
            serializer = VoteTypeSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            vote_type = serializer.validated_data.get('vote_type')
            like_dislike = LikeDislike.objects.get(content_type=ContentType.objects.get_for_model(comment),
                                                   object_id=comment.id,
                                                   account=request.user)
            if like_dislike.vote is not vote_type:
                like_dislike.vote = vote_type
                like_dislike.save(update_fields=['vote'])
                is_liked = vote_type
            else:
                like_dislike.delete()
                is_liked = 0
        except Comment.DoesNotExist:
            raise Http404
        except LikeDislike.DoesNotExist:
            comment.votes.create(account=request.user, vote=vote_type)
            is_liked = vote_type

        comment = Comment.objects.get(pk=pk)
        return Response(
            {"comment_id": comment.id,
             "is_liked": is_liked,
             "likes_count": comment.likes_count,
             "dislikes_count": comment.dislikes_count,
             "rating": comment.rating,
             }, status=status.HTTP_200_OK
        )
