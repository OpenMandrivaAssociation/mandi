# EDIT IN SVN NOT IN SOURCE PACKAGE (NO PATCH ALLOWED).

Summary:	Monitoring daemon bridge
Name:		mandi
Version:	1.1
Release:	1
License:	GPL
Group:		Networking/Other
Url:		http://svn.mandriva.com/cgi-bin/viewvc.cgi/soft/mandi
Source0:	%{name}-%{version}.tar.bz2
BuildRequires:	dbus-devel
Requires(post):	rpm-helper
Requires(preun):	rpm-helper
Requires:	dbus
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Mandi is a monitoring daemon which acts as a bridge from root
monitoring libraries to user applications, using D-Bus.
Its plugin system allows to monitor different kind of events.
A built-in plugin forwards wireless scan results from wpa_supplicant
to user applications.

%package ifw
Summary:	Firewall rules for Interactive Firewall
Group:		Networking/Other
Requires:	mandi = %{version}
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
rm -rf %{buildroot}
install -D -m755 src/%{name} %{buildroot}%{_sbindir}/%{name}
install -D -m644 conf/%{name}.conf %{buildroot}%{_sysconfdir}/dbus-1/system.d/%{name}.conf

%if %mdkver >= 201100
install -D -m755 scripts/%{name}.service %{buildroot}%{_systemunitdir}/%{name}
%else
install -D -m755 scripts/%{name}.init %{buildroot}%{_initrddir}/%{name}
%endif

install -d -m755 %{buildroot}%{_sysconfdir}/ifw/rules.d/
install -m644 rules.d/* %{buildroot}%{_sysconfdir}/ifw/rules.d/
install -m644 scripts/{start,stop} %{buildroot}%{_sysconfdir}/ifw
touch %{buildroot}/%{_sysconfdir}/ifw/whitelist

%clean
rm -rf %{buildroot}

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
%_post_service mandi

%preun
%_preun_service mandi

%endif



%files
%defattr(-,root,root)
%{_sbindir}/%{name}
%config %{_sysconfdir}/dbus-1/system.d/%{name}.conf

%if %mdkver >= 201100
%{_systemunitdir}/mandi
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
