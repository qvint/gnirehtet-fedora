# Should be disabled in COPR, I guess.
%bcond_with build_apk

%if %{with build_apk}
%{error:Not implemented yet}
%endif

Name:           gnirehtet
Version:        2.3
Release:        1%{?dist}
Summary:        Gnirehtet provides reverse tethering for Android

%global committish v%{version}
%global has_official_apk 1

%if !%{has_official_apk} && !%{with build_apk}
%{error:This version of %{name} is not shipped with official prebuilt APK}
%endif

License:        ASL 2.0
URL:            https://github.com/Genymobile/%{name}

Source0:        https://github.com/Genymobile/%{name}/archive/%{committish}/%{name}-%{committish}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        vendored-sources-%{version}.tar.gz
%if !%{with build_apk}
Source2:        https://github.com/Genymobile/%{name}/releases/download/%{committish}/%{name}-rust-linux64-%{committish}.zip
%endif
Patch0:         %{name}-%{version}-paths.patch

ExclusiveArch:  x86_64
BuildRequires:  rust-packaging
Requires:       /usr/bin/adb

%description
Gnirehtet provides reverse tethering over adb for Android: it allows devices to
use the internet connection of the computer they are plugged on. It does not
require any root access (neither on the device nor on the computer).

%prep
%global cargo_registry %{_builddir}/%{name}-%{version}/vendored-sources

%autosetup -p1 -n %{name}-%{version}
tar xf %{SOURCE1}

pushd relay-rust
%{cargo_prep}
popd

%if !%{with build_apk}
unzip -p %{SOURCE2} %{name}-rust-linux64/%{name}.apk > %{name}.apk
%endif

%build
pushd relay-rust
%{cargo_build}
popd

%install
pushd relay-rust
%{__cargo} install %{__cargo_common_opts}
rm %{buildroot}%{_prefix}/.crates.toml
popd

mkdir -p %{buildroot}%{_datadir}/%{name}
install -m644 %{name}.apk %{buildroot}%{_datadir}/%{name}

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*

%changelog
* Mon Oct 14 2019 qvint <dotqvint@gmail.com> - 2.3-1
- Initial release
