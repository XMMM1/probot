
Vagrant.configure(2) do |config|
  	config.vm.box = "ubuntu/trusty64"
  	#ubuntu/xenial64
  	config.vm.box_check_update = true
	config.vm.provider :virtualbox do |vb|
	    vb.name = "chatBot"
	    vb.customize ["modifyvm", :id, "--memory", "1024", "--cpus", "1"]
	end
	config.vm.synced_folder "/Volumes/Data/Matej/Dropbox/www/chatBot","/home/vagrant/workspace", create: true
	config.vm.network "private_network", ip: "10.0.0.7"
end