#
# Conditional build:
%bcond_without	tests	# unit tests

Summary:	Easy Swagger UI for your Flask API
Summary(pl.UTF-8):	Łatwe w użyciu UI Swagger dla API Flaska
Name:		python3-flasgger
Version:	0.9.7.1
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/flasgger/
Source0:	https://files.pythonhosted.org/packages/source/f/flasgger/flasgger-%{version}.tar.gz
# Source0-md5:	3f2d4b14b25b22a0e99008c6ad826ba4
Patch0:		flasgger-marshmallow.patch
URL:		https://pypi.org/project/flasgger/
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-apispec
BuildRequires:	python3-apispec-webframeworks
BuildRequires:	python3-PyYAML >= 3.0
BuildRequires:	python3-flask >= 0.10
BuildRequires:	python3-flask-restful
BuildRequires:	python3-flex
BuildRequires:	python3-jsonschema >= 3.0.1
BuildRequires:	python3-mistune
BuildRequires:	python3-pytest
BuildRequires:	python3-six >= 1.10.0
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
Requires:	python3-modules >= 1:3.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Flasgger is a Flask extension to extract OpenAPI-Specification from
all Flask views registered in your API.

Flasgger also comes with SwaggerUI <http://swagger.io/swagger-ui/>
embedded so you can access <http://localhost:5000/apidocs> and
visualize and interact with your API resources.

%description -l pl.UTF-8
Flasgger to rozszerzenie Flaska do wydobywania specyfikacji OpenAPI ze
wszystkich widoków Flaska zarejestrowanych w danym API.

Flasgger ma także wbudowany interfejs użytkownika SwaggerUI
<http://swagger.io/swagger-ui/>, dzięki czemu odwołując się do
<http://localhost:5000/apidocs> można wizualizować i wykonywać
interakcje z zasobami swojego API.

%prep
%setup -q -n flasgger-%{version}
%patch -P0 -p1

%build
%py3_build

%if %{with tests}
# test_example.py requires readable resolv.conf to collect
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd):$(pwd)/etc/flasgger_package \
%{__python3} -m pytest tests --ignore tests/test_example.py
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-flasgger-%{version}
cp -pr demo_app examples $RPM_BUILD_ROOT%{_examplesdir}/python3-flasgger-%{version}
%{__sed} -i -e '1s,/usr/bin/python$,%{__python3},' \
	$RPM_BUILD_ROOT%{_examplesdir}/python3-flasgger-%{version}/demo_app/app.py

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%{py3_sitescriptdir}/flasgger
%{py3_sitescriptdir}/flasgger-%{version}-py*.egg-info
%{_examplesdir}/python3-flasgger-%{version}
