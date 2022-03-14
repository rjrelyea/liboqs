Name:       {{{ git_dir_name }}}
Version:    {{{ git_dir_version }}}
Release:    1%{?dist}
Summary:    liboqs is an open source C library for quantum-safe cryptographic algorithms.

%global oqs_version 0.7.2-dev
License:    MIT
URL:        https://github.com/open-quantum-safe/liboqs.git
VCS:        {{{ git_dir_vcs }}}

Source:     {{{ git_dir_pack }}}
BuildRequires: ninja-build
BuildRequires: cmake
#BuildRequires: python-pytest
#BuildRequires: python-pytest-xdist
#BuildRequires: python-yaml
BuildRequires: doxygen
#BuildRequires: astyle
BuildRequires: graphviz

%description
liboqs provides:
 - a collection of open source implementations of quantum-safe key encapsulation mechanism (KEM) and digital signature algorithms; the full list can be found below
 - a common API for these algorithms
 - a test harness and benchmarking routines
liboqs is part of the Open Quantum Safe (OQS) project led by Douglas Stebila and Michele Mosca, which aims to develop and integrate into applications quantum-safe cryptography to facilitate deployment and testing in real world contexts. In particular, OQS provides prototype integrations of liboqs into TLS and SSH, through OpenSSL and OpenSSH.

%package devel
Summary:          Development libraries for liboqs
Requires:         liboqs%{?_isa} = %{version}-%{release}

%description devel
Header and Library files for doing development with liboqs.

%prep
{{{ git_dir_setup_macro }}}

%build
mkdir build 
pushd build
#
# add others as necessary...
#
# CMAKE_INSTALL_BINDIR
# CMAKE_INSTALL_DATADIR
# CMAKE_INSTALL_DATAROOTDIR
# CMAKE_INSTALL_DOCDIR
# CMAKE_INSTALL_INCLUDEDIR
# CMAKE_INSTALL_INFODIR
# CMAKE_INSTALL_LIBDIR
# CMAKE_INSTALL_LIBEXECDIR
# CMAKE_INSTALL_LOCALEDIR
# CMAKE_INSTALL_LOCALSTATEDIR
# CMAKE_INSTALL_MANDIR
# CMAKE_INSTALL_OLDINCLUDEDIR
# CMAKE_INSTALL_RUNSTATEDIR
# CMAKE_INSTALL_SBINDIR
# CMAKE_INSTALL_SHAREDSTATEDIR
# CMAKE_INSTALL_SYSCONFDIR
#
cmake -GNinja -DBUILD_SHARED_LIBS=ON -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX=$RPM_BUILD_ROOT -DOQS_USE_OPENSSL=OFF -DCMAKE_INSTALL_LIBDIR=$RPM_BUILD_ROOT/%{_libdir} -DCMAKE_INSTALL_INCLUDEDIR=$RPM_BUILD_ROOT/%{_includedir} ..
OQS_VERSION=$(grep OQS_VERSION_TEXT include/oqs/oqsconfig.h)
OQS_VERSION=${OQS_VERSION##\#*OQS_VERSION_TEXT \"}
OQS_VERSION=${OQS_VERSION%\"}
echo $OQS_VERSION
if [ "%{oqs_version}" != "${OQS_VERSION}" ]; then
   echo "Spec oqs version %{oqs_version} != Library version ${OQS_VERSION}"
   echo "Need to update the liboqs.spec"
   exit 1;
fi
ninja
ninja gen_docs
popd

%install
pushd build
echo $OQS_VERSION
#DEST=$RPM_BUILD_ROOT ninja install 
ninja install 
for i in liboqsTargets.cmake liboqsTargets-debug.cmake
do
  cp $RPM_BUILD_ROOT/%{_libdir}/cmake/liboqs/$i /tmp/$i
  sed -e "s;$RPM_BUILD_ROOT;;g" /tmp/$i   > $RPM_BUILD_ROOT/%{_libdir}/cmake/liboqs/$i
  rm /tmp/$i
done
#mkdir -p $RPM_BUILD_ROOT/%{_datadir}/doc/oqs
#install -d doc $RPM_BUILD_ROOT/%{_datadir}/doc/oqs
popd

%files
%{_libdir}/liboqs.so.%{oqs_version}

%files devel
%{_libdir}/liboqs.so.0
%{_libdir}/liboqs.so
%dir %{_libdir}/cmake/liboqs
%{_libdir}/cmake/liboqs/liboqsTargets.cmake
%{_libdir}/cmake/liboqs/liboqsTargets-debug.cmake
%{_libdir}/cmake/liboqs/liboqsConfig.cmake
%{_libdir}/cmake/liboqs/liboqsConfigVersion.cmake

%dir %{_includedir}/oqs
%{_includedir}/oqs/*
#%dir %%{_datadir}/doc/oqs
#%doc %%{_datadir}/doc/oqs/html/*
#%doc %%{_datadir}/doc/oqs/xml/*

%changelog
{{{ git_dir_changelog }}}

