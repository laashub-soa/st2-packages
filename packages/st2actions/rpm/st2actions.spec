%define package st2actions
%include ../rpmspec/st2pkg_toptags.spec

Summary: st2actions - StackStorm actions component
Requires: st2common = %{version}-%{release}

%description
  <insert long description, indented with spaces>

%install
  %default_install
  %pip_install_venv

  # systemd service file
  mkdir -p %{buildroot}%{_unitdir}
  install -m0644 %{SOURCE0}/rpm/st2actionrunner.service %{buildroot}%{_unitdir}/st2actionrunner.service
  install -m0644 %{SOURCE0}/rpm/st2actionrunner@.service %{buildroot}%{_unitdir}/st2actionrunner@.service
  install -m0644 %{SOURCE0}/rpm/st2notifier.service %{buildroot}%{_unitdir}/st2notifier.service
  install -m0644 %{SOURCE0}/rpm/st2resultstracker.service %{buildroot}%{_unitdir}/st2resultstracker.service
  make post_install DESTDIR=%{?buildroot}

%prep
  rm -rf %{buildroot}
  mkdir -p %{buildroot}

%clean
  rm -rf %{buildroot}

%post
  %systemd_post st2actionrunner st2actionrunner@ st2notifier st2resultstracker
  systemctl --no-reload enable st2actionrunner st2notifier st2resultstracker >/dev/null 2>&1 || :

%preun
  %systemd_preun st2actionrunner st2actionrunner@ st2notifier st2resultstracker

%postun
  %systemd_postun

%files
  %{_datadir}/python/%{name}
  %config(noreplace) %{_sysconfdir}/st2/*
  %{_unitdir}/st2actionrunner.service
  %{_unitdir}/st2actionrunner@.service
  %{_unitdir}/st2notifier.service
  %{_unitdir}/st2resultstracker.service