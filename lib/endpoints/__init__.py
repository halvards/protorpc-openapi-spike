# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Stub implementation of class and method decorators for Cloud Endpoints.

This allows for using google-endpoints
(https://github.com/cloudendpoints/endpoints-python) at build time to generate
OpenAPI (Swagger) specs from service classes while using ProtoRPC at runtime.
"""

from protorpc import message_types
from protorpc import remote
from protorpc.wsgi import service

#: Override ProtoRPC URL path mapping to use '/' as separator instead of '.'.
#: https://github.com/google/protorpc/blob/v0.12.0/protorpc/wsgi/service.py#L47
service._REQUEST_PATH_PATTERN = '^(%s)(?:\\/([^?]+))$'


def api(name,
        version,
        description=None,
        hostname=None,
        audiences=None,
        scopes=None,
        allowed_client_ids=None,
        canonical_name=None,
        auth=None,
        owner_domain=None,
        owner_name=None,
        package_path=None,
        frontend_limits=None,
        title=None,
        documentation=None,
        auth_level=None,
        issuers=None,
        namespace=None,
        api_key_required=None,
        base_path='/_ah/api/',
        limit_definitions=None,
        use_request_uri=None):
    """Class decorator for API service.

    https://github.com/cloudendpoints/endpoints-python/blob/9da60817aefbb0f2a4b9145c17ee39b9115067b0/endpoints/api_config.py#L994
    """

    def _api(service_class):
        service_class.wrapper_api_name = name
        service_class.wrapper_api_version = version
        service_class.wrapper_api_base_path = base_path
        return service_class

    return _api


def method(request_message=message_types.VoidMessage,
           response_message=message_types.VoidMessage,
           name=None,
           path=None,
           http_method='POST',
           scopes=None,
           audiences=None,
           allowed_client_ids=None,
           auth_level=None,
           api_key_required=None,
           metric_costs=None,
           use_request_uri=None):
    """Method decorator for API endpoint.

    Note that the path attribute _must_ match the name of the decorated method.

    https://github.com/cloudendpoints/endpoints-python/blob/9da60817aefbb0f2a4b9145c17ee39b9115067b0/endpoints/api_config.py#L1263
    """
    return remote.method(request_type=request_message,
                         response_type=response_message)


def api_server(api_services):
    """Set up an WSGIApplication instance for the API services provided.

    https://github.com/cloudendpoints/endpoints-python/blob/9da60817aefbb0f2a4b9145c17ee39b9115067b0/endpoints/apiserving.py#L541
    """
    services = []
    for service_class in api_services:
        service_path = '{}{}/{}'.format(service_class.wrapper_api_base_path,
                                        service_class.wrapper_api_name,
                                        service_class.wrapper_api_version)
        services.append((service_path, service_class))
    return service.service_mappings(services)
