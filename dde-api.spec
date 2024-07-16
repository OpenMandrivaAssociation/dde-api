Name:           dde-api
Release:        1
Version:	6.0.11
Summary:        Go-lang bingding for dde-daemon
License:        GPLv3+
URL:            https://github.com/linuxdeepin/dde-api
Source0:        https://github.com/linuxdeepin/dde-api/archive/refs/tags/%{version}/%{name}-%{version}.tar.gz
Source1:	godeps-for-dde-api-6.0.11.tar.xz

BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(cairo-ft)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(gdk-pixbuf-xlib-2.0)
BuildRequires:  pkgconfig(gudev-1.0)
BuildRequires:  pkgconfig(libcanberra)
BuildRequires:  pkgconfig(libpulse-simple)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(poppler-glib)
BuildRequires:  pkgconfig(polkit-qt5-1)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xi)
#BuildRequires:  deepin-gettext-tools
BuildRequires:  compiler(go-compiler)
BuildRequires:  deepin-gir-generator
BuildRequires:  deepin-gir-generator
BuildRequires:  golang-github-linuxdeepin-dbus-factory
BuildRequires:  golang-deepin-go-lib
BuildRequires:  golang-github-linuxdeepin-go-x11-client
#BuildRequires:  golang(github.com/linuxdeepin/go-dbus-factory/org.bluez)
#BuildRequires:  golang(github.com/disintegration/imaging)
#BuildRequires:  golang(github.com/fogleman/gg)
#BuildRequires:  golang(github.com/nfnt/resize)
#BuildRequires:  golang(gopkg.in/alecthomas/kingpin.v2)
#BuildRequires:  golang(github.com/mattn/go-sqlite3)
#BuildRequires:  golang(github.com/gosexy/gettext)
#BuildRequires:  golang(github.com/rickb777/date)
BuildRequires:  make
BuildRequires:  systemd-rpm-macros
%{?systemd_requires}
Requires:       deepin-desktop-base
Requires:       rfkill

%description
%{summary}.

%package -n golang-%{name}-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n golang-%{name}-devel
%{summary}.

This package contains library source intended for
building other packages which use import path with
%{goipath} prefix.

%prep
%autosetup -p1 -a1

sed -i 's|boot/grub/|boot/grub2/|' adjust-grub-theme/main.go

# add targets to print the binaries and libraries, so we can build/install them
# in Fedora style
cat <<EOF >> Makefile
print_binaries:
	@echo \${BINARIES}

print_libraries:
	@echo \${LIBRARIES}
EOF

%build
export GOPATH=$(pwd)/.godeps:$(pwd)/gopath

go generate
go build

%install
%make_install PREFIX=%{_prefix}

%if %{with check}
%check
%gochecks
%endif

%pre
%sysusers_create_compat archlinux/%{name}.sysusers

%post
%systemd_post deepin-shutdown-sound.service

%preun
%systemd_preun deepin-shutdown-sound.service

%postun
%systemd_postun_with_restart deepin-shutdown-sound.service

%files
%doc README.md
%license LICENSE
%{_bindir}/dde-open
%{_libexecdir}/%{name}/
%{_prefix}/lib/%{name}/
%{_unitdir}/*.service
%{_datadir}/dbus-1/services/*.service
%{_datadir}/dbus-1/system-services/*.service
%{_datadir}/dbus-1/system.d/*.conf
%{_datadir}/icons/hicolor/*/actions/*
%{_datadir}/dde-api
%{_datadir}/polkit-1/actions/com.deepin.api.locale-helper.policy
%{_datadir}/polkit-1/actions/com.deepin.api.device.unblock-bluetooth-devices.policy
%{_var}/lib/polkit-1/localauthority/10-vendor.d/com.deepin.api.device.pkla
%{_sysusersdir}/%{name}.conf

%files -n golang-%{name}-devel -f devel.file-list

%changelog
%autochangelog
