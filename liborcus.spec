#
# Conditional build:
%bcond_without	ixion		# ixion-based spreadsheet model support
%bcond_without	libzip		# ZIP-based formats support via libzip
%bcond_without	static_libs	# static library
#
Summary:	Standalone file import filter library for spreadsheet documents
Summary(pl.UTF-8):	Biblioteka samodzielnego filtra importującego pliki dla arkuszy kalkulacyjnych
Name:		liborcus
Version:	0.7.0
Release:	4
License:	MIT
Group:		Libraries
#Source0Download: http://gitorious.org/orcus/pages/Download
Source0:	http://kohei.us/files/orcus/src/%{name}-%{version}.tar.bz2
# Source0-md5:	7681383be6ce489d84c1c74f4e7f9643
URL:		http://gitorious.org/orcus
BuildRequires:	autoconf >= 2.65
BuildRequires:	automake >= 1:1.11
BuildRequires:	boost-devel >= 1.36
%{?with_ixion:BuildRequires:	ixion-devel >= 0.7}
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
%{?with_libzip:BuildRequires:	libzip-devel}
BuildRequires:	mdds-devel >= 0.8.0
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
Requires:	boost-devel >= 1.36
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

%package spreadsheet
Summary:	liborcus spreadsheet model library
Summary(pl.UTF-8):	Biblioteka liborcus spreadsheet model
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ixion >= 0.7

%description spreadsheet
liborcus spreadsheet model library.

%description spreadsheet -l pl.UTF-8
Biblioteka liborcus spreadsheet model (modelu arkuszy kalkulacyjnych).

%package spreadsheet-devel
Summary:	Development files for liborcus spreadsheet model library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki liborcus spreadsheet model
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-spreadsheet = %{version}-%{release}
Requires:	ixion-devel >= 0.7

%description spreadsheet-devel
Development files for liborcus spreadsheet model library.

%description spreadsheet-devel -l pl.UTF-8
Pliki programistyczne biblioteki liborcus spreadsheet model.

%package spreadsheet-static
Summary:	Static liborcus spreadsheet model library
Summary(pl.UTF-8):	Biblioteka statyczna liborcus spreadsheet model
Group:		Development/Libraries
Requires:	%{name}-spreadsheet-devel = %{version}-%{release}

%description spreadsheet-static
Static liborcus spreadsheet model library.

%description spreadsheet-static -l pl.UTF-8
Biblioteka statyczna liborcus spreadsheet model.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
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

%post	spreadsheet -p /sbin/ldconfig
%postun	spreadsheet -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS
%attr(755,root,root) %{_bindir}/orcus-detect
%attr(755,root,root) %{_bindir}/orcus-mso-encryption
%attr(755,root,root) %{_bindir}/orcus-xml-dump
%attr(755,root,root) %{_bindir}/orcus-zip-dump
%attr(755,root,root) %{_libdir}/liborcus-0.8.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liborcus-0.8.so.0
%attr(755,root,root) %{_libdir}/liborcus-mso-0.8.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liborcus-mso-0.8.so.0
%attr(755,root,root) %{_libdir}/liborcus-parser-0.8.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liborcus-parser-0.8.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liborcus-0.8.so
%attr(755,root,root) %{_libdir}/liborcus-mso-0.8.so
%attr(755,root,root) %{_libdir}/liborcus-parser-0.8.so
%{_includedir}/liborcus-0.8
%{_pkgconfigdir}/liborcus-0.8.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/liborcus-0.8.a
%{_libdir}/liborcus-mso-0.8.a
%{_libdir}/liborcus-parser-0.8.a
%endif

%if %{with ixion}
%files spreadsheet
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/orcus-csv
%attr(755,root,root) %{_bindir}/orcus-gnumeric
%attr(755,root,root) %{_bindir}/orcus-ods
%attr(755,root,root) %{_bindir}/orcus-xls-xml
%attr(755,root,root) %{_bindir}/orcus-xlsx
%attr(755,root,root) %{_bindir}/orcus-xml
%attr(755,root,root) %{_libdir}/liborcus-spreadsheet-model-0.8.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liborcus-spreadsheet-model-0.8.so.0

%files spreadsheet-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liborcus-spreadsheet-model-0.8.so
%{_pkgconfigdir}/liborcus-spreadsheet-model-0.8.pc

%files spreadsheet-static
%defattr(644,root,root,755)
%{_libdir}/liborcus-spreadsheet-model-0.8.a
%endif
