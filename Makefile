IMAGE=satishweb/xrdp
# PLATFORMS=linux/amd64,linux/arm64,linux/arm/v7,linux/ppc64le
PLATFORMS=linux/amd64,linux/arm64
# PLATFORMS=linux/arm64
WORKDIR=$(shell pwd)
XRDP_VERSION?=$(shell sudo docker run --rm --entrypoint=bash public.ecr.aws/ubuntu/ubuntu:22.04 -c \
		"set -x; apt update >/dev/null 2>&1; \
		apt-cache madison xrdp \
		|cut -d \| -f 2 \
		|sed 's/ //g'" \
	)

ifdef PUSH
	EXTRA_BUILD_PARAMS = --push-images --push-git-tags
endif

ifdef LATEST
	EXTRA_BUILD_PARAMS += --mark-latest
endif

ifdef NO-CACHE
	EXTRA_BUILD_PARAMS += --no-cache
endif

ifdef LOAD
	EXTRA_BUILD_PARAMS += --load
endif

test-env:
	echo "test-env: printing env values:"
	echo "XRDP Version: ${XRDP_VERSION}"
	exit 1

all: build

build:
	./build.sh \
	  --image-name "${IMAGE}" \
	  --platforms "${PLATFORMS}" \
	  --work-dir "${WORKDIR}" \
	  --git-tag "${XRDP_VERSION}" \
	  --extra-args "--build-arg XRDP_VERSION=${XRDP_VERSION}" \
	${EXTRA_BUILD_PARAMS}

test:
	sudo docker build --build-arg XRDP_VERSION=${XRDP_VERSION} -t ${IMAGE}:${XRDP_VERSION} .
