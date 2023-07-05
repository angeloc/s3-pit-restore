#!/bin/bash
BUILD_DATE="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
VCS_REF="$(git rev-parse --short=7 HEAD)"
VERSION="$(git rev-parse --abbrev-ref HEAD)"
docker build --build-arg BUILD_DATE="$BUILD_DATE" --build-arg VCS_REF="$VCS_REF" --build-arg VERSION="$VERSION" -t angelocompagnucci/s3-pit-restore .
