# EDIT IN SVN NOT IN SOURCE PACKAGE (NO PATCH ALLOWED).

%define name mandi
%define version 1.0
%define release %mkrel 11

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
touch %{buildroot}/%{_sysconfdir}/ifw/whitelist

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
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/ifw/whitelist
%{_sysconfdir}/ifw/start
%{_sysconfdir}/ifw/stop
%{_sysconfdir}/ifw/rules.d/*


%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0-10mdv2011.0
+ Revision: 666380
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0-9mdv2011.0
+ Revision: 606628
- rebuild

* Sun Mar 14 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0-8mdv2010.1
+ Revision: 519037
- rebuild

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.0-7mdv2010.0
+ Revision: 426072
- rebuild

* Mon Mar 30 2009 Eugeni Dodonov <eugeni@mandriva.com> 1.0-6mdv2009.1
+ Revision: 362586
- Installing missing whitelist file to prevent mandi from complaining on start (#49215 #48173).

* Mon Jan 26 2009 Eugeni Dodonov <eugeni@mandriva.com> 1.0-5mdv2009.1
+ Revision: 333916
- Disable MDV_LDFLAGS for now, as it crashes mandi daemon.

* Mon Dec 22 2008 Olivier Blin <oblin@mandriva.com> 1.0-4mdv2009.1
+ Revision: 317475
- 1.0
- wireless plugin: forward wpa_supplicant events to listeners

* Sat Dec 20 2008 Oden Eriksson <oeriksson@mandriva.com> 0.9-4mdv2009.1
+ Revision: 316440
- use the %%ldflags macro

* Fri Dec 19 2008 Oden Eriksson <oeriksson@mandriva.com> 0.9-3mdv2009.1
+ Revision: 316245
- use %%optflags and LDFLAGS

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 0.9-2mdv2009.0
+ Revision: 223150
- rebuild

* Tue Mar 04 2008 Olivier Blin <oblin@mandriva.com> 0.9-1mdv2008.1
+ Revision: 179234
- 0.9
- adapt to new IFW kernel module (from Luiz Fernando N. Capitulino)
- unref shared dbus connection instead of closing it
- remove some debug messages

* Mon Mar 03 2008 Olivier Blin <oblin@mandriva.com> 0.8.2-4mdv2008.1
+ Revision: 177941
- do not require shorewall for post script anymore
- require rpm-helper for preun

* Tue Jan 15 2008 Thierry Vignaud <tv@mandriva.org> 0.8.2-3mdv2008.1
+ Revision: 152902
- rebuild
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Wed Aug 22 2007 Adam Williamson <awilliamson@mandriva.org> 0.8.2-1mdv2008.0
+ Revision: 69295
- Import mandi



* Tue Aug  8 2006 Olivier Blin <oblin@mandriva.com> 0.8.2-1mdv2007.0
- 0.8.2: close D-Bus connection on exit

* Sun Jul 16 2006 Olivier Blin <oblin@mandriva.com> 0.8.1-1mdv2007.0
- 0.8.1: abort only if all plugin fail to init
- remove triggerpostun migration stuff, it was cooker only

* Mon May 15 2006 Olivier Blin <oblin@mandriva.com> 0.8.0-1mdk
- mandi init script should start shorewall
  (for the iptables modules to be loaded, #21629)

* Thu Jan 26 2006 Olivier Blin <oblin@mandriva.com> 0.7.9-3mdk
- rebuild for new dbus

* Mon Jan  9 2006 Olivier Blin <oblin@mandriva.com> 0.7.9-2mdk
- fix typo in initscript

* Mon Jan  9 2006 Olivier Blin <oblin@mandriva.com> 0.7.9-1mdk
- 0.7.9: convert parallel init to LSB

* Mon Jan  2 2006 Olivier Blin <oblin@mandriva.com> 0.7.8-1mdk
- 0.7.8: fix parallel init (dbus service is named messagebus)

* Sun Jan  1 2006 Olivier Blin <oblin@mandriva.com> 0.7.7-1mdk
- 0.7.7: parallel init support

* Fri Nov  4 2005 Olivier Blin <oblin@mandriva.com> 0.7.6-1mdk
- 0.7.6: more dbus 0.50 fixes
  (dbus_message_append_args wants pointers now)

* Thu Oct 27 2005 Olivier Blin <oblin@mandriva.com> 0.7.5-1mdk
- 0.7.5: switch to dbus 0.50

* Fri Sep 23 2005 Olivier Blin <oblin@mandriva.com> 0.7.4-1mdk
- 0.7.4:
  o fix saving whitelist
  o don't skip reports when a another attack is being reported

* Thu Sep  8 2005 Olivier Blin <oblin@mandrakesoft.com> 0.7.3-1mdk
- 0.7.3:
  o fix stop script to remove all entries in the Ifw rule
  o fix D-Bus message order for blacklist notification

* Sun Sep  4 2005 Olivier Blin <oblin@mandriva.com> 0.7.2-2mdk
- remove "INCLUDE ifw" in shorewall start file on upgrade

* Thu Sep  1 2005 Olivier Blin <oblin@mandriva.com> 0.7.2-1mdk
- mandi: save white list right after adding/modifying entries

* Thu Sep  1 2005 Olivier Blin <oblin@mandriva.com> 0.7.1-1mdk
- 0.7.1:
  o add start/stop scripts
  o add rules.d directorty, with a sample psd rule
  o shorewall isn't required by the package anymore
  o remove shorewall workarounds, it'is better done by drakfirewall now
  o notify attacks even if attacker is already present in log
  o don't create ipsets in the daemon

* Thu Aug 25 2005 Olivier Blin <oblin@mandriva.com> 0.7-2mdk
- use clean tarball (fix build on 64 bits, thanks couriousous)

* Wed Aug 24 2005 Olivier Blin <oblin@mandriva.com> 0.7-1mdk
- 0.7, IFW plugin improvements:
  o keep logs and allow to clear them
  o allow applications to notify themselves when the user has
    checked reports or asked to manage the lists
  o send notifications in automatic mode too

* Mon Aug 22 2005 Olivier Blin <oblin@mandriva.com> 0.6-4mdk
- do not match for ESTABLISHED,RELATED connections (Samir),
  this should avoid DNS blacklist

* Mon Aug 22 2005 Olivier Blin <oblin@mandriva.com> 0.6-3mdk
- remove ifw inclusion in shorewall on full removal only

* Sat Aug 20 2005 Olivier Blin <oblin@mandriva.com> 0.6-2mdk
- really fix dbus permissions

* Fri Aug 19 2005 Olivier Blin <oblin@mandriva.com> 0.6-1mdk
- 0.6
  o create ipsets in shorewall start script
  o start mandi service after messagebus
  o allow console users to use Interactive Firewall

* Thu Aug 18 2005 Olivier Blin <oblin@mandriva.com> 0.5-1mdk
- 0.5
  o use an Ifw chain in shorewall/iptables
  o handle blacklist and whitelist in the Ifw chain

* Thu Aug 18 2005 Olivier Blin <oblin@mandriva.com> 0.4-1mdk
- 0.4 (ignore notifications from the loopback interface)
- start mandi daemon as a service
- add a mandi-ifw subpackage to insert Interactive Firewall in
  shorewall start rules
- use psd to detect port scans

* Thu Aug 11 2005 Olivier Blin <oblin@mandriva.com> 0.3-1mdk
- 0.3, Interactive Firewall improvements:
  o really support ipset (using iptrees)
  o use correct byte order to add IP addresses in iptrees
  o send only one attack report per IP address
  o fix description (thanks to Mathieu Geli)

* Fri Jul 29 2005 Olivier Blin <oblin@mandriva.com> 0.2-1mdk
- 0.2 (small bugfix)
- Requires ipset

* Thu Jul 28 2005 Olivier Blin <oblin@mandriva.com> 0.1-1mdk
- allow to select a wireless network
- enable fake Active Firewall mode

* Fri Jul 15 2005 Olivier Blin <oblin@mandriva.com> 0.1-0.1mdk
- initial release
