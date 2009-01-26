# EDIT IN SVN NOT IN SOURCE PACKAGE (NO PATCH ALLOWED).

%define name mandi
%define version 1.0
%define release %mkrel 5

Summary:	Monitoring daemon bridge
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	%{name}-%{version}.tar.bz2
#Patch0:		mandi-0.9-MDV_LDFLAGS.diff
License:	GPL
Group:		Networking/Other
Url:		http://cvs.mandriva.com/cgi-bin/cvsweb.cgi/soft/mandi/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:  dbus-devel
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires:       dbus

%description
Mandi is a monitoring daemon which acts as a bridge from root
monitoring libraries to user applications, using D-Bus.
Its plugin system allows to monitor different kind of events.
A built-in plugin forwards wireless scan results from wpa_supplicant
to user applications.

%package ifw
Summary:	Firewall rules for Interactive Firewall
Group:		Networking/Other
Requires:       mandi = %{version}
Requires:       ipset

%description ifw
This package contains the iptables rules used to forward intrusion
detections to the mandi daemon.
It is a component of Interactive Firewall.

%prep
%setup -q
#%patch0 -p0 -b .MDV_LDFLAGS

%build
%make

%install
rm -rf %{buildroot}
install -D -m755 src/%{name} %{buildroot}%{_sbindir}/%{name}
install -D -m644 conf/%{name}.conf %{buildroot}%{_sysconfdir}/dbus-1/system.d/%{name}.conf
install -D -m755 scripts/%{name}.init %buildroot%{_initrddir}/%{name}
install -d -m755 %buildroot%{_sysconfdir}/ifw/rules.d/
install -m644 rules.d/* %buildroot%{_sysconfdir}/ifw/rules.d/
install -m644 scripts/{start,stop} %{buildroot}%{_sysconfdir}/ifw

%clean
rm -rf %{buildroot}

%post
%_post_service mandi

%preun
%_preun_service mandi

%files
%defattr(-,root,root)
%{_sbindir}/%{name}
%config %{_sysconfdir}/dbus-1/system.d/%{name}.conf
%{_initrddir}/mandi

%files ifw
%dir %{_sysconfdir}/ifw/
%{_sysconfdir}/ifw/start
%{_sysconfdir}/ifw/stop
%{_sysconfdir}/ifw/rules.d/*
