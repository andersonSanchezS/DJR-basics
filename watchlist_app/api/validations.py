from rest_framework import serializers


class WatchListValidations:
    @staticmethod
    def validate_title(value):
        if len(value['title']) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long")
        return value

    @staticmethod
    def validate_description(value):
        if len(value['storyLine']) < 10:
            raise serializers.ValidationError("StoryLine must be at least 10 characters long")
        return value

    @staticmethod
    def validate_equals(value):
        if value['title'] != value['storyLine']:
            return value
        raise serializers.ValidationError("Title and Description cannot be equal")
