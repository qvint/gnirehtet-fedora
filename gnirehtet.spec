Name:           gnirehtet
Version:        2.5
Release:        1%{?dist}
Summary:        Gnirehtet provides reverse tethering for Android

License:        ASL 2.0
URL:            https://github.com/Genymobile/%{name}

%global committish v%{version}

Source0:        https://github.com/Genymobile/%{name}/archive/%{committish}/%{name}-%{committish}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        https://github.com/Genymobile/%{name}/releases/download/%{committish}/%{name}-rust-linux64-%{committish}.zip
Source2:        vendored-sources-%{version}.tar.gz
Patch0:         %{name}-%{version}-paths.patch

ExclusiveArch:  x86_64
BuildRequires:  rust-packaging
Requires:       /usr/bin/adb

%description
Gnirehtet provides reverse tethering over adb for Android: it allows devices to
use the internet connection of the computer they are plugged on. It does not
require any root access (neither on the device nor on the computer).

%prep
%setup -qTn %{name}-rust-linux64 -b1
%setup -qTn vendored-sources -b2
%setup -qn %{name}-%{version}

%global cargo_registry %{_builddir}/vendored-sources
%global prebuilt_root %{_builddir}/%{name}-rust-linux64

%autopatch -p1

pushd relay-rust
%{cargo_prep}
popd

%build
pushd relay-rust
%{cargo_build}
popd

%install
pushd relay-rust
%{__cargo} install --no-track --path . %{__cargo_common_opts}
popd

mkdir -p %{buildroot}%{_datadir}/%{name}
install -m644 %{prebuilt_root}/%{name}.apk %{buildroot}%{_datadir}/%{name}

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*

%changelog
* Sun Aug 16 2020 qvint <dotqvint@gmail.com> - 2.5-1
- Update to 2.5
- Clean up spec file

* Sun May 03 2020 qvint <dotqvint@gmail.com> - 2.4-2
- Use --no-track option for 'cargo install'

* Mon Nov 18 2019 qvint <dotqvint@gmail.com> - 2.4-1
- Update to 2.4

* Mon Oct 14 2019 qvint <dotqvint@gmail.com> - 2.3-1
- Initial release
