# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.box_check_update = true
  config.vm.network "private_network", ip: "192.168.33.50"
  config.vm.synced_folder ".", "/vagrant"

  config.vm.provision "ansible" do |ansible|
    ansible.groups = {
      "dev" => ["libreeze"]
    }
    ansible.playbook = "provision/site.yml"
  end
end
