%define name novnc-config
%define version 1.0
%define unmangled_version 1.0
%define unmangled_version 1.0
%define release 1
%define pkg_name novnc-for-vcenter

Summary: Just for vcenter novnc console.
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{pkg_name}-%{unmangled_version}.tar.gz
License: CertuseNet
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Hongquan Zhu <zhuhq@certusnet.com.cn>

%description
UNKNOWN

%prep
%setup -n %{pkg_name}-%{unmangled_version} -n %{pkg_name}-%{unmangled_version}

%build
python setup.py build

%install
cp -r etc $RPM_BUILD_ROOT
cp -r usr $RPM_BUILD_ROOT
chmod 0755 $RPM_BUILD_ROOT/usr/bin/novnc-bin

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-,root,root)
/etc/contrail/novnc.conf
/usr/bin/novnc-bin
/usr/lib/systemd/system/novnc-proxy.service
/usr/share/novnc/*
