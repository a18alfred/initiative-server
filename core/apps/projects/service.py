from django_filters import rest_framework as filters
from .models import Project, Comment, LikeDislike
from django.contrib.contenttypes.models import ContentType


class ProjectFilter(filters.FilterSet):
    """
    Фильтр для работы со списком проектов
    """
    category = filters.AllValuesMultipleFilter()
    is_approved = filters.BooleanFilter(field_name='is_approved')
    is_feature = filters.BooleanFilter(field_name='is_feature')
    rating = filters.RangeFilter()
    created_at = filters.DateTimeFromToRangeFilter()

    o = filters.OrderingFilter(fields=['created_at', 'rating'])

    class Meta:
        model = Project
        fields = ['category', 'is_approved', 'is_feature', 'rating', 'created_at']


class CommentFilter(filters.FilterSet):
    """
    Фильтр для работы со списком комментариев
    """
    created_at = filters.DateTimeFromToRangeFilter()
    rating = filters.RangeFilter()

    o = filters.OrderingFilter(fields=['created_at', 'rating'])

    class Meta:
        model = Comment
        fields = ['created_at', 'rating']


def is_liked(obj, user) -> int:
    """
    Проверяем лайкнул ли пользователь объект
    0 нет,
    1 лайк
    -1 дизлайк
    """
    if not user.is_authenticated:
        return 0

    try:
        likedislike = LikeDislike.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.id,
                                              account=user)
        return likedislike.vote
    except LikeDislike.DoesNotExist:
        return 0
