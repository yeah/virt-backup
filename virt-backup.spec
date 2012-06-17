
Summary: backup script for libvirt managed VM
Name: virt-backup
Version: 0.1.0
Release: 1
Source0: %{name}-%{version}.tar.gz
BuildArch: noarch

License: GPL
Group: Virtualization
BuildRoot: %{_tmppath}/%{name}-buildroot
Prefix: %{_prefix}
Requires: lvm2
Requires: util-linux
Requires: lzop, bzip2, pbzip2, gzip, xz
Requires: perl(Sys::Virt) => 0.2.3
Requires: perl(XML::Simple)
Requires: fuse-chunkfs

Requires(pre): shadow-utils
Requires(preun): initscripts, chkconfig
Requires(postun): initscripts
Requires(post): initscripts, chkconfig

AutoReq: no

%description
This package contains utilities for virtualization stack
on RHEL & ci. It provides for example SELinux policy, hook
scripts to set permissions on ressources files
etc...

%prep
%setup -q

%build

%install

%{__rm} -rf $RPM_BUILD_ROOT

# Install backup script
%{__mkdir_p} $RPM_BUILD_ROOT%{_bindir}/
%{__install} -m 0755 virt-backup $RPM_BUILD_ROOT%{_bindir}/

# Create backup dir
%{__mkdir_p} $RPM_BUILD_ROOT%{_localstatedir}/lib/libvirt/backup

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre
getent group kvm >/dev/null || groupadd -g 36 -r kvm
getent group qemu >/dev/null || groupadd -g 107 -r qemu
getent passwd qemu >/dev/null || \
  useradd -r -u 107 -g qemu -G kvm -d / -s /sbin/nologin \
    -c "qemu user" qemu

%preun

%post

%files
%defattr(-,root,root,-)
%doc README
%{_bindir}/*
%dir %attr(0770, qemu, kvm) %{_localstatedir}/lib/libvirt/backup

%changelog
* Sun Jun 17 2012 Daniel B. <daniel@firewall-services.com> - 0.1.0-1
- Move virt-backup to it's own RPM (and GIT repo)

