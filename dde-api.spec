%undefine _debugsource_packages
%global goipath github.com/linuxdeepin/dde-api

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
BuildRequires:	git-core
BuildRequires:	golang
BuildRequires:	go-compilers-golang-compiler
#BuildRequires:  deepin-gettext-tools
BuildRequires:  deepin-gir-generator
BuildRequires:	deepin-gettext-tools
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
%autosetup -p1

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
%__make prepare
# upstream Makefile expects binaries generated to out/bin
for cmd in $(make print_binaries); do
    %gobuild -o out/bin/$cmd %{goipath}/$cmd
done
# don't build binaries or libraries based on Makefile
%make_build ts-to-policy

%install
# install dev libraries mannally
gofiles=$(find $(make print_libraries) %{?gofindfilter} -print)
%goinstall $gofiles
# install binaries based on Makefile
%__make DESTDIR=%{buildroot} SYSTEMD_SERVICE_DIR="%{_unitdir}" GOBUILD_DIR=_build install-binary
install -p -D -m 0644 archlinux/deepin-api.sysusers %{buildroot}%{_sysusersdir}/%{name}.conf

%if %{with check}
%check
%gochecks
%endif

%files
%doc README.md
%license LICENSE
%{_bindir}/dde-open
%{_unitdir}/*.service
%{_datadir}/dbus-1/services/*.service
%{_datadir}/dbus-1/system-services/*.service
%{_datadir}/dbus-1/system.d/*.conf
%{_datadir}/icons/hicolor/*/actions/*
%{_datadir}/dde-api
%{_sysusersdir}/%{name}.conf
%{_prefix}/lib/deepin-api
%{_datadir}/polkit-1/actions/org.deepin.dde.device.unblock-bluetooth-devices.policy
%{_datadir}/polkit-1/actions/org.deepin.dde.locale-helper.policy
%{_localstatedir}/lib/polkit-1/localauthority/10-vendor.d/org.deepin.dde.device.pkla

%files -n golang-%{name}-devel -f devel.file-list
