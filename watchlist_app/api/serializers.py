from rest_framework import serializers
from watchlist_app.models import WatchList
from watchlist_app.api.validations import WatchListValidations


class WatchListSerializer(serializers.ModelSerializer):
    len_name = serializers.SerializerMethodField(method_name='len_name')

    class Meta:
        model = WatchList
        fields = "__all__"
        read_only_fields = ['id', 'len_name', 'created_at']
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

    def len_name(self, obj):
        return len(obj.title)
