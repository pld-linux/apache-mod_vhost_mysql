#
# TODO:
# Summary clean +pl, description,other number at httpd.conf ?

%define		mod_name	vhost_mysql
%define 	apxs		/usr/sbin/apxs
Summary:	Apache vhost in mysql
Name:		apache-mod_%{mod_name}
Version:	0.10
Release:	0.8
License:	GPL
Group:		Networking/Daemons
Source0:	http://fabienne.tc2.utelisys.net/~skinkie/mod_%{mod_name}2/mod_%{mod_name}2-%{version}.tar.gz
# Source0-md5:	c47c8dc4ac41e9ed2c91a239c876d272
Source1:	95_vhost_mysql.conf
BuildRequires:	%{apxs}
BuildRequires:	apache-devel
BuildRequires:	db-devel >= 4.2.52
BuildRequires:	mysql-devel
Requires(post,preun):	%{apxs}
Requires:	apache
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)

%description

%prep
%setup -q -n mod_%{mod_name}2-%{version}

%build
%{__make} APXS=apxs

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/httpd.conf}

install .libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

CFG="$RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf"
install %{SOURCE1} ${CFG}/

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{apxs} -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc README vh.sql
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/httpd.conf/95_vhost_mysql.conf
%attr(755,root,root) %{_pkglibdir}/*
