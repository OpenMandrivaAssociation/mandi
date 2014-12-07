# EDIT IN SVN NOT IN SOURCE PACKAGE (NO PATCH ALLOWED).

Summary:	Monitoring daemon bridge
Name:		mandi
Version:	1.1
Release:	15
License:	GPLv2
Group:		Networking/Other
Url:		http://svn.mandriva.com/cgi-bin/viewvc.cgi/soft/mandi
Source0:	%{name}-%{version}.tar.bz2
BuildRequires:	pkgconfig(dbus-1)
Requires(post,preun):	rpm-helper
Requires:	dbus

%description
Mandi is a monitoring daemon which acts as a bridge from root
monitoring libraries to user applications, using D-Bus.
Its plugin system allows to monitor different kind of events.
A built-in plugin forwards wireless scan results from wpa_supplicant
to user applications.

%package ifw
Summary:	Firewall rules for Interactive Firewall
Group:		Networking/Other
Requires:	mandi = %{version}-%{release}
Requires:	ipset

%description ifw
This package contains the iptables rules used to forward intrusion
detections to the mandi daemon.
It is a component of Interactive Firewall.

%prep
%setup -q

%build
%serverbuild_hardened
export LDFLAGS="%{ldflags}"

%make

%install
install -D -m755 src/%{name} %{buildroot}%{_sbindir}/%{name}
install -D -m644 conf/%{name}.conf %{buildroot}%{_sysconfdir}/dbus-1/system.d/%{name}.conf

%if %mdkver >= 201100
install -D -m644 scripts/%{name}.service %{buildroot}%{_unitdir}/%{name}.service
%else
install -D -m755 scripts/%{name}.init %{buildroot}%{_initrddir}/%{name}
%endif

install -d -m755 %{buildroot}%{_sysconfdir}/ifw/rules.d/
install -m644 rules.d/* %{buildroot}%{_sysconfdir}/ifw/rules.d/
install -m644 scripts/{start,stop} %{buildroot}%{_sysconfdir}/ifw
touch %{buildroot}/%{_sysconfdir}/ifw/whitelist

%if %mdkver >= 201100
%post
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -eq 1 ]; then
    /bin/systemctl enable %{name}.service > /dev/null 2>&1 || :
fi
    /bin/systemctl try-restart %{name}.service > /dev/null 2>&1 || :


%preun
if [ "$1" = "0" ]; then
    /bin/systemctl disable %{name}.service > /dev/null 2>&1 || :
    /bin/systemctl stop %{name}.service > /dev/null 2>&1 || :
fi

%else

%post
%systemd_post mandi

%preun
%systemd_preun mandi

%endif

%files
%{_sbindir}/%{name}
%config %{_sysconfdir}/dbus-1/system.d/%{name}.conf
%if %mdkver >= 201100
%{_unitdir}/mandi.service
%else
%{_initrddir}/mandi
%endif

%files ifw
%dir %{_sysconfdir}/ifw/
%dir %{_sysconfdir}/ifw/rules.d
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/ifw/whitelist
%{_sysconfdir}/ifw/start
%{_sysconfdir}/ifw/stop
%{_sysconfdir}/ifw/rules.d/*

