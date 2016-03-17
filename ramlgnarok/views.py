from urllib.parse import urlsplit, urlunsplit
from collections import OrderedDict

from django.views.generic import TemplateView
from django.template.loader import render_to_string

import ramlfications

from ramlgnarok.loader import RAMLgnarokLoader


def get_base_uri(request):
    url_parts = urlsplit(request.build_absolute_uri())
    return urlunsplit((url_parts[0], url_parts[1], '', '', ''))


class RAMLDocs(TemplateView):
    template_name = 'raml_docs_base.html'

    def parse(self, raml_file, override_file=None):
        raml = render_to_string(
            'raml/{}.raml'.format(raml_file),
            {'base_url': get_base_uri(self.request)}
        )
        override_raml = None
        if override_file:
            override_raml = render_to_string(
                'raml/overrides/{}.raml'.format(override_file),
            )
        loader = RAMLgnarokLoader().load(raml, override_raml)
        config = ramlfications.setup_config(None)
        api = ramlfications.parse_raml(loader, config)

        resources = OrderedDict()

        for resource in api.resources:
            resource.children = []
            resource.methods = OrderedDict()
            resource.methods[resource.method] = resource
            if resource.parent:
                resource.parent.children.append(resource)

            if resource.path in resources:
                resources[resource.path].methods[resource.method] = resource
            else:
                resources[resource.path] = resource

        return {'api': api, 'resources': resources}

    def get_context_data(self, **kwargs):
        ctx = super(RAMLDocs, self).get_context_data(**kwargs)
        ctx.update(self.parse(**kwargs))
        return ctx
