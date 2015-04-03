Vagrant::Config.run do |config|
  config.vm.box = "trusty"
  config.vm.box_url = "https://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box"

  config.vm.provision :puppet do |puppet|
    puppet.manifests_path = "manifests"
    puppet.manifest_file  = "dev.pp"
  end

  config.vm.network :hostonly, "33.33.33.10"

  config.vm.share_folder "www", "/var/www/app", "./", :nfs => true
end
