%define section         free
%bcond_without          full
%define gcj_support     0

Name:           bsf
Version:        2.4.0
Release:        %mkrel 1.7
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
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

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
%{__cp} -a %{SOURCE3} build-properties.xml

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
%{__cp} -a dist/bsf-%{version}/lib/bsf.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do %{__ln_s} ${jar} ${jar/-%{version}/}; done)
# javadoc
%{__mkdir_p} %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -a dist/bsf-%{version}/docs/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
(cd %{buildroot}%{_javadocdir} && %{__ln_s} %{name}-%{version} %{name})

%{__perl} -pi -e 's/\r$//g' dist/bsf-%{version}/samples/scriptedui/ui.jacl dist/bsf-%{version}/samples/scriptedui/ui.py

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
%{__rm} -rf %{buildroot}

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


