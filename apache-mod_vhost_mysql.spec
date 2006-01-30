%define		mod_name	vhost_mysql
%define 	apxs		/usr/sbin/apxs
Summary:	Apache vhost in MySQL
Summary(pl):	Wirtualne hosty dla Apache'a w bazie MySQL
Name:		apache-mod_%{mod_name}
Version:	0.10
Release:	4
License:	GPL
Group:		Networking/Daemons
Source0:	http://fabienne.tc2.utelisys.net/~skinkie/mod_vhost_mysql2/mod_%{mod_name}2-%{version}.tar.gz
# Source0-md5:	c47c8dc4ac41e9ed2c91a239c876d272
Source1:	apache_vhost_mysql.conf
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0
BuildRequires:	db-devel >= 4.2.52
BuildRequires:	mysql-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
This module provides dynamically configured virtual hosting using
MySQL in Apache2.

%description -l pl
Ten modu� umo�liwia dynamicznie konfigurowanie host�w wirtualnych w
Apache'u 2 przy u�yciu bazy MySQL.

%prep
%setup -q -n mod_%{mod_name}2-%{version}
rm -rf .libs *.{la,lo,o,slo}

%build
%{__make} \
	APXS=%{apxs}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/httpd.conf}

install .libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/21_vhost_mysql.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%preun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc README vh.sql
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*_vhost_mysql.conf
%attr(755,root,root) %{_pkglibdir}/*.so
