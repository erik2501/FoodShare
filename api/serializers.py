from django.contrib.auth.models import User
from django.db.models import Count
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from taggit.models import Tag
from taggit.serializers import TaggitSerializer, TagListSerializerField

from .models import Comment, Like, Recipe, UserFollow


class TagListSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ("id", "name", "count")

    def get_count(self, obj):
        return Recipe.objects.filter(tags=obj).count()


class RecipeSerializer(TaggitSerializer, serializers.ModelSerializer):

    comment_count = serializers.IntegerField(
        source="comments.count",
        read_only=True,
        default=-1,
    )

    like_count = serializers.IntegerField(
        source="likes.count",
        read_only=True,
        default=-1,
    )

    username = serializers.CharField(
        source="user.username",
        read_only=True,
        default="N/A",
    )

    tags = TagListSerializerField()

    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
            "id",
            "title",
            "summary",
            "content",
            "prep_time",
            "image",
            "user",
            "username",
            "created",
            "tags",
            "like_count",
            "is_liked",
            "comment_count",
        ]
        read_only_fields = ["user"]  # this is set automatically

    def get_is_liked(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return Like.objects.filter(user=user, recipe=obj).exists()
        return False


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["user"]


class LikeSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(), read_only=True
    )

    class Meta:
        model = Like
        fields = ["id", "recipe", "user", "created"]
        read_only_fields = ["user"]
        validators = [
            UniqueTogetherValidator(
                queryset=Like.objects.all(),
                fields=["user", "recipe"],
            )
        ]


class UserSerializer(serializers.ModelSerializer):

    recipes = serializers.HyperlinkedRelatedField(
        many=True, view_name="recipes-detail", read_only=True
    )

    followers = serializers.IntegerField(
        source="followers.count", default=0, read_only=True
    )

    following = serializers.IntegerField(
        source="following.count", default=0, read_only=True
    )

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "date_joined",
            "last_login",
            "is_superuser",
            "recipes",
            "followers",
            "following",
        ]


class UserFollowSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(), read_only=True
    )

    class Meta:
        model = UserFollow
        fields = "__all__"
        read_only_fields = ["user"]
        validators = [
            UniqueTogetherValidator(
                queryset=UserFollow.objects.all(),
                fields=["user", "follows"],
            )
        ]
