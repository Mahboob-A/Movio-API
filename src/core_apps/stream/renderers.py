import json

from rest_framework.renderers import JSONRenderer


class VideoMetaDataJSONRenderer(JSONRenderer):
    """Defalut renderer class for single VideoMetadata or Subtitele object."""

    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context is None:
            status_code = 200
        else:
            status_code = renderer_context.get("response").status_code

        if data is not None:
            errors = data.get("errors", None)
        else:
            errors = None

        if errors is not None:
            return super(VideoMetaDataJSONRenderer, self).render(data)
        else:
            return json.dumps({"status_code": status_code, "video": data})


class VideosMetadataJSONRenderer(JSONRenderer):
    """Defalut Renderer class for VideoMetadata Queryset"""

    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context is None:
            status_code = 200
        else:
            status_code = renderer_context.get("response").status_code

        errors = data.get("errors", None)

        # if there are errors, then render as per default JSON style. Pass if errors is None
        if errors is not None:
            return super(VideosMetadataJSONRenderer, self).render(data)
        else:
            return json.dumps({"status_code": status_code, "videos": data})
