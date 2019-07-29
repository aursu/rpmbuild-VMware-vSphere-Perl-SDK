%global debug_package %{nil}

Summary: Perl scripting interface to the vSphere API
Name: VMware-vSphere-Perl-SDK
Version: 6.7.0-8156551
Release: 1%{?dist}
Group: System Environment/Libraries
License: VMware, Inc.
Source: VMware-vSphere-Perl-SDK-6.7.0-8156551.x86_64.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)

Patch1: VMware-vSphere-Perl-SDK-5.5.0-1384587-destdir.patch
Patch2: VMware-vSphere-Perl-SDK-5.5.0-1384587-noeula.patch
Patch3: VMware-vSphere-Perl-SDK-5.5.0-1384587-nomodules.patch
Patch4: VMware-vSphere-Perl-SDK-5.5.0-1384587-nosoft.patch
# https://communities.vmware.com/message/2298661
Patch5: VMware-vSphere-Perl-SDK-5.5.0-1384587-sslslowness.patch

Requires:		perl > 5.8, /usr/bin/perldoc
Requires:		e2fsprogs > 1.38
Requires:		libxml2 > 2.6.26, openssl > 0.9.8, openssl-devel
Requires:		perl-Archive-Zip >= 1.28, perl-IO-Compress >= 2.037, perl-Compress-Raw-Zlib >= 2.037
Requires:		perl-ExtUtils-MakeMaker >= 1.54, perl-Crypt-SSLeay >= 0.55, perl-version
Requires:		perl-Class-MethodMaker >= 2.10, perl-HTML-Parser >= 3.60, perl-UUID
Requires:		perl-Data-Dump >= 1.15, perl-SOAP-Lite >= 0.710.08, perl-URI >= 1.37
Requires:		perl-XML-SAX >= 0.16, perl-XML-NamespaceSupport >= 1.09, perl-XML-LibXML-Common >= 0.13
Requires:		perl-XML-LibXML >= 1.63, perl-libwww-perl >= 5.805, perl-LWP-Protocol-https >= 5.805
Requires:		glibc(x86-32), compat-expat1(x86-32), libgcc(x86-32), libstdc++(x86-32), ncurses-libs(x86-32), zlib(x86-32), libxml2(x86-32)

BuildRequires:		openssl-devel
BuildRequires:		perl-devel
#BuildRequires:		redhat-rpm-config

# we do not provide included libpython and py modules
%filter_provides_in %{_usr}/lib/vmware-vcli/bin/esxcli/.*\.so\..*$
%filter_provides_in %{_usr}/lib/vmware-vcli/bin/esxcli/.*\.so$
# we do not provide included ssl, crypto, expat and stdc++ libs
%filter_provides_in %{_usr}/lib/vmware-vcli/lib32/.*\.so\..*
%filter_provides_in %{_usr}/lib/vmware-vcli/VMware
# All requires already listed above
%filter_requires_in %{_usr}/lib/vmware-vcli
%filter_from_requires /perl(VMware/d; /perl(WSMan/d
%{?perl_default_filter}

%description
The vSphere SDK for Perl provides an easy-to-use Perl scripting interface to the
vSphere API. Administrators and developers can work with vSphere API objects using
vSphere SDK for Perl subroutines

%prep
%setup -q -n vmware-vsphere-cli-distrib
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
# Disable for 6.7
# %patch5 -p0

%build
exit 0

%install
rm -rf $RPM_BUILD_ROOT
DESTDIR=$RPM_BUILD_ROOT ./vmware-install.pl --default

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_sysconfdir}/vmware-vcli
%{_usr}/lib/vmware-vcli
# duplicate perl-VMware stuff
%exclude %{_usr}/lib/vmware-vcli/VMware
%{_bindir}/vihostupdate
%{_bindir}/vihostupdate35
%{_bindir}/vifs
%{_bindir}/vmware-cmd
%{_bindir}/resxtop
%{_bindir}/svmotion
%{_bindir}/vmkfstools
%{_bindir}/viperl-support
# no need uninstll script for RPM package
%exclude %{_bindir}/vmware-uninstall-vSphere-CLI.pl
%{_bindir}/vicfg-*
%{_bindir}/esxcfg-*
%{_bindir}/esxcli
%{perl_privlib}/WSMan
%{perl_privlib}/VMware
%{_docdir}/vmware-vcli
%{_mandir}/man1/resxtop.1*

%changelog
* Mon Jun 22 2015 Alexander Ursu <aursu@hostopia.com> 5.5.0-1384587.el6.1
- apply patch to fix SSL slowness

* Wed Jun 17 2015 Alexander Ursu <aursu@hostopia.com> 5.5.0-1384587
- initial build

