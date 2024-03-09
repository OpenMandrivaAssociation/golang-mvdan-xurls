%global debug_package %{nil}

%bcond_with bootstrap2

# Run tests in check section
%bcond_with check

# https://github.com/mvdan/xurls
%global goipath		mvdan.cc/xurls
%global goaltipaths	mvdan.cc/xurls/v2
%global forgeurl	https://github.com/mvdan/xurls
Version:		2.5.0

%gometa

Summary:	Extract urls from text
Name:		golang-github-mvdan-xurls

Release:	1
Source0:	https://github.com/mvdan/xurls/archive/v%{version}/xurls-%{version}.tar.gz
%if %{with bootstrap2}
# Generated from Source100
Source3:	vendor.tar.zst
Source100:	golang-package-dependencies.sh
%endif
URL:		https://github.com/mvdan/xurls
License:	BSD
Group:		Development/Other
BuildRequires:	compiler(go-compiler)
%if ! %{with bootstrap2}
BuildRequires:	golang(golang.org/x/mod/module)
BuildRequires:	golang(golang.org/x/sync/semaphore)
BuildRequires:	golang-ipath(mvdan.cc/xurls)
%endif
%if %{with check}
BuildRequires:	golang(github.com/rogpeppe/go-internal/testscript)
%endif

%description
A Go library to Extract urls from text using regular expressions.

%files
%license LICENSE
%doc README.md
%{_bindir}/xurls

#-----------------------------------------------------------------------

%package devel
Summary:	%{summary}
Group:		Development/Other
BuildArch:	noarch

%description devel
%{description}

This package contains library source intended for
building other packages which use import path with
%{goipath} prefix.

%files devel -f devel.file-list
%license LICENSE
%doc README.md

#-----------------------------------------------------------------------

%prep
%autosetup -p1 -n xurls-%{version}

rm -rf vendor

%if %{with bootstrap2}
tar xf %{S:3}
%endif

%build
%gobuildroot
for cmd in $(ls -1 cmd) ; do
	%gobuild -o _bin/$cmd %{goipath}/cmd/$cmd
done

%install
%goinstall
for cmd in $(ls -1 _bin) ; do
	install -Dpm 0755 _bin/$cmd %{buildroot}%{_bindir}/$cmd
done

# install alternative name
ln -fs . %{buildroot}%{_datadir}/gocode/src/%{goaltipaths}
echo \"%{_datadir}/gocode/src/%{goaltipaths}\" >> devel.file-list

%check
%if %{with check}
%gochecks
%endif

