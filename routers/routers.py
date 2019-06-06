import itertools
import os
import re
from collections import namedtuple
from typing import Any, Iterable, Pattern, Union

import tornado.web

Route = namedtuple("Route", ("detail", "mapping"))


class Router(object):
    def __init__(
        self, api_prefix: str = "/", trailing_slash: bool = False
    ) -> None:
        self.api_prefix = api_prefix
        self.trailing_slash = "/" if trailing_slash else ""
        self.registry = []

    def register(
        self,
        pattern: Union[str, Pattern],
        handler: Any,
        kwargs: dict = None,
        name: str = None
    ) -> None:
        if hasattr(self, "_rules"):
            del self._rules
        self.registry.append((pattern, handler, kwargs, name))

    def get_rules(self) -> list:
        raise NotImplementedError("`get_rules` must be overridden.")

    @property
    def rules(self) -> list:
        if not hasattr(self, "_rules"):
            self._rules = self.get_rules()
        return self._rules


class GenericRouter(Router):
    def get_rules(self) -> list:
        rules = []
        for pattern, handler, kwargs, name in self.registry:
            pattern = os.path.join(
                self.api_prefix, pattern.strip("/")
            ) + self.trailing_slash
            rules.append(tornado.web.url(pattern, handler, kwargs, name))
        return rules


class NestedRouter(Router):
    routes = [
        Route(detail=False, mapping={
            "get": "list",
            "post": "create"
        }),
        Route(
            detail=True,
            mapping={
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy"
            }
        )
    ]

    def register(
        self,
        resources: Union[Iterable[str], str],
        handler: Any,
        kwargs: dict = None,
        name: str = None
    ) -> None:
        if isinstance(resources, str):
            resources = (resources, )
        for resource in resources:
            if not re.match(r"^[a-zA-Z0-9_-]+$", resource):
                raise AssertionError(f"Invalid resource name `{resource}`.")
        super().register(resources, handler, kwargs, name)

    def get_lookup_regexs(
        self, resources: Iterable[str], handler: Any
    ) -> list:
        base_regex = "(?P<{lookup_url_kwarg}>{lookup_value_regex})"
        lookup_field = getattr(handler, "lookup_field", "pk")
        lookup_value = getattr(handler, "lookup_value", "[^/.]+")
        lookup_url_kwargs = getattr(
            handler, "lookup_url_kwargs",
            tuple(
                map(lambda x: x.rstrip("s") + "_" + lookup_field, resources)
            ) if len(resources) > 1 else (lookup_field, )
        )
        lookup_value_regexs = getattr(
            handler, "lookup_value_regexs", (lookup_value, ) * len(resources)
        )
        if not len(lookup_url_kwargs) == len(lookup_value_regexs):
            raise AssertionError(
                "Attribute `lookup_url_kwargs` and `lookup_value_regexs` "
                "have different lengths."
            )
        lookup_regexs = []
        for kwarg, regex in zip(lookup_url_kwargs, lookup_value_regexs):
            lookup_regex = base_regex.format(
                lookup_url_kwarg=kwarg, lookup_value_regex=regex
            )
            lookup_regexs.append(lookup_regex)
        return lookup_regexs

    def get_method_map(self, handler: Any, mapping: dict) -> dict:
        method_map = {}
        for method, action in mapping.items():
            if hasattr(handler, action):
                method_map[method] = action
        return method_map

    def get_rules(self) -> None:
        rules = []
        for resources, handler, kwargs, name in self.registry:
            kwargs = {} if not isinstance(kwargs, dict) else kwargs
            regexs = self.get_lookup_regexs(resources, handler)
            zipped = zip(resources, regexs)
            flat = tuple(itertools.chain.from_iterable(zipped))
            standalone = getattr(handler, "standalone", False)
            for route in self.routes:
                mapping = self.get_method_map(handler, route.mapping)
                if not mapping:
                    continue
                if standalone and not route.detail:
                    continue
                pattern = os.path.join(
                    self.api_prefix, "/".join(
                        flat if route.detail and not standalone else flat[:-1]
                    )
                ) + self.trailing_slash
                kwargs.update(mapping=mapping)
                rules.append(
                    tornado.web.url(pattern, handler, kwargs.copy(), name)
                )
        return rules
