%define section         free
%bcond_without          full
%define gcj_support     0

Name:           bsf
Version:        2.4.0
Release:        3
Epoch:          0
Summary:        Bean Scripting Framework
License:        Apache License
Url:            http://jakarta.apache.org/bsf/
Group:          Development/Java
#Vendor:        JPackage Project
#Distribution:  JPackage
Source0:        http://www.apache.org/dist/jakarta/bsf/source/bsf-src-%{version}.tar.gz
Source1:        http://www.apache.org/dist/jakarta/bsf/source/bsf-src-%{version}.tar.gz.asc
Source2:        http://www.apache.org/dist/jakarta/bsf/source/bsf-src-%{version}.tar.gz.md5
Source3:        build-properties.xml
Requires:       jakarta-commons-logging
Requires:       jython
Requires:       rhino
Requires:       servletapi5
Requires:       java >= 0:1.6
BuildRequires:  ant
BuildRequires:  jakarta-commons-logging
%if %with full
#BuildRequires: jacl
BuildRequires:  jython
#BuildRequires: netrexx
BuildRequires:  rhino
BuildRequires:  java-devel >= 0:1.6
%endif
BuildRequires:  servletapi5
BuildRequires:	java-rpmbuild
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
Buildarch:      noarch
%endif

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
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
%{_bindir}/find . -name '*.jar' -o -name '*.class' | %{_bindir}/xargs -t %{__rm}
cp -a %{SOURCE3} build-properties.xml

%build
%if %with full
export CLASSPATH=$(build-classpath rhino xalan-j2 jython servletapi5 jspapi jakarta-commons-logging)
%else
export CLASSPATH=$(build-classpath servletapi5 jspapi jakarta-commons-logging)
%endif
##export CLASSPATH=$CLASSPATH:$JAVA_HOME/lib/tools.jar
%{ant} bindist

%install
%{__rm} -rf %{buildroot}
# jar
%{__mkdir_p} 755 %{buildroot}%{_javadir}
cp -a dist/bsf-%{version}/lib/bsf.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do %{__ln_s} ${jar} ${jar/-%{version}/}; done)
# javadoc
%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -a dist/bsf-%{version}/docs/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
(cd %{buildroot}%{_javadocdir} && %{__ln_s} %{name}-%{version} %{name})

%{__perl} -pi -e 's/\r$//g' dist/bsf-%{version}/samples/scriptedui/ui.jacl dist/bsf-%{version}/samples/scriptedui/ui.py

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%post javadoc
%{__rm} -f %{_javadocdir}/%{name}
%{__ln_s} %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ $1 -eq 0 ]; then
  %{__rm} -f %{_javadocdir}/%{name}
fi

%files
%defattr(0644,root,root,0755)
%doc dist/bsf-%{version}/*.txt dist/bsf-%{version}/samples
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%dir %{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}-%{version}/*
%ghost %{_javadocdir}/%{name}




%changelog
* Tue Nov 30 2010 Oden Eriksson <oeriksson@mandriva.com> 0:2.4.0-1.8mdv2011.0
+ Revision: 603771
- rebuild

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 0:2.4.0-1.7mdv2010.1
+ Revision: 522302
- rebuilt for 2010.1

* Tue Aug 18 2009 Jaroslav Tulach <jtulach@mandriva.org> 0:2.4.0-1.6mdv2010.0
+ Revision: 417724
- Simplifying dependencies. Requiring java 1.6 and removing special dependencies on various XML tools as they are part of java 1.6 already

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 0:2.4.0-1.5mdv2010.0
+ Revision: 413186
- rebuild

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 0:2.4.0-1.4mdv2009.0
+ Revision: 136280
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:2.4.0-1.4mdv2008.1
+ Revision: 120805
- buildrequires java-rpmbuild

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:2.4.0-1.3mdv2008.0
+ Revision: 87257
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Sat Sep 08 2007 Pascal Terjan <pterjan@mandriva.org> 0:2.4.0-1.2mdv2008.0
+ Revision: 82698
- update to new version


* Thu Mar 22 2007 David Walluck <walluck@mandriva.org> 0:2.4.0-1.1mdv2007.1
+ Revision: 147890
- (Build)Requires jakarta-commons-logging, not log4j
- fix (Build)Requires, specifically log4j
- 2.4.0
- Import bsf

* Sun Jul 23 2006 David Walluck <walluck@mandriva.org> 0:2.3.0-10.1mdv2007.0
- bump release

* Sun Jun 04 2006 David Walluck <walluck@mandriva.org> 0:2.3.0-8.3mdv2007.0
- rebuild for libgcj.so.7
- aot-compile

* Mon May 16 2005 David Walluck <walluck@mandriva.org> 0:2.3.0-8.2mdk
- update javac patch

* Mon May 16 2005 David Walluck <walluck@mandriva.org> 0:2.3.0-8.1mdk
- release

* Wed Nov 03 2004 Nicolas Mailhot <nim@jpackage.org>  0:2.3.0-8jpp
- Clean up specfile a bit

* Sat Aug 21 2004 Ralph Apel <r.apel at r-apel.de> 0:2.3.0-7jpp
- Build with ant-1.6.2

