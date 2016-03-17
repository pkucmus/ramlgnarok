from collections import OrderedDict, Mapping
import yaml

from ramlfications.loader import RAMLLoader
from ramlfications.errors import LoadRAMLError


class RAMLgnarokLoader(RAMLLoader):

    def update(self, d, u):
        for k, v in u.items():
            if d is None:
                d = u
            else:
                if isinstance(v, Mapping):
                    r = self.update(d.get(k, {}), v)
                    d[k] = r
                else:
                    d[k] = u[k]
        return d

    def _ordered_load(
        self, stream, overload_stream=None, loader=yaml.SafeLoader
    ):
        class OrderedLoader(loader):
            pass

        def construct_mapping(loader, node):
            loader.flatten_mapping(node)
            return OrderedDict(loader.construct_pairs(node))
        OrderedLoader.add_constructor("!include", self._yaml_include)
        OrderedLoader.add_constructor(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)

        self._ordered_loader = OrderedLoader

        data = yaml.load(stream, OrderedLoader)

        if overload_stream:
            overload_data = yaml.load(overload_stream, OrderedLoader)
            data = self.update(data, overload_data)

        return data

    def load(self, raml, raml_overload):
        try:
            return self._ordered_load(
                stream=raml,
                overload_stream=raml_overload,
                loader=yaml.SafeLoader,
            )
        except yaml.parser.ParserError as e:
            msg = "Error parsing RAML: {0}".format(e)
            raise LoadRAMLError(msg)
        except yaml.constructor.ConstructorError as e:
            msg = "Error parsing RAML: {0}".format(e)
            raise LoadRAMLError(msg)
