from urllib.parse import urlsplit, urlunsplit
from collections import OrderedDict

from django.views.generic import TemplateView

import ramlfications

from ramlgnarok.loader import RAMLgnarokLoader


def get_base_uri(request):
    url_parts = urlsplit(request.build_absolute_uri())
    return urlunsplit((url_parts[0], url_parts[1], '', '', ''))


class RAMLDocs(TemplateView):
    template_name = 'base.html'

    def parse(self, raml_file, override_file=None):
        loader = RAMLgnarokLoader().load(raml_file)
        config = ramlfications.setup_config(None)
        api = ramlfications.parse_raml(loader, config)

        resources = OrderedDict()

        for resource in api.resources:
            resource.children = []
            resource.methods = OrderedDict()
            resource.methods[resource.method] = resource

            if resource.query_params:
                resource.query_params_optional = []
                resource.query_params_required = []
                for query_param in resource.query_params:
                    if query_param.required:
                        resource.query_params_required.append(query_param)
                    else:
                        resource.query_params_optional.append(query_param)

            if resource.parent:
                resource.parent.children.append(resource)

            if resource.path in resources:
                resources[resource.path].methods[resource.method] = resource
            else:
                resources[resource.path] = resource
        # import pdb; pdb.set_trace()
        return {'api': api, 'resources': resources}

    def get_context_data(self, **kwargs):
        ctx = super(RAMLDocs, self).get_context_data(**kwargs)
        ctx.update(self.parse(**kwargs))
        return ctx
