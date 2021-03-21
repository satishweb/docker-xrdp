IMAGE=satishweb/xrdp
PLATFORMS=linux/amd64,linux/arm64,linux/arm/v7,linux/ppc64le
WORKDIR=$(shell pwd)
#TAGNAME?=$(shell curl -s https://api.github.com/repos/xx/xx/tags|jq -r '.[0].name')
TAGNAME?=devel
ifdef PUSH
	EXTRA_BUILD_PARAMS = --push-images --push-git-tags
endif

ifdef LATEST
	EXTRA_BUILD_PARAMS += --mark-latest
endif

ifdef NO-CACHE
	EXTRA_BUILD_PARAMS += --no-cache
endif

all:
	./build.sh \
	  --image-name "${IMAGE}" \
	  --platforms "${PLATFORMS}" \
	  --work-dir "${WORKDIR}" \
	  --git-tag "${TAGNAME}" \
	  ${EXTRA_BUILD_PARAMS}
