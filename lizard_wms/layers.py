from django.utils import simplejson as json

"""Defining lizard_wms' adapter."""
import logging

from lizard_map.workspace import WorkspaceItemAdapter
from lizard_wms import models

logger = logging.getLogger(__name__)


class AdapterWMS(WorkspaceItemAdapter):
    """
    Adapter. Tries to get information for X,Y points using
    GetFeatureInfo requests.
    """

    @property
    def wms_source(self):
        """Helper method that returns this layer's WMSSource
        object. wms_source_id is given in adapter_layer_json."""
        if not hasattr(self, '_wms_source'):
            self._wms_source = models.WMSSource.objects.get(
                pk=self.layer_arguments['wms_source_id'])

        return self._wms_source

    def layer(self, layer_ids=None, request=None):
        return [], {}

    def location(self, x, y):
        """This can't possibly be correct, but it works."""

        search = self.search(x, y)
        if search:
            return search[0]

    def search(self, x, y, radius=None):
        """Get information about features at x, y from this WMS layer.

        The construction of the result is somewhat difficult: what do we use
        as the identifier of whatever is returned, what as the name?

        It seems that we can't do better than use a x, y value as
        identifier, it's the only bit of information we have that can
        be used to reconstruct the object.
        """

        feature_info = self.wms_source.get_feature_info(x, y)
        name = self.wms_source.get_feature_name(feature_info)

        if feature_info:
            return [{
                    'name': name,
                    'distance': 0,
                    'workspace_item': self.workspace_item,
                    'identifier': {
                        'x': x,
                        'y': y
                        },
                    }]
        else:
            return []

    def html(self, identifiers, layout_options=None):
        identifier = identifiers[0]

        feature_info = self.wms_source.get_feature_info(identifier['x'],
                                                        identifier['y'])

        return self.html_default(identifiers=identifiers,
                                 template="lizard_wms/popup.html",
                                 layout_options=layout_options,
                                 extra_render_kwargs={
                'feature_info': self.wms_source.get_popup_info(feature_info),
                })

    def symbol_url(self, identifier=None, start_date=None, end_date=None):
        """
        returns symbol
        """
        icon_style = {
            'icon': 'polygon.png',
            'mask': ('mask.png', ),
            'color': (0, 1, 0, 0)}

        return super(AdapterWMS, self).symbol_url(
            identifier=identifier,
            start_date=start_date,
            end_date=end_date,
            icon_style=icon_style)

    def legend_image_url(self):
        """Return url with WMS legend image."""
        if 'legend_url' in self.layer_arguments:
            legend_url = self.layer_arguments['legend_url']
            if legend_url:
                return legend_url
        wms_url = self.layer_arguments['url']
        params_json = self.layer_arguments['params']
        params = json.loads(params_json)
        layer = params['layers']
        url_template = (
            "%s?REQUEST=GetLegendGraphic&FORMAT=image/png" +
            "&WIDTH=20&HEIGHT=20&transparent=false&bgcolor=0xffffff&" +
            "LAYER=%s")
        return url_template % (wms_url, layer)

    def extent(self, identifiers=None):
        extent = {'north': None, 'south': None, 'east': None, 'west': None}

        if self.wms_source and self.wms_source.bbox:
            minx, miny, maxx, maxy = self.wms_source.bounding_box
            extent = {'north': maxy, 'south': miny, 'east': maxx, 'west': minx}

        logger.debug("EX-TENT: " + repr(extent))
        return extent

