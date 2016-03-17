import os

from collections import OrderedDict, Mapping
import yaml

from django.template.loader import render_to_string

from ramlfications.loader import RAMLLoader
from ramlfications.errors import LoadRAMLError


class RAMLgnarokLoader(RAMLLoader):

    extended_data = None

    def _yaml_include(self, loader, node):
        """
        Adds the ability to follow ``!include`` directives within
        RAML Files.
        """
        file_ext = os.path.splitext(node.value)[1]
        parsable_ext = [".yaml", ".yml", ".raml", ".json"]

        stream = self._render(node.value)

        if file_ext not in parsable_ext:
            return stream

        # if file_ext == ".json":
        #     return self._parse_json(file_name, os.path.dirname(file_name))

        return load(stream, self._ordered_loader)

    def _extends(self, loader, node):
        assert node.start_mark.line == 0, (
            '!extends should be defined once in the first line of '
            'the RAML file'
        )
        loader.extended_data = load(
            self._render(node.value), self._ordered_loader
        )

    def _ordered_load(
        self, raml, loader=yaml.SafeLoader, **ctx
    ):
        class OrderedLoader(loader):
            pass

        def construct_mapping(loader, node):
            loader.flatten_mapping(node)
            return OrderedDict(loader.construct_pairs(node))
        OrderedLoader.add_constructor("!include", self._yaml_include)
        OrderedLoader.add_constructor("!extends", self._extends)
        OrderedLoader.add_constructor(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)

        self._ordered_loader = OrderedLoader

        stream = self._render('{}.raml'.format(raml))

        data = load(stream, OrderedLoader)

        return data

    def _render(self, template_file):
        return render_to_string(
            'raml/{}'.format(template_file), self.ctx
        )

    def load(self, raml, **ctx):
        self.ctx = ctx
        try:
            return self._ordered_load(
                raml=raml,
                loader=yaml.SafeLoader
            )
        except yaml.parser.ParserError as e:
            msg = "Error parsing RAML: {0}".format(e)
            raise LoadRAMLError(msg)
        except yaml.constructor.ConstructorError as e:
            msg = "Error parsing RAML: {0}".format(e)
            raise LoadRAMLError(msg)


def update(d, u):
    for k, v in u.items():
        if d is None:
            d = u
        else:
            if isinstance(v, Mapping):
                r = update(d.get(k, {}), v)
                d[k] = r
            else:
                d[k] = u[k]
    return d


def load(stream, Loader=None):
    """
    Parse the first YAML document in a stream
    and produce the corresponding Python object.
    """
    loader = Loader(stream)
    try:
        data = loader.get_single_data()
        if hasattr(loader, 'extended_data'):
            data = update(loader.extended_data, data)
        return data
    finally:
        loader.dispose()
