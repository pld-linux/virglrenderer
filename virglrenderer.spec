#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	VirGL virtual OpenGL renderer library
Summary(pl.UTF-8):	VirGL - biblioteka wirtualnego renderera OpenGL
Name:		virglrenderer
Version:	0.5.0
Release:	1
License:	MIT
Group:		Libraries
Source0:	https://www.freedesktop.org/software/virgl/%{name}-%{version}.tar.bz2
# Source0-md5:	29804ecd1713e298828f9d1642eb289d
Patch0:		%{name}-link.patch
URL:		https://virgil3d.github.io/
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake
BuildRequires:	check-devel >= 0.9.4
BuildRequires:	libdrm-devel >= 2.4.50
BuildRequires:	libepoxy-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	pkgconfig
BuildRequires:	python >= 2
Requires:	libdrm >= 2.4.50
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
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I build-aux
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libvirglrenderer.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING
%attr(755,root,root) %{_bindir}/virgl_test_server
%attr(755,root,root) %{_libdir}/libvirglrenderer.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libvirglrenderer.so.0

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
