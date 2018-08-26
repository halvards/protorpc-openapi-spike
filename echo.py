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

import endpoints
from protorpc import messages
from protorpc import remote


class EchoRequest(messages.Message):
    content = messages.StringField(1)


class EchoResponse(messages.Message):
    content = messages.StringField(1)


@endpoints.api(name='echo',
               version='v1',
               base_path='/echo/')
class EchoApi(remote.Service):
    """base_path _must_ begin and end with '/'"""

    @endpoints.method(request_message=EchoRequest,
                      response_message=EchoResponse,
                      name='echo',
                      path='echo')
    def echo(self, request):
        """Method name _must_ match decorator path attribute."""
        return EchoResponse(content=request.content)


api = endpoints.api_server([EchoApi])
