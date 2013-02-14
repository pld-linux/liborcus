# TODO: ixion (requires newer version than existing in PLD)
#
# Conditional build:
%bcond_with	ixion		# ixion-based spreadsheet model support
%bcond_without	libzip		# ZIP-based formats support via libzip
%bcond_without	static_libs	# static library
#
Summary:	Standalone file import filter library for spreadsheet documents
Summary(pl.UTF-8):	Biblioteka samodzielnego filtra importującego pliki dla arkuszy kalkulacyjnych
Name:		liborcus
Version:	0.3.0
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://kohei.us/files/orcus/src/%{name}_%{version}.tar.bz2
# Source0-md5:	8755aac23317494a9028569374dc87b2
URL:		http://gitorious.org/orcus
BuildRequires:	boost-devel
%{?with_ixion:BuildRequires:	ixion-devel >= 0.6}
BuildRequires:	libstdc++-devel
%{?with_libzip:BuildRequires:	libzip-devel}
BuildRequires:	mdds-devel
BuildRequires:	pkgconfig >= 1:0.20
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
liborcus is a standalone file import filter library for spreadsheet
documents. Currently under development are ODS, XLSX and CSV import
filters.

%description -l pl.UTF-8
liborcus to biblioteka samodzielnego filtra importującego pliki dla
arkuszy kalkulacyjnych. Obecnie rozwijane są filtry importujące
dokumenty ODS, XLSX i CSV.

%package devel
Summary:	Header files for liborcus
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki liborcus
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	boost-devel
Requires:	libstdc++-devel

%description devel
This package contains the header files for developing applications
that use liborcus.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
wykorzystujących bibliotekę liborcus.

%package static
Summary:	Static liborcus library
Summary(pl.UTF-8):	Statyczna biblioteka liborcus
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static liborcus library.

%description static -l pl.UTF-8
Statyczna biblioteka liborcus.

%prep
%setup -q -n %{name}_%{version}

%build
%configure \
	--disable-debug \
	--disable-silent-rules \
	%{!?with_ixion:--disable-spreadsheet-model} \
	%{!?with_static_libs:--disable-static} \
	--disable-werror \
	--with-pic \
	%{!?with_libzip:--without-libzip}
%{__make}


%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/liborcus-*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS
%attr(755,root,root) %{_bindir}/orcus-xml-dump
%attr(755,root,root) %{_libdir}/liborcus-0.4.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liborcus-0.4.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liborcus-0.4.so
%{_includedir}/liborcus-0.4
%{_pkgconfigdir}/liborcus-0.4.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%endif
%{_libdir}/liborcus-0.4.a
