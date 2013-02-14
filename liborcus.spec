Summary:	Standalone file import filter library for spreadsheet documents
Name:		liborcus
Version:	0.3.0
Release:	1
License:	MIT
Group:		Libraries
URL:		http://gitorious.org/orcus
Source0:	http://kohei.us/files/orcus/src/%{name}_%{version}.tar.bz2
# Source0-md5:	8755aac23317494a9028569374dc87b2
BuildRequires:	boost-devel
BuildRequires:	mdds-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
%{name} is a standalone file import filter library for spreadsheet
documents. Currently under development are ODS, XLSX and CSV import
filters.

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n %{name}_%{version}

%build
# TODO spreadsheet-model requires ixion
%configure \
	--disable-debug \
	--disable-static \
	--disable-werror \
	--with-pic \
	--disable-spreadsheet-model \
	--without-libzip
%{__make}


%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS
%attr(755,root,root) %{_bindir}/orcus-xml-dump
%attr(755,root,root) %{_libdir}/%{name}-0.4.so.*.*.*
%attr(755,root,root) %ghost   %{_libdir}/%{name}-0.4.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}-0.4.so
%{_includedir}/%{name}-0.4
%{_pkgconfigdir}/%{name}-0.4.pc
