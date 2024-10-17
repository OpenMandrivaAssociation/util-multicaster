%define section         free
# according to crisb dead upstream. sflo
%define gcj_support     0

Name:           util-multicaster
Version:        0.3.3
Release:        0.0.6
Epoch:          0
Summary:        Utility classes for low-cost event dispatch to multiple listeners
License:        MIT
Group:          Development/Java
URL:            https://www.freecompany.org/
# svn export https://svn.freecompany.org/public/util/tags/util-multicaster-0.3.3
# zip -9r util-multicaster-src-0.3.3.zip util-multicaster-0.3.3
Source0:        http://repository.freecompany.org/org/freecompany/util/zips/util-multicaster-src-%{version}.zip
Source1:        util-multicaster-0.3.3-build.xml
BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  java-rpmbuild >= 0:1.6
BuildRequires:  junit
%if %{gcj_support}
BuildRequires:  java-sdk-gcj = 1.5.0.0
%else
BuildRequires:  java-devel
BuildArch:      noarch
%endif

%description
The multicaster package provides utility classes for low-cost event dispatch 
to multiple listeners. Modeled after the AWTEventMulticaster this class 
provides type-safe and thread-safe generic method dispatch. The benefit of 
this approach to handling multiple listeners is the low overhead - when there 
is a single listener there is zero cost, and each additional listener requires 
only two additional method calls.

A basic implementation is provided, the DefaultMulticaster, which uses dynamic 
proxies to minimize the amount of new code that must be written in order to use 
a multicaster.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q
cp -a %{SOURCE1} build.xml
perl -pi -e 's|<javac|<javac nowarn="true"|g' build.xml

%build
export CLASSPATH=$(build-classpath junit)
export OPT_JAR_LIST="ant/ant-junit"
%{ant} jar javadoc test

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_javadir}
cp -af dist/%{name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do %{__ln_s} ${jar} ${jar/-%{version}/}; done)

mkdir -p %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -ra dist/doc/* %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__ln_s} %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-%{version}.jar.db
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-%{version}.jar.so
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}
