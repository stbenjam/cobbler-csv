Name:		cobbler-csv
Version:	1.1
Release:    2
Summary:	Tool for importing cobbler system profiles from a CSV

BuildArch:  noarch

Group:	    Applications/System	
License:	MIT
URL:		https://github.com/stbenjam/cobbler-csv
Source0:	cobbler-csv.tar.gz

Requires:	python

%description
Tool for importing cobbler system profiles from an ENC

%prep
%setup -n src

%build
%{__python} setup.py build

%install
test "x$RPM_BUILD_ROOT" != "x" && rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --optimize=1 --root=$RPM_BUILD_ROOT $PREFIX
mkdir -p ${RPM_BUILD_ROOT}/usr/bin
mkdir -p ${RPM_BUILD_ROOT}/etc
install -m 0755 cobbler-import-enc ${RPM_BUILD_ROOT}/usr/bin
install -m 0600 etc/cobbler-csv.conf ${RPM_BUILD_ROOT}/etc

%files
%defattr(-,root,root,-)
%{python_sitelib}/cobbler_csv
/usr/bin/cobbler-import-enc
%config(noreplace) /etc/cobbler-csv.conf
%if 0%{?fedora} >= 9 || 0%{?rhel} > 5
%{python_sitelib}/cobbler*.egg-info
%endif

%changelog
* Fri Mar 22 2013 Stephen Benjamin <skbenja@gmail.com>
- Initial creation
