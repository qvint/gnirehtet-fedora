#!/usr/bin/env bash
# shellcheck disable=SC2164

spec_dir="$(pwd)"
temp_dir="$(mktemp --directory)"
package_version="$(rpmspec \
  --srpm --query --queryformat='%{VERSION}\n' "${spec_dir}/gnirehtet.spec")"
gnirehtet_archive="${spec_dir}/gnirehtet-${package_version}.tar.gz"
output_archive="${spec_dir}/vendored-sources-${package_version}.tar.gz"

cd "${temp_dir}"
tar xf "${gnirehtet_archive}" --strip-components=1
mkdir vendored-sources
(cd relay-rust; cargo vendor ../vendored-sources)
tar cf "${output_archive}" vendored-sources

rm -rf "${temp_dir}"
