Vagrant.configure("2") do |config|
  config.vm.define "srv-infrastructure-elastic-master-01", autostart: true do |elastic|
    elastic.vm.box = "bento/ubuntu-22.04"
    elastic.vm.hostname = 'srv-infrastructure-elastic-master-01'

    elastic.vm.network "public_network", use_dhcp_assigned_default_route: true, bridge: "enp7s0", ip: "172.21.5.161"
    elastic.vm.synced_folder "/work/", "/work"
    elastic.vm.provider :virtualbox do |v|
        v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
        v.customize ["modifyvm", :id, "--memory", 1024]
        v.customize ["modifyvm", :id, "--name", "srv-infrastructure-elastic-master-01"]
    end
  end
end

