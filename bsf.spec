%{?_javapackages_macros:%_javapackages_macros}
%undefine __cp
%define __cp /bin/cp
# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

Name:           bsf
Version:        2.4.0
Release:        17.1%{?dist}
Epoch:          0
Summary:        Bean Scripting Framework
License:        ASL 2.0
URL:            http://commons.apache.org/bsf/

Source0:        http://apache.mirror.anlx.net//commons/%{name}/source/%{name}-src-%{version}.tar.gz
Source1:        %{name}-pom.xml
Patch0:         build-file.patch
Patch1:	        build.properties.patch
BuildRequires:  jpackage-utils >= 1.6
BuildRequires:  ant
BuildRequires:  xalan-j2
BuildRequires:  rhino
BuildRequires:  apache-commons-logging
Requires:       xalan-j2
Requires:       apache-commons-logging
Requires:       jpackage-utils
BuildArch:      noarch

%description
Bean Scripting Framework (BSF) is a set of Java classes which provides
scripting language support within Java applications, and access to Java
objects and methods from scripting languages. BSF allows one to write
JSPs in languages other than Java while providing access to the Java
class library. In addition, BSF permits any Java application to be
implemented in part (or dynamically extended) by a language that is
embedded within it. This is achieved by providing an API that permits
calling scripting language engines from within Java, as well as an
object registry that exposes Java objects to these scripting language
engines.

BSF supports several scripting languages currently:
* Javascript (using Rhino ECMAScript, from the Mozilla project)
* Python (using either Jython or JPython)
* Tcl (using Jacl)
* NetRexx (an extension of the IBM REXX scripting language in Java)
* XSLT Stylesheets (as a component of Apache XML project's Xalan and
Xerces)

In addition, the following languages are supported with their own BSF
engines:
* Java (using BeanShell, from the BeanShell project)
* JRuby
* JudoScript

%package javadoc
Summary:        Javadoc for %{name}

Requires:       jpackage-utils

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
# remove all binary libs
find . -name "*.jar" -exec %{__rm} -f {} \;
%{__rm} -fr bsf

%patch0 -p1
%patch1 -p1

%build
[ -z "$JAVA_HOME" ] && export JAVA_HOME=%{_jvmdir}/java
export CLASSPATH=$(build-classpath apache-commons-logging xalan-j2 rhino)
ant jar
%{__rm} -rf bsf/src/org/apache/bsf/engines/java
ant javadocs

%install
# jar
%{__install} -d -m 755 %{buildroot}%{_javadir}
%{__install} -m 644 build/lib/%{name}.jar \
             %{buildroot}%{_javadir}/%{name}.jar
# javadoc
%{__install} -d -m 755 %{buildroot}%{_javadocdir}/%{name}
%{__cp} -pr build/javadocs/* %{buildroot}%{_javadocdir}/%{name}

%{__install} -DTm 644 %{SOURCE1} %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom
%add_maven_depmap JPP-%{name}.pom %{name}.jar -a "org.apache.bsf:%{name}"

%pre javadoc
# workaround for rpm bug, can be removed in F-20
[ $1 -gt 1 ] && [ -L %{_javadocdir}/%{name} ] && \
rm -rf $(readlink -f %{_javadocdir}/%{name}) %{_javadocdir}/%{name} || :

%files
%doc LICENSE.txt AUTHORS.txt CHANGES.txt NOTICE.txt README.txt TODO.txt RELEASE-NOTE.txt
%{_javadir}/%{name}.jar
%{_mavenpomdir}/JPP-%{name}.pom
%{_mavendepmapfragdir}/%{name}

%files javadoc
%doc LICENSE.txt NOTICE.txt
%{_javadocdir}/%{name}

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.4.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.4.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 22 2012 Tomas Radej <tradej@redhat.com> - 0:2.4.0-15
- Fixed URL of Source0

* Tue Nov 20 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:2.4.0-14
- Remove unneeded BR: jython

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.4.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Mar 16 2012 Alexander Kurtakov <akurtako@redhat.com> 0:2.4.0-12
- Drop jsp/servlet api dependencies, leftovers from the past.

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.4.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec  2 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.4.0-10
- Fixes according to latest guidelines
- Fix maven depmap

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Sep 21 2010 Orion Poplawski <orion@cora.nwra.com> - 0:2.4.0-8
- Build against rhino for JavaScript support

* Mon Jun 14 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.4.0-7
- Added pom file to enable maven dependency resolution
- Fix Source0 URL
- Fix Group designation

* Mon Jun  7 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:2.4.0-6
- Fix BR after jakarta-commons rename

* Wed Apr 7 2010 Alexander Kurtakov <akurtako@redhat.com> 0:2.4.0-5
- Drop gcj support.
- Build against servlet and jsp apis from tomcat6.

* Mon Jan 11 2010 Andrew Overholt <overholt@redhat.com> 2.4.0-4
- Fix License (ASL 2.0 and not 1.1) (rhbz#554465).

* Mon Sep 14 2009 Christoph Höger <choeger@cs.tu-berlin.de> - 0:2.4.0-3
- Fix typo in Requires

* Wed Sep 09 2009 Christoph Höger <choeger@cs.tu-berlin.de> - 0:2.4.0-1
- New Upstream release: 2.4.0
- Add jython build dependency to include bsf-jython engine

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.3.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:2.3.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:2.3.0-13
- drop repotag
- fix license

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:2.3.0-12jpp.2
- Autorebuild for GCC 4.3

* Wed Mar 07 2007 Permaine Cheung <pcheung@redhat.com> 0:2.3.0-11jpp.2
- Update spec file as per Fedora guidelines

* Thu Aug 03 2006 Deepak Bhole <dbhole@redhat.com> 0:2.3.0-11jpp.1
- Added missing requirements.

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> 0:2.3.0-10jpp_2fc
- Rebuilt

* Fri Jul 21 2006 Deepak Bhole <dbhole@redhat.com> 0:2.3.0-10jpp_2fc
- Removing vendor and distribution tags.

* Thu Jul 20 2006 Deepak Bhole <dbhole@redhat.com> 0:2.3.0-10jpp_1fc
- Added conditional native compilation.
- From gbenson@redhat:
-   Build without Jython or Rhino for now.
-   Build with servletapi5.
-   Avoid Sun-specific classes.

* Wed Apr 26 2006 Fernando Nasser <fnasser@redhat.com>  0:2.3.0-9jpp
- First JPP 1.7 build

* Wed Nov 3 2004 Nicolas Mailhot <nim@jpackage.org>  0:2.3.0-8jpp
- Clean up specfile a bit

* Fri Aug 20 2004 Ralph Apel <r.apel at r-apel.de> 0:2.3.0-7jpp
- Build with ant-1.6.2

* Thu Oct 09 2003 David Walluck <david@anti-microsoft.org> 0:2.3.0-6jpp
- add javadoc symlinks
- change Apache Software License to Apache License

* Tue Aug 26 2003 David Walluck <david@anti-microsoft.org> 0:2.3.0-5jpp
- remove all Requires

* Fri Apr 12 2003 David Walluck <david@anti-microsoft.org> 0:2.3.0-4jpp
- fix strange permissions

* Fri Apr 11 2003 David Walluck <david@anti-microsoft.org> 0:2.3.0-3jpp
- rebuild for jpackage 1.5

* Wed Jan 22 2003 David Walluck <david@anti-microsoft.org> 2.3.0-2jpp
- Requires/BuildRequires: xalan-j2
- update %%description

* Mon Jan 13 2003 David Walluck <david@anti-microsoft.org> 2.3.0-1jpp
- version 2.3.0 (first jakarta release)

* Tue May 07 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 2.2-5jpp
- vendor, distribution, group tags
- versioned dir for javadoc
- section macro

* Sat Dec 1 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 2.2-4jpp
- javadoc in javadoc package

* Wed Nov 21 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 2.2-3jpp
- removed packager tag
- new jpp extension
- fixed url

* Sat Oct 6 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 2.2-2jpp
- first unified release
- used original tarball
- s/jPackage/JPackage

* Thu Aug 30 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 2.2-1jpp
- first Mandrake release
