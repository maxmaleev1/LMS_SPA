from rest_framework.serializers import ValidationError


class URLValidator:
    def __call__(self, link):
        if "youtube.com" not in link:
            raise ValidationError("Можно добавлять ссылки только на youtube.com")
