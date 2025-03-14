#
# Conditional build:
%bcond_without	ixion		# ixion-based spreadsheet model support
%bcond_without	python		# Python 3 binding
%bcond_without	apidocs		# Sphinx documentation
%bcond_without	static_libs	# static library
#
Summary:	Standalone file import filter library for spreadsheet documents
Summary(pl.UTF-8):	Biblioteka samodzielnego filtra importującego pliki dla arkuszy kalkulacyjnych
Name:		liborcus
# keep in sync with BuildRequires in libreoffice.spec
Version:	0.19.2
Release:	4
License:	MPL v2.0
Group:		Libraries
#Source0Download: https://gitlab.com/orcus/orcus/-/releases
Source0:	https://kohei.us/files/orcus/src/%{name}-%{version}.tar.xz
# Source0-md5:	7360797e8fe50f793ddfa578a6ca3a76
Patch0:		%{name}-flags.patch
URL:		https://gitlab.com/orcus/orcus
BuildRequires:	autoconf >= 2.65
BuildRequires:	automake >= 1:1.11
BuildRequires:	boost-devel >= 1.36
%if %{with ixion}
BuildRequires:	ixion-devel >= 0.19.0
BuildRequires:	ixion-devel < 0.20
%endif
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	libtool >= 2:1.5
BuildRequires:	mdds-devel >= 2.1.1
BuildRequires:	mdds-devel < 2.2
BuildRequires:	pkgconfig >= 1:0.20
%{?with_python:BuildRequires:	python3-devel >= 1:3.2}
BuildRequires:	rpm-build >= 4.6
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
%if %{with apidocs}
BuildRequires:	doxygen
BuildRequires:	python3-breathe
BuildRequires:	python3-sphinx_argparse
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-3
%endif
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
Requires:	libstdc++-devel >= 6:7

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
Requires:	ixion >= 0.18.0

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
Requires:	ixion-devel >= 0.18.0

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

%package apidocs
Summary:	API documentation for orcus libraries
Summary(pl.UTF-8):	Dokumentacja API bibliotek orcus
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for orcus libraries.

%description apidocs -l pl.UTF-8
Dokumentacja API bibliotek orcus.

%package -n python3-orcus
Summary:	Python 3 binding for liborcus library
Summary(pl.UTF-8):	Wiązanie Pythona 3 do biblioteki liborcus
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python3-libs >= 1:3.2

%description -n python3-orcus
Python 3 binding for liborcus library.

%description -n python3-orcus -l pl.UTF-8
Wiązanie Pythona 3 do biblioteki liborcus.

%prep
%setup -q
%patch -P 0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	am_cv_python_pyexecdir=%{py3_sitedir} \
	am_cv_python_pythondir=%{py3_sitescriptdir} \
	--disable-debug \
	%{!?with_python:--disable-python} \
	--disable-silent-rules \
	%{!?with_ixion:--disable-spreadsheet-model} \
	%{?with_static_libs:--enable-static} \
	--disable-werror \
	--with-pic

%{__make}

%if %{with apidocs}
cd doc
doxygen doxygen.conf
sphinx-build-3 -b html . _build
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/liborcus-*.la

%if %{with python}
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/*.la
%if %{with static_libs}
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/*.a
%endif
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	spreadsheet -p /sbin/ldconfig
%postun	spreadsheet -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CHANGELOG ChangeLog LICENSE README.md
%attr(755,root,root) %{_bindir}/orcus-css-dump
%attr(755,root,root) %{_bindir}/orcus-detect
%if %{without ixion}
# when building with ixion, orcus-json supports map mode which uses spreadsheet-model library, so it's packaged in -spreadsheet then
%attr(755,root,root) %{_bindir}/orcus-json
%endif
%attr(755,root,root) %{_bindir}/orcus-mso-encryption
%attr(755,root,root) %{_bindir}/orcus-yaml
%attr(755,root,root) %{_bindir}/orcus-zip-dump
%attr(755,root,root) %{_libdir}/liborcus-0.18.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liborcus-0.18.so.0
%attr(755,root,root) %{_libdir}/liborcus-mso-0.18.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liborcus-mso-0.18.so.0
%attr(755,root,root) %{_libdir}/liborcus-parser-0.18.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liborcus-parser-0.18.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liborcus-0.18.so
%attr(755,root,root) %{_libdir}/liborcus-mso-0.18.so
%attr(755,root,root) %{_libdir}/liborcus-parser-0.18.so
%{_includedir}/liborcus-0.18
%{_pkgconfigdir}/liborcus-0.18.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/liborcus-0.18.a
%{_libdir}/liborcus-mso-0.18.a
%{_libdir}/liborcus-parser-0.18.a
%endif

%if %{with ixion}
%files spreadsheet
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/orcus-csv
%attr(755,root,root) %{_bindir}/orcus-gnumeric
%attr(755,root,root) %{_bindir}/orcus-json
%attr(755,root,root) %{_bindir}/orcus-styles-ods
%attr(755,root,root) %{_bindir}/orcus-ods
%attr(755,root,root) %{_bindir}/orcus-xls-xml
%attr(755,root,root) %{_bindir}/orcus-xlsx
%attr(755,root,root) %{_bindir}/orcus-xml
%attr(755,root,root) %{_libdir}/liborcus-spreadsheet-model-0.18.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liborcus-spreadsheet-model-0.18.so.0

%files spreadsheet-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liborcus-spreadsheet-model-0.18.so
%{_pkgconfigdir}/liborcus-spreadsheet-model-0.18.pc

%if %{with static_libs}
%files spreadsheet-static
%defattr(644,root,root,755)
%{_libdir}/liborcus-spreadsheet-model-0.18.a
%endif
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/_build/{_static,cpp,overview,python,*.html,*.js}
%endif

%if %{with python}
%files -n python3-orcus
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/_orcus.so
%attr(755,root,root) %{py3_sitedir}/_orcus_json.so
%{py3_sitescriptdir}/orcus
%endif
