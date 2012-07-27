Name:           wildmidi
Version:        0.2.2
Release:        8%{?dist}
Summary:        Softsynth midi player
Group:          Applications/Multimedia
License:        GPLv2+
URL:            http://wildmidi.sourceforge.net/index.html
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Patch0:         wildmidi-0.2.2-opt.patch
Patch1:         wildmidi-0.2.2-cfg-abs-path.patch
Patch2:         wildmidi-0.2.2-pulseaudio.patch
Patch3:         wildmidi-0.2.2-bigendian.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  alsa-lib-devel libtool
Requires:       %{name}-libs = %{version}-%{release}

%description
WildMidi is a software midi player which has a core softsynth library that can
be used with other applications. Originally conceived in December 2001 as a
stand alone player, it wasn't until September 2003, and several revisions
later, that the library came into existance.


%package libs
Summary:        WildMidi Midi Wavetable Synth Lib
Group:          System Environment/Libraries
License:        LGPLv2+
Requires:       timidity++-patches

%description libs
This package contains the WildMidi core softsynth library. The library is
designed to process a midi file and stream out the stereo audio data
through a buffer which an external program can then process further.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}-libs = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch0 -p1 -z .opt
%patch1 -p1 -z .abs
%patch2 -p1 -z .pa
%patch3 -p1
sed -i 's/\r//g' COPYING
# we need to update libtool to fix compilation on systems which have lib64
autoreconf -i -f


%build
%configure --disable-static --disable-werror --without-arch
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_bindir}/wildmidi

%files libs
%defattr(-,root,root,-)
%doc COPYING README TODO
%{_libdir}/libWildMidi.so.0*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/libWildMidi.so


%changelog
* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Nov 24 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2.2-6
- Fixup Summary

* Mon Jul  7 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2.2-5
- Fix wildmidi cmdline player sound output on bigendian archs (bz 454198),
  patch by Ian Chapman

* Sat Feb  9 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2.2-4
- Change alsa output code to use regular write mode instead of mmap to make
  it work with pulseaudio (bz 431846)

* Sun Oct 14 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2.2-3
- Require timidity++-patches instead of timidity++ itself so that we don't
  drag in arts and through arts, qt and boost.

* Wed Aug 15 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2.2-2
- Put the lib in a seperate -libs subpackage
- Update License tags for new Licensing Guidelines compliance

* Sat Jul 14 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.2.2-1
- Initial Fedora Extras version
