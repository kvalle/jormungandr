# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.hostname = "ormebol"

  config.vm.provision "shell", inline: <<-SCRIPT
    sudo apt-get update

    sudo apt-get install python-pip -y
    sudo pip install flake8

    sudo pip install PyYAML
    sudo apt-get install git -y
    git clone https://github.com/kvalle/dotfiles.git
SCRIPT

  # config.vm.network "forwarded_port", guest: 4321, host: 4321
  # config.vm.network "forwarded_port", guest: 8000, host: 8000
  config.vm.synced_folder "", "/home/vagrant/orm"
end
