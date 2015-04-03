# load base manifest
import "base.pp"

node default inherits base {
  package {"sendmail":
      ensure => installed,
  }

  package {"supervisor":
      ensure => installed,
  }
  service { "supervisor":
    ensure => running,
    enable => true,
    require => Package['supervisor'],
  }

  file { "/etc/supervisor/conf.d/website.conf":
    ensure => present,
    source => "/var/www/app/manifests/resources/supervisor_website.conf",
    require => [Package['supervisor'],File['/etc/uwsgi.xml']],
    notify => Service["supervisor"]
  }

  package {"nginx":
      ensure => installed,
  }
  service { "nginx":
    ensure => running,
    enable => true,
    require => Package['nginx'],
  }

  file { "/etc/nginx/sites-enabled/default":
      require => Package["nginx"],
      ensure  => absent,
      notify  => Service["nginx"]
  }

  file { "/etc/nginx/sites-enabled/app.conf":
    ensure => present,
    source => "/var/www/app/manifests/resources/nginx_app.conf",
    require => [Package['nginx'],File['/etc/supervisor/conf.d/website.conf']],
    notify => Service["nginx"]
  }

  file { "/etc/nginx/sites-enabled/admin.conf":
    ensure => present,
    source => "/var/www/app/manifests/resources/nginx_admin.conf",
    require => [Package['nginx'],File['/etc/supervisor/conf.d/website.conf']],
    notify => Service["nginx"]
  }

  file { "/etc/nginx/sites-enabled/api.conf":
    ensure => present,
    source => "/var/www/app/manifests/resources/nginx_api.conf",
    require => [Package['nginx'],File['/etc/supervisor/conf.d/website.conf']],
    notify => Service["nginx"]
  }

  package { "uwsgi":
    ensure => present,
    provider => "pip"
  }

  file { "/etc/uwsgi.xml":
    ensure => present,
    source => "/var/www/app/manifests/resources/uwsgi.xml",
    require => Package['uwsgi'],
    notify => Service["supervisor"]
  }
}
