node base {
  # this makes puppet and vagrant shut up about the puppet group
  group { "puppet":
    ensure => "present",
  }

  # Set default paths
  Exec { path => '/usr/bin:/bin:/usr/sbin:/sbin' }

  # make sure the packages are up to date before beginning
  exec { "apt-get update":
    command => "apt-get update"
  }

  # because puppet command are not run sequentially, ensure that packages are
  # up to date before installing before installing packages, services, files, etc.
  Package { require => Exec["apt-get update"] }
  File { require => Exec["apt-get update"] }

  package {
      "build-essential": ensure => installed;
      "python3": ensure => installed;
      "python3-dev": ensure => installed;
      "python3-pip": ensure => installed;
  }

  exec { "python-virtualenv":
    command => "pip3 install virtualenv",
    require => Package["python3-pip"],
  }

  exec { "website-virtualenv":
    command => "virtualenv -p python3 venv",
    cwd => "/var/www/app/website",
    creates => "/var/www/app/website/venv/bin/activate",
    require => Exec["python-virtualenv"],
  }

  exec { "website-dependencies":
    command => "/var/www/app/website/venv/bin/pip install -r requirements.txt",
    cwd => "/var/www/app/website",
    require => [Exec["website-virtualenv"], Package["libmysqlclient-dev"]],
    logoutput => "on_failure",
  }

  $image = ["libtiff4-dev", "libjpeg8-dev", "libjpeg-dev", "zlib1g-dev", "libfreetype6-dev", "liblcms2-dev", "libwebp-dev", "tcl8.5-dev", "tk8.5-dev", "python-tk"]
  package { $image: ensure => "installed" }

  $xml = ["libxml2-dev", "libxslt1-dev"]
  package { $xml: ensure => "installed" }

  package { "libmysqlclient-dev": ensure => installed }
}
