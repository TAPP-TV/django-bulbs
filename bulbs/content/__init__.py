def get_content_fields_model():
    from django.conf import settings
    from django.core.exceptions import ImproperlyConfigured

    # get the name of the content fields abstract model that should be used on the base content object
    full_name = getattr(settings, 'BULBS_CONTENT_FIELDS', 'bulbs.content.models.ContentFields')
    module_name, model_name = full_name.rsplit('.', 1)
    try:
        model = getattr(__import__(module_name, None, None, 'models'), model_name)
    except ValueError:
        raise ImproperlyConfigured("Error importing BULBS_CONTENT_FIELDS model")
    return model

class TagCache:

    _cache = {}  # Maybe too terrible?

    @classmethod
    def count(cls, slug):
        from .models import Content
        # Gets the count for a tag, hopefully form an in-memory cache.
        cnt = cls._cache.get(slug)
        if cnt is None:
            cnt = Content.search_objects.query(**{"tags.slug": slug}).count()
            cls._cache[slug] = cnt
        return cnt
