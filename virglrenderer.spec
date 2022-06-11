# TODO: optional percetto>=0.0.8 or vperfetto_min for tracing
#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	VirGL virtual OpenGL renderer library
Summary(pl.UTF-8):	VirGL - biblioteka wirtualnego renderera OpenGL
Name:		virglrenderer
Version:	0.9.1
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://gitlab.freedesktop.org/virgl/virglrenderer/-/tags
Source0:	https://gitlab.freedesktop.org/virgl/virglrenderer/-/archive/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	0918da613ff02a8c1c34041d81144e5f
URL:		https://virgil3d.github.io/
BuildRequires:	Mesa-libgbm-devel
BuildRequires:	check-devel >= 0.9.4
BuildRequires:	libdrm-devel >= 2.4.50
BuildRequires:	libepoxy-devel >= 1.5.4
BuildRequires:	meson >= 0.46
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	python >= 2
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	sed >= 4.0
BuildRequires:	xorg-lib-libX11-devel
Requires:	libdrm >= 2.4.50
Requires:	libepoxy >= 1.5.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
VirGL virtual OpenGL renderer library.

%description -l pl.UTF-8
VirGL - biblioteka wirtualnego renderera OpenGL.

%package devel
Summary:	Header file for virglrenderer library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki virglrenderer
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header file for virglrenderer library.

%description devel -l pl.UTF-8
Plik nagłówkowy biblioteki virglrenderer.

%package static
Summary:	Static virglrenderer library
Summary(pl.UTF-8):	Statyczna biblioteka virglrenderer
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static virglrenderer library.

%description static -l pl.UTF-8
Statyczna biblioteka virglrenderer.

%prep
%setup -q

%if %{with static_libs}
%{__sed} -i -e '/^libvirglrenderer = / s/shared_library/library/' src/meson.build
%endif

%build
%meson build \
	%{!?with_static_libs:--default-library=shared}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING
%attr(755,root,root) %{_bindir}/virgl_test_server
%attr(755,root,root) %{_libdir}/libvirglrenderer.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libvirglrenderer.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvirglrenderer.so
%{_includedir}/virgl
%{_pkgconfigdir}/virglrenderer.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libvirglrenderer.a
%endif
