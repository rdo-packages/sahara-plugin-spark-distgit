# Globals Declaration


%global pname sahara-plugin-spark
%global module sahara_plugin_spark

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc 1
# guard for packages OSP does not ship
%global rhosp 0

%global common_desc \
The Spark plugin for Sahara allows Sahara to provision and \
manage Spark clusters on OpenStack.

Name:          python-sahara-plugin-spark
Version:       XXX
Release:       XXX
Summary:       Apache Hadoop cluster management on OpenStack
License:       ASL 2.0
URL:           https://launchpad.net/sahara
Source0:       https://tarballs.openstack.org/%{pname}/%{pname}-%{upstream_version}.tar.gz
BuildArch:     noarch

BuildRequires:    git
BuildRequires:    python3-devel
BuildRequires:    python3-setuptools
BuildRequires:    python3-pbr >= 2.0.0
BuildRequires:    openstack-macros

# test requirements
BuildRequires:    python3-stestr >= 1.0.0
BuildRequires:    python3-testscenarios
BuildRequires:    python3-oslotest
BuildRequires:    python3-hacking
BuildRequires:    python3-oslo-i18n >= 3.15.3
BuildRequires:    python3-oslo-log >= 3.36.0
BuildRequires:    python3-oslo-serialization >= 2.18.0
BuildRequires:    python3-oslo-utils >= 3.33.0
BuildRequires:    python3-sahara >= 10.0.0


%description
%{common_desc}


%package -n python3-%{pname}
Summary:          Spark plugin for Sahara
%{?python_provide:%python_provide python3-%{pname}}

Requires:         python3-babel >= 2.3.4
Requires:         python3-eventlet >= 0.18.2
Requires:         python3-oslo-i18n >= 3.15.3
Requires:         python3-oslo-log >= 3.36.0
Requires:         python3-oslo-serialization >= 2.18.0
Requires:         python3-oslo-utils >= 3.33.0
Requires:         python3-pbr >= 2.0.0
Requires:         python3-requests >= 2.14.2
Requires:         python3-sahara >= 10.0.0
Requires:         python3-six >= 1.10.0

# Extend the Sahara api and engine packages
Supplements:      openstack-sahara-api
Supplements:      openstack-sahara-engine
Supplements:      openstack-sahara-image-pack

%description -n python3-%{pname}
%{common_desc}


%package -n python3-%{pname}-tests-unit
Summary:        Tests of the Spark plugin for Sahara
%{?python_provide:%python_provide python3-%{pname}-tests-unit}
Requires:       python3-%{pname} = %{version}-%{release}

%description -n python3-%{pname}-tests-unit
%{common_desc}

This package contains the test files of the Spark plugin for Sahara.


%if 0%{?with_doc}

%package -n python-%{pname}-doc
Group:         Documentation
Summary:       Usage documentation for the Spark plugin for Sahara
Requires:      python3-%{pname} = %{version}-%{release}
BuildRequires:    python3-reno
BuildRequires:    python3-sphinx >= 1.6.2
BuildRequires:    python3-openstackdocstheme >= 1.18.1

BuildRequires:    python3-sphinxcontrib-httpdomain

%description -n python-%{pname}-doc
%{common_desc}

This documentation provides details about the Spark plugin for Sahara.

%endif


%prep
%autosetup -n %{pname}-%{upstream_version} -S git

# let RPM handle deps
%py_req_cleanup

# set executable on these files to suppress rpmlint warnings, they are used as
# templates to create shell scripts.
chmod a+x sahara_plugin_spark/plugins/spark/resources/spark-env.sh.template
chmod a+x sahara_plugin_spark/plugins/spark/resources/tmp-cleanup.sh.template
# also set executable on this topology script, should have been set upstream
chmod a+x sahara_plugin_spark/plugins/spark/resources/topology.sh


%build
%{py3_build}


%if 0%{?with_doc}
export PYTHONPATH=.
sphinx-build -W -b html doc/source doc/build/html
rm -rf doc/build/html/.{doctrees,buildinfo}
sphinx-build -W -b man doc/source doc/build/man
%endif


%install
%{py3_install}


%if 0%{?with_doc}
mkdir -p %{buildroot}%{_mandir}/man1
install -p -D -m 644 doc/build/man/*.1 %{buildroot}%{_mandir}/man1/
%endif


# TODO: re-enable when the split version of sahara.git is packaged
#%check
#export PATH=$PATH:%{buildroot}/usr/bin
#export PYTHONPATH=$PWD
#stestr run


%files -n python3-%{pname}
%doc README.rst
%license LICENSE
%{python3_sitelib}/%{module}
%{python3_sitelib}/%{module}-%{upstream_version}-py?.?.egg-info
%exclude %{python3_sitelib}/%{module}/tests

%files -n python3-%{pname}-tests-unit
%license LICENSE
%{python3_sitelib}/%{module}/tests

%if 0%{?with_doc}
%files -n python-%{pname}-doc
%license LICENSE
%doc doc/build/html
%{_mandir}/man1/%{pname}.1.gz
%endif


%changelog
# REMOVEME: error caused by commit http://git.openstack.org/cgit/openstack/sahara-plugin-spark/commit/?id=7628c535082f39ec75768af4bc13c2b8fe34c098
