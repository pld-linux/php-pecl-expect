%bcond_without	tests

%define		php_name	php%{?php_suffix}
%define		modname	expect
%define		status		beta
Summary:	%{modname} - PHP extension for expect library
Summary(pl.UTF-8):	%{modname} - rozszerzenie PHP dla biblioteki expect
Name:		%{php_name}-pecl-%{modname}
Version:	0.4.0
Release:	1
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	https://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	f4cfd4ff3a1ff5ee29ff833a9e5df1cb
Patch0:		master.patch
Patch1:		build.patch
URL:		https://pecl.php.net/package/expect/
BuildRequires:	%{php_name}-devel >= 3:5.0.4
BuildRequires:	expect-devel
BuildRequires:	rpmbuild(macros) >= 1.650
%if %{with tests}
BuildRequires:	%{php_name}-cli
BuildRequires:	%{php_name}-pcre
%endif
%{?requires_php_extension}
Provides:	php(%{modname}) = %{version}
Obsoletes:	php-pecl-expect < 0.3.1-5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This extension allows to interact with processes through PTY, using
expect library.

In PECL status of this extension is: %{status}.

%description -l pl.UTF-8
To rozszerzenie pozwala na interakcję z procesami poprzez PTY przy
użyciu biblioteki expect.

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -qc
mv %{modname}-%{version}/* .
%patch -P0 -p1
%patch -P1 -p1

%build
phpize
%configure \
	--with-tcldir=%{_prefix}/lib
%{__make}

%if %{with tests}
export NO_INTERACTION=1
%{__make} test \
	PHP_EXECUTABLE=%{_bindir}/%{php_name}
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

install -p modules/%{modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
