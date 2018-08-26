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

ifndef GOOGLE_CLOUD_PROJECT
  GOOGLE_CLOUD_PROJECT := $(shell gcloud config list --format 'value(core.project)')
endif

ifndef PORT
  PORT := 8080
endif

.PHONY: all generate-api generate-discovery deploy-api deploy-service virtualenv local

all: generate-api generate-discovery deploy-api deploy-service

generate-api:
	python env/lib/python2.7/site-packages/endpoints/endpointscfg.py get_openapi_spec echo.EchoApi --hostname ${GOOGLE_CLOUD_PROJECT}.appspot.com --x-google-api-name

generate-discovery:
	python env/lib/python2.7/site-packages/endpoints/endpointscfg.py get_discovery_doc echo.EchoApi --hostname ${GOOGLE_CLOUD_PROJECT}.appspot.com --output static

deploy-api:
	gcloud endpoints services deploy echov1openapi.json

deploy-service:
	gcloud app deploy app.yaml -q

virtualenv:
	virtualenv -p python2.7 env

local:
	dev_appserver.py --port ${PORT} app.yaml
