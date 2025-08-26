# TODO: optional percetto>=0.0.8 or vperfetto_min or sysprof>=3.38.0 for tracing
# optional minijail support in venus renderer? (Android specific?)
#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_with	drm_amdgpu	# AMDGPU DRM native-context renderer (experimental)
%bcond_without	drm_msm		# MSM DRM native-context renderer
%bcond_without	va		# video accelleration via libva
%bcond_without	vulkan		# venus renderer
#
%ifnarch aarch64
%undefine	with_drm_msm
%endif
%if %{with drm_amdgpu}
%define		libdrm_ver	2.4.50
%else
# actually it's libdrm_amdgpu library dependency, but it isnt'a a separate package in PLD
%define		libdrm_ver	2.4.121
%endif
Summary:	VirGL virtual OpenGL renderer library
Summary(pl.UTF-8):	VirGL - biblioteka wirtualnego renderera OpenGL
Name:		virglrenderer
Version:	1.1.1
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://gitlab.freedesktop.org/virgl/virglrenderer/-/tags
Source0:	https://gitlab.freedesktop.org/virgl/virglrenderer/-/archive/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	2c7588e8ced5053224f9bb5330f9bad6
Patch0:		%{name}-types.patch
URL:		https://virgil3d.github.io/
BuildRequires:	Mesa-libgbm-devel
%{?with_vulkan:BuildRequires:	Vulkan-Loader-devel}
BuildRequires:	check-devel >= 0.9.4
BuildRequires:	gcc >= 6:4.1
BuildRequires:	libdrm-devel >= %{libdrm_ver}
BuildRequires:	libepoxy-devel >= 1.5.4
%if %{with va}
BuildRequires:	libva-devel
BuildRequires:	libva-drm-devel
%endif
BuildRequires:	meson >= 0.55
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	python3
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	sed >= 4.0
BuildRequires:	xorg-lib-libX11-devel
Requires:	libdrm >= %{libdrm_ver}
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
Requires:	Mesa-libgbm-devel
%if %{with vulkan}
Requires:	Vulkan-Loader-devel
%endif
Requires:	libdrm-devel >= %{libdrm_ver}
Requires:	libepoxy-devel >= 1.5.4
%if %{with va}
Requires:	libva-devel
Requires:	libva-drm-devel
%endif
Requires:	xorg-lib-libX11-devel

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
%patch -P0 -p1

%build
drm_renderers="%{?with_drm_amdgpu:amdgpu-experimental} %{?with_drm_msm:msm}"
%meson \
	%{!?with_static_libs:--default-library=shared} \
	-Ddrm-renderers="$(echo $drm_renderers | tr ' ' ',')" \
	%{?with_vulkan:-Dvenus=true} \
	%{?with_va:-Dvideo=true}

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING
%attr(755,root,root) %{_bindir}/virgl_test_server
%attr(755,root,root) %{_libdir}/libvirglrenderer.so.*.*.*
%ghost %{_libdir}/libvirglrenderer.so.1
%if %{with vulkan}
%attr(755,root,root) %{_libexecdir}/virgl_render_server
%endif

%files devel
%defattr(644,root,root,755)
%{_libdir}/libvirglrenderer.so
%{_includedir}/virgl
%{_pkgconfigdir}/virglrenderer.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libvirglrenderer.a
%endif
