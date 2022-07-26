from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform, Review
from watchlist_app.api.validations import WatchListValidations


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ['watchlist']


class WatchListSerializer(serializers.ModelSerializer):
    len_name = serializers.SerializerMethodField(method_name='get_len_name')
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = WatchList
        fields = "__all__"
        extra_fields = ['len_name']
        read_only_fields = ['id', 'created_at']
        required_fields = ['title', 'storyLine']

        @staticmethod
        def create(self, validated_data):
            return WatchList.objects.create(**validated_data)

        @staticmethod
        def update(self, instance, validated_data):
            instance.title = validated_data.get('title', instance.title)
            instance.description = validated_data.get('storyLine', instance.description)
            instance.active = validated_data.get('active', instance.active)
            instance.save()
            return instance

        validators = [WatchListValidations.validate_title, WatchListValidations.validate_description,
                      WatchListValidations.validate_equals]

    @staticmethod
    def get_len_name(obj):
        return len(obj.title)


class StreamPlatformSerializer(serializers.HyperlinkedModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)
    #watchlist = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='movie_details')

    class Meta:
        model = StreamPlatform
        fields = "__all__"
        read_only_fields = ['id']
        required_fields = ['name', 'about', 'webSite']


