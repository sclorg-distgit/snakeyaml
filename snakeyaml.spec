%global pkg_name snakeyaml
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}


%global group_id  org.yaml

Name:             %{?scl_prefix}%{pkg_name}
Version:          1.11
Release:          8.10%{?dist}
Summary:          YAML parser and emitter for the Java programming language
License:          ASL 2.0
# http://code.google.com/p/snakeyaml
URL:              http://code.google.com/p/%{pkg_name}
# http://snakeyaml.googlecode.com/files/SnakeYAML-all-1.9.zip
Source0:          http://%{pkg_name}.googlecode.com/files/SnakeYAML-all-%{version}.zip

# Upstream has forked gdata-java and base64 and refuses [1] to
# consider replacing them by external dependencies.  Bundled libraries
# need to be removed and their use replaced by system libraries.
# See rhbz#875777 and http://code.google.com/p/snakeyaml/issues/detail?id=175
#
# Remove use of bundled Base64 implementation
Patch0:           0001-Replace-bundled-base64-implementation.patch
# We don't have gdata-java in Fedora any longer, use commons-codec instead
Patch1:           0002-Replace-bundled-gdata-java-client-classes-with-commo.patch

BuildArch:        noarch

BuildRequires:    %{?scl_prefix_java_common}javapackages-tools
BuildRequires:    %{?scl_prefix_java_common}maven-local
BuildRequires:    maven30-maven-surefire-provider-junit
BuildRequires:    maven30-cobertura
BuildRequires:    maven30-joda-time
BuildRequires:    maven30-gnu-getopt
BuildRequires:    maven30-base64coder
BuildRequires:    %{?scl_prefix_java_common}apache-commons-codec
%{?fedora:BuildRequires: springframework}

%description
SnakeYAML features:
    * a complete YAML 1.1 parser. In particular,
      SnakeYAML can parse all examples from the specification.
    * Unicode support including UTF-8/UTF-16 input/output.
    * high-level API for serializing and deserializing
      native Java objects.
    * support for all types from the YAML types repository.
    * relatively sensible error messages.


%package javadoc
Summary:          API documentation for %{pkg_name}

%description javadoc
This package contains the API documentation for %{pkg_name}.

%prep
%setup -q -n %{pkg_name}
%{?scl:scl enable maven30 %{scl} - <<"EOF"}
set -e -x

%patch0 -p1
%patch1 -p1

%pom_remove_plugin org.codehaus.mojo:cobertura-maven-plugin
%pom_add_dep net.sourceforge.cobertura:cobertura:any:test
sed -i "/<artifactId>spring</s/spring/&-core/" pom.xml
rm -f src/test/java/examples/SpringTest.java

# Replacement for bundled gdata-java-client
%pom_add_dep commons-codec:commons-codec

# remove bundled stuff
rm -rf target
rm -rf src/main/java/org/yaml/snakeyaml/external

# convert CR+LF to LF
sed -i 's/\r//g' LICENSE.txt

%if !0%{?fedora}
# Remove test dependencies because tests are skipped anyways.
%pom_xpath_remove "pom:dependency[pom:scope[text()='test']]"
%endif

%mvn_file : %{pkg_name}
%{?scl:EOF}

%build
%{?scl:scl enable maven30 %{scl} - <<"EOF"}
set -e -x
%mvn_build %{!?fedora:-f}
%{?scl:EOF}

%install
%{?scl:scl enable maven30 %{scl} - <<"EOF"}
set -e -x
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%doc LICENSE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%changelog
* Sat Jan 09 2016 Michal Srb <msrb@redhat.com> - 1.11-8.10
- maven33 rebuild

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 1.11-8.9
- Mass rebuild 2015-01-13

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 1.11-8.8
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.11-8.7
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.11-8.6
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.11-8.5
- Mass rebuild 2014-02-18

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.11-8.4
- Remove requires on java

* Mon Feb 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.11-8.3
- SCL-ize build-requires

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.11-8.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.11-8.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.11-8
- Mass rebuild 2013-12-27

* Thu Aug 22 2013 Michal Srb <msrb@redhat.com> - 1.11-7
- Migrate away from mvn-rpmbuild (#997461)

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.11-6
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Fri Apr 26 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.11-5
- Explain gdata-java and base64 bundling situation
- Resolves: rhbz#875777

* Mon Apr 22 2013 Michal Srb <msrb@redhat.com> - 1.11-5
- Replace bundled base64 implementation
- Replace bundled gdata-java-client classes with apache-commons-codec

* Wed Apr 10 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.11-4
- Conditionally disable tests
- Conditionally remove test dependencies from POM

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.11-2
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Mon Oct 15 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.11-1
- Update to upstream version 1.11

* Mon Oct 15 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.9-3
- Remove unneeded dependencies: base64coder, gdata-java
- Convert pom.xml patch to POM macro

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 20 2012 Mo Morsi <mmorsi@redhat.com> - 1.9-1
- Update to latest upstream release
- patch2, patch3 no longer needed
- update to latest fedora java guidelines

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jun 20 2011 Jaromir Capik <jcapik@redhat.com> - 1.8-6
- Patch for the issue67 test removed

* Fri Jun 17 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.8-5
- Add osgi metadata to jar file (#713935)

* Thu Jun 09 2011 Jaromir Capik <jcapik@redhat.com> - 1.8-4
- File handle leaks patched

* Tue Jun 07 2011 Jaromir Capik <jcapik@redhat.com> - 1.8-3
- base64coder-java renamed to base64coder

* Wed Jun 01 2011 Jaromir Capik <jcapik@redhat.com> - 1.8-2
- Bundled stuff removal

* Mon May 16 2011 Jaromir Capik <jcapik@redhat.com> - 1.8-1
- Initial version of the package
