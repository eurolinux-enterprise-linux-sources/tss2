#
# Spec file for IBM's TSS for the TPM 2.0
#
%{!?__global_ldflags: %global __global_ldflags -Wl,-z,relro}

Name:		tss2
Version:	713
Release:	10%{?dist}
Summary:	IBM's TCG Software Stack (TSS) for TPM 2.0 and related utilities

Group:		Applications/System	
License:	BSD
URL:		http://sourceforge.net/projects/ibmtpm20tss/
Source0:	https://sourceforge.net/projects/ibmtpm20tss/files/NotForUsers_FedoraSourceRpm/ibmtss%{version}withman.tar
# submitted upstream https://sourceforge.net/p/ibmtpm20tss/mailman/message/35768541/
Patch0000: tssmarshal-pointer-deref.patch
# submitted upstream https://sourceforge.net/p/ibmtpm20tss/mailman/message/35768637/
Patch0001: array-index-check.patch
# RHEL only. Upstream commit fce4d3d8 is more extensive
# replacing all mallocs with wrapper. Pick up next rebase
Patch0002: malloc-check.patch
# RHEL only. Upstream commit 4abb70ed contains change along with many others
Patch0003: tss-name-getname-fix-default-case.patch
# RHEL only. Upstream commit 4abb70ed contains change along with many others
Patch0004: unmarshal-return-fix.patch
# submitted upstream https://sourceforge.net/p/ibmtpm20tss/mailman/message/35769161/
Patch0005: ticket-file-name-check.patch
# submitted upstream https://sourceforge.net/p/ibmtpm20tss/mailman/message/35769195/
Patch0006: fix-context-file-name-check.patch

# tss2 does not work on Big Endian arch yet
ExcludeArch:	ppc64 s390x
BuildRequires:	openssl-devel
Requires:	openssl

%description
TSS2 is a user space Trusted Computing Group's Software Stack (TSS) for
TPM 2.0.  It implements the functionality equivalent to the TCG TSS
working group's ESAPI, SAPI, and TCTI layers (and perhaps more) but with
a hopefully far simpler interface.

It comes with about 80 "TPM tools" that can be used for rapid prototyping,
education and debugging. 

%package devel
Summary:	Development libraries and headers for IBM's TSS 2.0
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Development libraries and headers for IBM's TSS 2.0. You will need this in
order to build TSS 2.0 applications.

%prep
%setup -q -c %{name}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
# nonstandard variable names are used in place of CFLAGS and LDFLAGS
pushd utils
CCFLAGS="%{optflags}" \
LNFLAGS="%{__global_ldflags}" \
make -f makefile.fedora %{?_smp_mflags} 
popd

%install
# Prefix for namespacing
BIN_PREFIX=tss
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_libdir}
mkdir -p %{buildroot}/%{_includedir}/%{name}/
mkdir -p %{buildroot}/%{_mandir}/man1
pushd utils
# Pick out executables and copy with namespacing
for f in *; do
	if [[ -x $f && -f $f && ! $f =~ .*\..* ]]; then
		cp -p $f %{buildroot}/%{_bindir}/${BIN_PREFIX}$f
	fi;
done
cp -p *.so.0.1 %{buildroot}/%{_libdir}
cp -p %{name}/*.h %{buildroot}/%{_includedir}/%{name}/
cp -p man/man1/tss*.1 %{buildroot}/%{_mandir}/man1/
popd


# Make symbolic links to the shared lib
pushd %{buildroot}/%{_libdir}
rm -f libtss.so.0
ln -sf libtss.so.0.1 libtss.so.0
rm -f libtss.so
ln -sf libtss.so.0 libtss.so
popd

%post -p /sbin/ldconfig 
%postun -p /sbin/ldconfig

%files
%license LICENSE
%{_bindir}/tss*
%{_libdir}/libtss.so.0
%{_libdir}/libtss.so.0.*
%attr(0644, root, root) %{_mandir}/man1/tss*.1*

%files devel
%{_includedir}/%{name}
%{_libdir}/libtss.so
%doc ibmtss.doc

%changelog
* Tue Apr 04 2017 Jerry Snitselaar <jsnitsel@redhat.com> - 713-10
- Fix missing pointer deref
- Fix array index check
- Clean up malloc checks
- Fix default switch case in TSS_Name_GetName
- Fix return in TPMS_NV_CERTIFY_INFO_Unmarshal
- Check for null ticket file name in policyticket
- Fix null check of context file name in contextload

* Fri Mar 10 2017 Jerry Snitselaar <jsnitsel@redhat.com> - 713-9
- Update release version
resolves: rhbz#1384452 - New package request: Include IBM's Trusted Computing Group Software Stack (TSS) 2.0 (tss2) 

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 713-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Oct 05 2016 Hon Ching(Vicky) Lo <lo1@us.ibm.com> - 713-7
- Removed defattr from the devel subpackage 

* Mon Sep 26 2016 Hon Ching(Vicky) Lo <lo1@us.ibm.com> - 713-6
- Added s390x arch as another "ExcludeArch"

* Mon Sep 26 2016 Hon Ching(Vicky) Lo <lo1@us.ibm.com> - 713-5
- Replaced ExclusiveArch with ExcludeArch 
 
* Mon Sep 19 2016 Hon Ching(Vicky) Lo <lo1@us.ibm.com> - 713-4
- Used ExclusiveArch instead of BuildArch tag
- Removed attr from symlink in devel subpackage 
- Added manpages and modified the Source0
- Added CCFLAGS and LNFLAGS to enforce hardening and optimization

* Wed Aug 17 2016 Hon Ching(Vicky) Lo <lo1@us.ibm.com> - 713-3
- Modified supported arch to ppc64le

* Sat Aug 13 2016 Hon Ching(Vicky) Lo <lo1@us.ibm.com> - 713-2
- Minor spec fixes 

* Tue Aug 09 2016 Hon Ching(Vicky) Lo <lo1@us.ibm.com> - 713-1
- Updated for initial submission 

* Fri Mar 20 2015 George Wilson <gcwilson@us.ibm.com>
- Initial implementation
