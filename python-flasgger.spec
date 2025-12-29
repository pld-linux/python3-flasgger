#
# Conditional build:
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module (built from python3-flasgger.spec)

Summary:	Easy Swagger UI for your Flask API
Summary(pl.UTF-8):	Łatwe w użyciu UI Swagger dla API Flaska
Name:		python-flasgger
# keep 0.9.5 here for python2 support
Version:	0.9.5
Release:	0.1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/flasgger/
Source0:	https://files.pythonhosted.org/packages/source/f/flasgger/flasgger-%{version}.tar.gz
# Source0-md5:	0b249888d2aa6732e8214a721f92b735
URL:		https://pypi.org/project/flasgger/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-PyYAML >= 3.0
BuildRequires:	python-apispec
BuildRequires:	python-apispec-webframeworks
BuildRequires:	python-flask >= 0.10
BuildRequires:	python-flask-restful
BuildRequires:	python-flask_jwt
BuildRequires:	python-flex
BuildRequires:	python-jsonschema >= 3.0.1
BuildRequires:	python-mistune
BuildRequires:	python-pytest
BuildRequires:	python-six >= 1.10.0
%endif
%endif
%if %{with python3}
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
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
Requires:	python-modules >= 1:2.7
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

%package -n python3-flasgger
Summary:	Easy Swagger UI for your Flask API
Summary(pl.UTF-8):	Łatwe w użyciu UI Swagger dla API Flaska
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.6

%description -n python3-flasgger
Flasgger is a Flask extension to extract OpenAPI-Specification from
all Flask views registered in your API.

Flasgger also comes with SwaggerUI <http://swagger.io/swagger-ui/>
embedded** so you can access <http://localhost:5000/apidocs> and
visualize and interact with your API resources.

%description -n python3-flasgger -l pl.UTF-8
Flasgger to rozszerzenie Flaska do wydobywania specyfikacji OpenAPI ze
wszystkich widoków Flaska zarejestrowanych w danym API.

Flasgger ma także wbudowany interfejs użytkownika SwaggerUI
<http://swagger.io/swagger-ui/>, dzięki czemu odwołując się do
<http://localhost:5000/apidocs> można wizualizować i wykonywać
interakcje z zasobami swojego API.

%prep
%setup -q -n flasgger-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS= \
PYTHONPATH=$(pwd):$(pwd)/etc/flasgger_package \
%{__python} -m pytest tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS= \
PYTHONPATH=$(pwd):$(pwd)/etc/flasgger_package \
%{__python3} -m pytest tests
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%if %{with python2}
install -d $RPM_BUILD_ROOT%{_examplesdir}/python-flasgger-%{version}
cp -pr demo_app examples $RPM_BUILD_ROOT%{_examplesdir}/python-flasgger-%{version}
%{__sed} -i -e '1s,/usr/bin/python$,%{__python},' \
	$RPM_BUILD_ROOT%{_examplesdir}/python-flasgger-%{version}/demo_app/app.py
%endif
%if %{with python3}
install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-flasgger-%{version}
cp -pr demo_app examples $RPM_BUILD_ROOT%{_examplesdir}/python3-flasgger-%{version}
%{__sed} -i -e '1s,/usr/bin/python$,%{__python3},' \
	$RPM_BUILD_ROOT%{_examplesdir}/python3-flasgger-%{version}/demo_app/app.py
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%{py_sitescriptdir}/flasgger
%{py_sitescriptdir}/flasgger-%{version}-py*.egg-info
%{_examplesdir}/python-flasgger-%{version}
%endif

%if %{with python3}
%files -n python3-flasgger
%defattr(644,root,root,755)
%doc LICENSE README.md
%{py3_sitescriptdir}/flasgger
%{py3_sitescriptdir}/flasgger-%{version}-py*.egg-info
%{_examplesdir}/python3-flasgger-%{version}
%endif
