%global debug_package %{nil}

Summary: Perl scripting interface to the vSphere API
Name: VMware-vSphere-Perl-SDK
Version: 7.0.0
Release: 16453907%{?dist}.1
Group: System Environment/Libraries
License: VMware, Inc.
Source: VMware-vSphere-Perl-SDK-7.0.0-16453907.x86_64.tar.gz
# https://kb.vmware.com/s/article/78473
Source1: esxcli-7.0.0-15866526-lin64.sh
Source2: resxtop-7.0.0-15992393-lin64.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)

Patch1: VMware-vSphere-Perl-SDK-6.7.0-8156551-destdir.patch
Patch2: VMware-vSphere-Perl-SDK-6.7.0-8156551-noeula.patch
Patch3: VMware-vSphere-Perl-SDK-5.5.0-1384587-nomodules.patch
Patch4: VMware-vSphere-Perl-SDK-5.5.0-1384587-nosoft.patch
# https://communities.vmware.com/message/2298661
Patch5: VMware-vSphere-Perl-SDK-5.5.0-1384587-sslslowness.patch
Patch6: VMware-vSphere-Perl-SDK-7.0.0-16453907-destdir.patch
Patch7: VMware-vSphere-Perl-SDK-7.0.0-16453907-noeula.patch
Patch8: VMware-vSphere-Perl-SDK-7.0.0-16453907-nomodules.patch

# Requires: perl-Crypt-SSLeay >= 0.72
# Requires: perl-ExtUtils-MakeMaker = 6.96
# Requires: perl-IO-Socket-INET6 >= 2.72
# Requires: perl-LWP-Protocol-https = 6.07
# Requires: perl-libwww-perl = 6.26
# Requires: perl-Module-Build = 0.42.05
# Requires: perl(Net::FTP) = 2.77
# Requires: perl-Net-HTTP >= 6.09
# Requires: perl-Net-INET6Glue >= 0.603
# Requires: perl-Socket6 >= 0.28
# Requires: perl-Text-Template >= 1.47
# Requires: perl-Time-Piece >= 1.31
# Requires: perl-Try-Tiny >= 0.28
# Requires: perl-XML-NamespaceSupport >= 1.12

Requires: perl-Archive-Zip >= 1.28
Requires: perl-Crypt-SSLeay >= 0.64
Requires: perl-Data-Dumper >= 2.121
Requires: perl-ExtUtils-Install > 1.54
Requires: perl-ExtUtils-MakeMaker >= 6.68
Requires: perl-HTML-Parser >= 3.60
Requires: perl-IO-Socket-INET6 >= 2.69
Requires: perl-LWP-Protocol-https >= 6.04
Requires: perl-libwww-perl >= 6.05
Requires: perl-Module-Build >= 0.40.05
Requires: perl(Net::FTP)
Requires: perl-Net-HTTP >= 6.06
# perl(Net::FTP) is a part of perl-5.16.3 distribution on CentOS 7
Requires: perl-Net-INET6Glue >= 0.5
Requires: perl-Path-Class >= 0.33
Requires: perl-Socket6 >= 0.23
Requires: perl-Text-Template >= 1.45
Requires: perl-Time-Piece >= 1.20.1
Requires: perl-Try-Tiny >= 0.12
Requires: perl-UUID >= 0.27
Requires: perl-version >= 0.78
Requires: perl-XML-SAX >= 0.99
Requires: perl-XML-NamespaceSupport >= 1.11
Requires: perl-XML-LibXML >= 2.0129


# https://code.vmware.com/docs/6530/vsphere-sdk-for-perl-installation-guide#/doc/GUID-8B0E6E94-A215-4904-935D-1B164C3941A8.html
Requires: e2fsprogs > 1.38
Requires: libxml2 > 2.6.26
Requires: ncurses-libs
Requires: openssl > 0.9.8
Requires: perl >= 5.8.8
Requires: glibc(x86-32)
Requires: zlib(x86-32)
# Requires: compat-expat1(x86-32)
# Requires: libgcc(x86-32)
# Requires: libstdc++(x86-32)
# Requires: libxml2(x86-32)
# Requires: ncurses-libs(x86-32)

BuildRequires: e2fsprogs-devel
BuildRequires: libuuid-devel
BuildRequires: openssl-devel
BuildRequires: perl-devel
BuildRequires: perl-Pod-Perldoc
BuildRequires: redhat-rpm-config

# we do not provide included libpython and py modules
%filter_provides_in %{_usr}/lib/vmware-vcli/bin/esxcli/.*\.so\..*$
%filter_provides_in %{_usr}/lib/vmware-vcli/bin/esxcli/.*\.so$
# we do not provide included ssl, crypto, expat and stdc++ libs
%filter_provides_in %{_usr}/lib/vmware-vcli/lib32/.*\.so\..*
%filter_provides_in %{_usr}/lib/vmware-vcli/VMware

# All requires already listed above
%filter_requires_in %{_usr}/lib/vmware-vcli
%filter_from_requires /perl\(VMware/d; /perl\(WSMan/d
%{?perl_default_filter}

%global __provides_exclude_from %{_usr}/lib/vmware-vcli/bin/(esxcli|vmware-dcli)/.*\\.so(\\..*)?|%{_usr}/lib/vmware-vcli/lib32/.*\\.so(\\..*)?|%{_usr}/lib/vmware-vcli/VMware|%{_docdir}/vmware-vcli|/opt/vmware|%{_usr}/lib/vmware/resxtop
%global __requires_exclude_from %{_usr}/lib/vmware-vcli|%{_docdir}/vmware-vcli|%{_usr}/lib/vmware/resxtop|/opt/vmware|%{_bindir}/resxtop|%{_bindir}/esxcli
%global __requires_exclude ^perl\\((VMware|WSMan)

%description
The vSphere SDK for Perl provides an easy-to-use Perl scripting interface to the
vSphere API. Administrators and developers can work with vSphere API objects using
vSphere SDK for Perl subroutines

%prep
%setup -q -n vmware-vsphere-cli-distrib
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch4 -p1
# Disable for 6.7
# %patch5 -p0

mkdir -p esxcli
pushd esxcli
sed -n '/^__ARCHIVE_BELOW__/,$ {//!p}' < %{SOURCE1} | tar zx
popd

mkdir -p resxtop
pushd resxtop
tar zxf %{SOURCE2}
popd

%build
exit 0

%install
rm -rf $RPM_BUILD_ROOT
DESTDIR=$RPM_BUILD_ROOT ./vmware-install.pl --default

pushd esxcli
mkdir -p $RPM_BUILD_ROOT/opt/vmware
tar zxf *.tgz -C $RPM_BUILD_ROOT/opt/vmware
ln -s /opt/vmware/esxcli/esxcli $RPM_BUILD_ROOT%{_bindir}/esxcli
popd

pushd resxtop
install -D -m 755 resxtop $RPM_BUILD_ROOT%{_bindir}/resxtop
mkdir -p $RPM_BUILD_ROOT%{_usr}/lib/vmware/resxtop
cp -rp lib64/* $RPM_BUILD_ROOT%{_usr}/lib/vmware/resxtop
cp -rp doc/esxtop* $RPM_BUILD_ROOT%{_mandir}/man1/
popd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_sysconfdir}/vmware-vcli
%{_usr}/lib/vmware/resxtop
%{_usr}/lib/vmware-vcli
# duplicate perl-VMware stuff
%exclude %{_usr}/lib/vmware-vcli/VMware
%{_bindir}/esxcli
%{_bindir}/resxtop
%{_bindir}/vihostupdate
%{_bindir}/vihostupdate35
%{_bindir}/vifs
%{_bindir}/vmware-cmd
%{_bindir}/svmotion
%{_bindir}/vmkfstools
%{_bindir}/viperl-support
# no need uninstll script for RPM package
%exclude %{_bindir}/vmware-uninstall-vSphere-CLI.pl*
%exclude %{_bindir}/*.bat
%exclude %{_bindir}/*.pyc
%{perl_privlib}/WSMan
%{perl_privlib}/VMware
%{_docdir}/vmware-vcli
/opt/vmware
%{_mandir}/man1/esxtop*

%changelog
* Mon Aug 10 2020 Alexander Ursu <alexander.ursu@gmail.com> 7.0.0-16453907.el7.1
- upgrade to 7.0.0

* Mon Jul 29 2019 Alexander Ursu <alexander.ursu@gmail.com> 6.7.0-8156551.el7.1
- upgrade to 6.7.0

* Mon Jun 22 2015 Alexander Ursu <aursu@hostopia.com> 5.5.0-1384587.el6.1
- apply patch to fix SSL slowness

* Wed Jun 17 2015 Alexander Ursu <aursu@hostopia.com> 5.5.0-1384587
- initial build

