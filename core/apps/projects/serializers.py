from rest_framework import serializers
from .models import Category, Project, Attachment, Link, LikeDislike, Comment
from .service import is_liked
from ..accounts.serializers import AccountShortSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = '__all__'


class AttachmentShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['id', 'uploaded_file', 'name', 'is_feature']


class AttachmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['id', 'uploaded_file', 'is_feature']


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = '__all__'


class LinkShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['id', 'url']


class ProjectSerializer(serializers.ModelSerializer):
    account = AccountShortSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    is_liked = serializers.SerializerMethodField(read_only=True)
    is_personal = serializers.BooleanField(required=True)
    attachments = AttachmentShortSerializer(read_only=True, many=True, source='project_attachments')
    links = LinkShortSerializer(read_only=True, many=True, source='project_links')
    uploaded_files = serializers.ListField(child=serializers.FileField(allow_empty_file=False),
                                           write_only=True, allow_empty=False, allow_null=False, required=False)
    uploaded_links = serializers.ListField(child=serializers.URLField(allow_blank=False),
                                           write_only=True, allow_empty=False, allow_null=False, required=False)

    def get_is_liked(self, obj) -> int:
        user = self.context.get('request').user
        return is_liked(obj, user)

    class Meta:
        model = Project
        fields = ['id', 'account', 'category', 'description', 'is_personal', 'is_approved', 'is_feature',
                  'likes_count', 'dislikes_count', 'rating', 'created_at', 'updated_at', 'is_liked', 'attachments',
                  'links', 'uploaded_files', 'uploaded_links', ]

    def create(self, validated_data):
        project = Project.objects.create(account=validated_data.get('account'),
                                         description=validated_data.get('description'),
                                         is_personal=validated_data.get('is_personal'))
        if "uploaded_files" in validated_data:
            uploaded_files = validated_data.pop('uploaded_files')
            for file in uploaded_files:
                Attachment.objects.create(project=project, uploaded_file=file)

        if "uploaded_links" in validated_data:
            uploaded_urls = validated_data.pop('uploaded_links')
            for url in uploaded_urls:
                Link.objects.create(project=project, url=url)

        return project


class ProjectSuperUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'account', 'category', 'description', 'is_personal', 'is_approved', 'is_feature',
                  'created_at', 'updated_at', ]


class ProjectShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'description', 'is_personal']


class CommentSerializer(serializers.ModelSerializer):
    account = AccountShortSerializer(read_only=True)
    is_liked = serializers.SerializerMethodField(read_only=True)

    def get_is_liked(self, obj) -> int:
        user = self.context.get('request').user
        return is_liked(obj, user)

    class Meta:
        model = Comment
        fields = '__all__'


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content']


class VoteTypeSerializer(serializers.Serializer):
    vote_type = serializers.ChoiceField(choices=LikeDislike.VOTES)
