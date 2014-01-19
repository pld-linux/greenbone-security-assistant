
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs

Summary:	Greenbone Security Assistant
Name:		greenbone-security-assistant
Version:	4.0.2
Release:	0.1
License:	GPL v2+
Group:		Applications
Source0:	http://wald.intevation.org/frs/download.php/1422/%{name}-%{version}.tar.gz
# Source0-md5:	d0c81070cb58cad1b7b41e51d69d3288
URL:		http://www.openvas.org/
BuildRequires:	cmake
BuildRequires:	glib2-devel >= 2.16
BuildRequires:	gnutls-devel > 2.8
BuildRequires:	libmicrohttpd-devel >= 0.4.2
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-devel
BuildRequires:	libxslt-progs
BuildRequires:	openvas-libraries-devel >= 6.0.0
BuildRequires:	pkgconfig
%if %{with apidocs}
BuildRequires:	doxygen
#BuildRequires:	xmltoman
%endif
BuildConflicts:	openvas-libraries-devel >= 7.0
Requires:	openvas-common >= 6.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Greenbone Security Assistant is a web application that connects to
the OpenVAS Manager and OpenVAS Administrator to provide for a
full-featured user interface for vulnerability management.

The Open Vulnerability Assessment System (OpenVAS) is a framework of
several services and tools offering a comprehensive and powerful
vulnerability scanning and vulnerability management solution.

%package apidocs
Summary:	GSA API documentation
Group:		Documentation

%description apidocs
Greenbone Security Assistant API documentation.

%prep
%setup -q

%build
install -d build
cd build
%cmake \
	-DSYSCONFDIR=%{_sysconfdir} \
	-DLOCALSTATEDIR=/var \
	..
%{__make}

%if %{with apidocs}
%{__make} doc
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES ChangeLog README
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/openvas/gsad_log.conf
%doc doc/*.html
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man8/*.8*
%{_datadir}/openvas/gsa
