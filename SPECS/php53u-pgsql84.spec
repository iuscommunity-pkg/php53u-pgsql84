
%global php_base php53u
%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%global php_ver 5.3.24
%global php_basever 5.3


Summary:        A PostgreSQL 8.4 database module for PHP        
Name:           %{php_base}-pgsql84
Version:        %{php_ver} 
Release:        2.ius%{?dist}
Group:          Development/Languages
License:        PHP 
URL:            http://php.net
Source0:        http://www.php.net/distributions/php-%{php_ver}.tar.gz       
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  krb5-devel, openssl-devel, postgresql84-devel
BuildRequires:  %{php_base} >= %{php_ver}, %{php_base}-devel
Requires:       %{php_base}-api = %{php_apiver}, %{php_base}-common, %{php_base}-pdo 

Conflicts:      %{php_base}-pgsql
Conflicts:      php-pgsql < %{php_basever}
Conflicts:      php-pdo-pgsql < %{php_basever}
Provides:       php-pgsql = %{version}-%{release}
Provides:       php-pdo-pgsql = %{version}-%{release}
Provides:       %{php_base}-pdo-pgsql = %{version}-%{release}
Provides:       php_database, php-pdo_pgsql 

%description 
The php-pgsql package includes a dynamic shared object (DSO) that can
be compiled in to the Apache Web server to add PostgreSQL database
support to PHP. PostgreSQL is an object-relational database management
system that supports almost all SQL constructs. PHP is an
HTML-embedded scripting language. If you need back-end support for
PostgreSQL, you should install this package in addition to the main
php package.


%prep
%setup -q -n php-%{php_ver}
cp -a ext/pgsql/README README.pgsql
cp -a ext/pgsql/CREDITS CREDITS.pgsql
cp -a ext/pdo_pgsql/CREDITS CREDITS.pdo_pgsql

%build
pushd ext/pgsql
phpize
%configure  --prefix=%{_prefix} \
            --disable-rpath \
            --with-pgsql=shared 

make %{?_smp_mflags}
popd

pushd ext/pdo_pgsql
phpize
%configure  --prefix=%{_prefix} \
            --disable-rpath \
            --enable-pdo=shared \
            --with-pdo-pgsql=shared,%{_prefix}

make %{?_smp_mflags}
popd


%install
rm -rf $RPM_BUILD_ROOT
%{__mkdir} -p   %{buildroot}%{_sysconfdir}/php.d \
                %{buildroot}%{_libdir}/php/modules
%{__install} ext/pgsql/modules/pgsql.so %{buildroot}%{_libdir}/php/modules/pgsql.so
%{__install} ext/pdo_pgsql/modules/pdo_pgsql.so %{buildroot}%{_libdir}/php/modules/pdo_pgsql.so

# the configs
cat >%{buildroot}%{_sysconfdir}/php.d/pgsql.ini <<EOF
; PostGreSQL 8.4 Module Configuration
extension=pgsql.so
EOF

cat >%{buildroot}%{_sysconfdir}/php.d/pdo_pgsql.ini <<EOF
; PostGreSQL 8.4 PDO Module Configuration
extension=pdo_pgsql.so
EOF


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc LICENSE README.pgsql CREDITS.pgsql CREDITS.pdo_pgsql
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/pgsql.ini
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/pdo_pgsql.ini
%{_libdir}/php/modules/pgsql.so
%{_libdir}/php/modules/pdo_pgsql.so

%changelog
* Fri Apr 12 2013 Ben Harper <ben.harper@rackspace.com> - 5.3.24-1.ius
- Rebuilding for 5.3.24

* Fri Mar 15 2013 Ben Harper <ben.harper@rackspace.com> - 5.3.23-1.ius
- Rebuilding for 5.3.23

* Wed Mar 06 2013 Jeffrey Ness <jeffrey.ness@rackspace.com> - 5.3.22-2.ius
- Rebuilding against 5.3.22-3

* Fri Feb 22 2013 Ben Harper <ben.harper@rackspace.com> - 5.3.22-1.ius
- Rebuilding for 5.3.22

* Thu Jan 17 2013 Ben Harper <ben.harper@rackspace.com> - 5.3.21-1.ius
- Rebuilding for 5.3.21

* Thu Dec 20 2012 Ben Harper <ben.harper@rackspace.com> - 5.3.20.-1.ius
- Rebuilding for 5.3.20

* Mon Nov 26 2012 Ben Harper <ben.harper@rackspace.com> - 5.3.19-1.ius
- Rebuilding for 5.3.19

* Tue Oct 30 2012 Ben Harper <ben.harper@rackspace.com> - 5.3.18-1.ius
- Rebuilding for 5.3.18

* Fri Aug 19 2011 Jeffrey Ness <jeffrey.ness@rackspace.com> - 5.3.5-2.ius
- Rebuilding

* Wed Feb 02 2011 BJ Dierkes <wdierkes@rackspace.com> - 5.3.5-1.ius
- Rebuild for php 5.3.5
- BuildRequires php53u >= %%{php_ver}

* Fri Dec 17 2010 BJ Dierkes <wdierkes@rackspace.com> - 5.3.4-1.ius
- Renamed as php53u-pgsql84.  Resolves LP#691755
- Rebuild against php53u-5.3.4

* Mon Jul 26 2010 BJ Dierkes <wdierkes@rackspace.com> - 5.3.3-1.ius
- Latest php source from upstream.

* Tue Jun 15 2010 BJ Dierkes <wdierkes@rackspace.com> - 5.3.2-1.ius
- Initial spec build

