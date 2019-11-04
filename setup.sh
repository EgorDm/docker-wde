if ! sudo grep "address=/dev/172.18.18.200" /etc/dnsmasq.conf; then
  sudo sh -c "echo \"address=/dev/172.18.18.200\" >> /etc/dnsmasq.conf"
  sudo systemctl enable dnsmasq.service
fi

if ! sudo grep "nameserver 127.0.0.1" /etc/resolv.conf; then
  sudo sh -c 'echo "$(echo "nameserver 127.0.0.1"; cat /etc/resolv.conf)" > /etc/resolv.conf'
fi
