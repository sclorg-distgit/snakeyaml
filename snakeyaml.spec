%{?scl:%scl_package snakeyaml}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

%global vertag 3f1ee79d50cf

Name:             %{?scl_prefix}snakeyaml
Version:          1.13
Release:          9.1%{?dist}
Summary:          YAML parser and emitter for the Java programming language
License:          ASL 2.0
# http://code.google.com/p/snakeyaml
URL:              http://code.google.com/p/%{pkg_name}
Source0:          https://snakeyaml.googlecode.com/archive/v%{version}.zip#/%{pkg_name}-%{version}.zip

# Upstream has forked gdata-java and base64 and refuses [1] to
# consider replacing them by external dependencies.  Bundled libraries
# need to be removed and their use replaced by system libraries.
# See rhbz#875777 and http://code.google.com/p/snakeyaml/issues/detail?id=175
#
# Remove use of bundled Base64 implementation
Patch0:           0001-Replace-bundled-base64-implementation.patch
# We don't have gdata-java in Fedora any longer, use commons-codec instead
Patch1:           0002-Replace-bundled-gdata-java-client-classes-with-commo.patch
# Fix tests on Java 8 (can be removed if version > 1.13)
Patch2:           java8-use-linked-hashmap.patch

BuildArch:        noarch

BuildRequires:  %{?scl_prefix_java_common}maven-local
BuildRequires:  %{?scl_prefix_java_common}mvn(asm:asm)
BuildRequires:  %{?scl_prefix}mvn(biz.source_code:base64coder)
BuildRequires:  %{?scl_prefix_java_common}mvn(commons-codec:commons-codec)
BuildRequires:  %{?scl_prefix_maven}mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  %{?scl_prefix_maven}mvn(org.apache.maven.plugins:maven-site-plugin)
BuildRequires:  %{?scl_prefix_maven}mvn(org.apache.maven.plugins:maven-source-plugin)

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
This package contains %{summary}.

%prep
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%setup -q -n %{pkg_name}-%{vertag}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%mvn_file : %{pkg_name}

%pom_remove_plugin org.codehaus.mojo:cobertura-maven-plugin
%pom_remove_plugin :maven-changes-plugin
%pom_remove_plugin :maven-license-plugin
%pom_remove_plugin :maven-javadoc-plugin

sed -i "/<artifactId>spring</s/spring/&-core/" pom.xml
rm -f src/test/java/examples/SpringTest.java

# Replacement for bundled gdata-java-client
%pom_add_dep commons-codec:commons-codec

# remove bundled stuff
rm -rf target
rm -rf src/main/java/org/yaml/snakeyaml/external

# convert CR+LF to LF
sed -i 's/\r//g' LICENSE.txt

%pom_xpath_remove "pom:dependency[pom:scope[text()='test']]"
%{?scl:EOF}


%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_build -f
%{?scl:EOF}


%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_install
%{?scl:EOF}


%files -f .mfiles
%doc LICENSE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%changelog
* Thu Jul 09 2015 Mat Booth <mat.booth@redhat.com> - 1.13-9.1
- Import latest from Fedora

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Apr 21 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.13-8
- Remove maven-javadoc-plugin from POM

* Tue Mar 31 2015 Michael Simacek <msimacek@redhat.com> - 1.13-7
- Remove BR on maven-changes-plugin

* Wed Mar 25 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.13-6
- Remove build dependency on cobertura

* Wed Mar 11 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.13-5
- Add BR on objectweb-asm3

* Wed Jan 21 2015 Mat Booth <mat.booth@redhat.com> - 1.13-4
- Add missing BR on maven-site-plugin

* Mon Jun 16 2014 Michal Srb <msrb@redhat.com> - 1.13-3
- Fix FTBFS

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Sep 30 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.13-1
- Update to upstream version 1.13

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 21 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.11-6
- Update to current packaging guidelines

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
