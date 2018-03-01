# https://github.com/xVST/xVideoServiceThief/commit/14dee4551645f6e23000c497f5c17631de98a368
%global commit  14dee4551645f6e23000c497f5c17631de98a368
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global gitdate 20171201
%global rname   xVST

Summary:        Downloading your favourite video clips from a lot of websites
Name:           xvst
Version:        3.0
Release:        2.%{gitdate}git%{shortcommit}%{?dist}
License:        GPLv3+
URL:            http://www.xvideothief.com
Source0:        https://github.com/xVST/xVideoServiceThief/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
Source1:        %{name}.desktop

Patch0:         beeg.patch
Patch1:         chilloutzone.patch
Patch2:         disable_update.patch
Patch3:         keezmovies.patch
Patch4:         myvideo.patch
Patch5:         sunporno.patch
Patch6:         wat.tv.patch

ExcludeArch:    ppc64 ppc64le

BuildRequires:  desktop-file-utils
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtwebkit-devel
BuildRequires:  qt5-qtscript-devel
BuildRequires:  qt5-qttools-devel
BuildRequires:  qt5-qtwebengine-devel
BuildRequires:  librtmp-devel
Requires:       ffmpeg
Requires:       youtube-dl

%description
xVideoServiceThief (a.k.a xVST) is a tool for downloading your favourite
video clips from a lot of video websites (currently supports 93 websites
and increasing!).
xVideoServiceThief also provide you the ability to convert each video
in most popular formats: AVI, MPEG1, MPEG2, WMV, MP4, 3GP, MP3 file formats.

%prep
%setup -qn xVideoServiceThief-%{commit}

# removed bundled rtmpdump
rm -rf src/rtmpdump

# Patches provided by getdeb.net. Add/fix download sites and turns off
# automatic updates.

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

# Fix path names and end-of-line encoding.
sed -i "s|getApplicationPath()\ +\ \"|\"/usr/share/%{name}|g" src/options.cpp
sed -i 's/\r//' "how to compile.txt"

chmod 0644 resources/services/youporngay/youporngay.js
chmod 0644 resources/services/tube8/tube8.js
chmod 0644 resources/services/hardsextube/hardsextube.js

%build
# Creat translation files.
lrelease-qt5 resources/translations/*.ts
rm -f resources/translations/template_for_new_translations.qm

%{qmake_qt5} \
CONFIG+="release"
%make_build

%install
install -d -m 0755 %{buildroot}%{_datadir}/%{name}/{plugins,languages}
find resources/services -name "*.js" \
        -exec cp -dpR {} %{buildroot}%{_datadir}/%{name}/plugins \;
install -m 0644 resources/translations/*.qm \
         %{buildroot}%{_datadir}/%{name}/languages
install -m 0644 resources/translations/definitions/*.language \
         %{buildroot}%{_datadir}/%{name}/languages
install -Dm755 bin/%{name} %{buildroot}%{_bindir}/%{name}
install -Dm644 %{SOURCE1} %{buildroot}%{_datadir}/applications/%{name}.desktop
install -Dm644 resources/images/InformationLogo.png %{buildroot}%{_datadir}/pixmaps/%{name}.png

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%post
update-desktop-database &> /dev/null || :

%postun
update-desktop-database &> /dev/null || :

%files
%license GPL.txt
%doc README.md resources/{changelog.txt,service_list.html}
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/plugins/
%{_datadir}/%{name}/languages/*language
%{_datadir}/%{name}/languages/*qm

%changelog
* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 3.0-2.20171201git14dee45
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Jan 07 2018 Martin Gansser <linux4martin@gmx.de> 3.0-1.20171201git14dee45
- Update to 3.0-1.20171201git14dee45

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 2.6-2.20170307git73d3f51
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jun 24 2017 Martin Gansser <linux4martin@gmx.de> 2.6-1.20170307git73d3f51
- Update to recent git version 2.6-1.20170307git73d3f51
- Dropped patch7
- Add BR qt5-qtwebengine-devel
- Add ExcludeArch: ppc64 ppc64le

* Tue Mar 21 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 2.5.2-6.20140804gitcbfafe4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jul 20 2016 Leigh Scott <leigh123linux@googlemail.com> - 2.5.2-5.20140804gitcbfafe4
- fix bundled qtsingleapplication

* Sat Mar 21 2015 Martin Gansser <linux4martin@gmx.de> 2.5.2-4.20140804gitcbfafe4
- dropped macro %%find_lang because it doesn't work in this certain case
- dropped macro %%exclude from %%{_datadir}/%%{name}/languages/*qm

* Fri Mar 20 2015 Martin Gansser <linux4martin@gmx.de> 2.5.2-3.20140804gitcbfafe4
- dropped %%Provides tag
- added %%find_lang macro to find .qm files

* Sun Mar 08 2015 Martin Gansser <linux4martin@gmx.de> 2.5.2-2.20140804gitcbfafe4
- removed bundled rtmpdump
- added BR librtmp-devel

* Sat Mar 07 2015 Martin Gansser <linux4martin@gmx.de> 2.5.2-1.20140804gitcbfafe4
- Inital build for Fedora

