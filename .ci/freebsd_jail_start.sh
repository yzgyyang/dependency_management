#!/bin/sh -x

ezjail-admin delete -w -f gitlab || true
ezjail-admin create gitlab 'lo1|192.168.0.2'
echo 'nameserver 8.8.8.8' >> /usr/jails/gitlab/etc/resolv.conf
echo 'nameserver 8.8.4.4' >> /usr/jails/gitlab/etc/resolv.conf
echo 'hostname="runner_jail"' >> /usr/jails/gitlab/etc/rc.conf
ezjail-admin start gitlab
jail -m name=gitlab allow.raw_sockets=1
