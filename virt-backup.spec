
Summary: backup script for libvirt managed VM
Name: virt-backup
Version: 0.2.9
Release: 1
Source0: %{name}-%{version}.tar.gz
BuildArch: noarch

License: GPL
Group: Virtualization
BuildRoot: %{_tmppath}/%{name}-buildroot
Prefix: %{_prefix}
Requires: lvm2
Requires: util-linux
Requires: lzop, bzip2, gzip, xz
Requires: perl(Sys::Virt) => 0.2.3
Requires: perl(XML::Simple)
Requires: fuse-chunkfs

AutoReq: no

%description
This package provides a helper script to backup
libvirt managed virtual machines with minimal downtime

%prep
%setup -q

%build

%install

%{__rm} -rf $RPM_BUILD_ROOT

%if %{?fedora}%{?rhel} <= 5
sed -i -e "s|/sbin/lvcreate|/usr/sbin/lvcreate|g" -e "s|/sbin/lvremove|/usr/sbin/lvremove|g" \
       -e "s|/sbin/lvs|/usr/sbin/lvs|g" virt-backup
%endif

# Install backup script
%{__mkdir_p} $RPM_BUILD_ROOT%{_bindir}/
%{__install} -m 0755 virt-backup $RPM_BUILD_ROOT%{_bindir}/

# Create backup dir
%{__mkdir_p} $RPM_BUILD_ROOT%{_localstatedir}/lib/libvirt/backup

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%pre

%preun

%post

%files
%defattr(-,root,root,-)
%doc README CHANGELOG.git
%{_bindir}/*
%dir %attr(0770, qemu, qemu) %{_localstatedir}/lib/libvirt/backup

%changelog
* Tue Feb 10 2015 Daniel B. <daniel@firewall-services.com> - 0.2.9-1
- Fix when using a relative path for backupdir
- Fix image based disk support when they are stored on the / filesystem

* Thu Nov 6 2014 Daniel B. <daniel@firewall-services.com> - 0.2.8-1
- Support thin volumes
- Possibility to specify an alternate lock directory

* Tue Oct 21 2014 Daniel B. <daniel@firewall-services.com> - 0.2.7-1
- Do not explicitly require pbzip2

* Mon Jun 23 2014 Daniel B. <daniel@firewall-services.com> - 0.2.6-1
- Add a --no-offline option
- Revert 10 tries max to take snapshot
- Cleanup snapshot and temp files for image based disks

* Wed Jun 4 2014 Daniel B. <daniel@firewall-services.com> - 0.2.5-1
- Fix breaking the loop while taking snapshots

* Tue Jun 3 2014 Daniel B. <daniel@firewall-services.com> - 0.2.4-1
- Try up to 30 times to take a snapshot before giving up

* Fri May 2 2014 Daniel B. <daniel@firewall-services.com> - 0.2.3-1
- Better handle snapshot failure when there's no lock

* Tue Apr 22 2014 Daniel B. <daniel@firewall-services.com> - 0.2.2-1
- Lock LVM before snapshot

* Thu Jan 30 2014 Daniel B. <daniel@firewall-services.com> - 0.2.1-1
- Gracefuly handle snapshot failure for file based disks
- Improve comments

* Fri Aug 9 2013 Daniel B. <daniel@firewall-services.com> - 0.2.0-1
- Support snapshot for file based images (if FS is backed by LVM)
- Support a dual nodes cluster situation
- Add a convert action, which uses qemu-img to convert into qcow2
  instead of dumping with dd
- Cleanup the spec file

* Tue Mar 5 2013 Daniel B. <daniel@firewall-services.com> - 0.1.3-1
- Send /dev/null to lvm commands stdin

* Tue Nov 20 2012 Daniel B. <daniel@firewall-services.com> - 0.1.2-1
- Fix some spacing issue
- re-add full path to lvcreate and lvremove
- sleep to prevent race conditions

* Thu Jun 28 2012 Daniel B. <daniel@firewall-services.com> - 0.1.1-1
- Don't use absolute path for lvcreate and lvremove

* Sun Jun 17 2012 Daniel B. <daniel@firewall-services.com> - 0.1.0-1
- Move virt-backup to it's own RPM (and GIT repo)

