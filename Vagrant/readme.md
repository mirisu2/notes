- [Resolving a problem](https://askubuntu.com/questions/900118/vboxdrv-sh-failed-modprobe-vboxdrv-failed-please-use-dmesg-to-find-out-why)
- [getting-started](https://learn.hashicorp.com/tutorials/vagrant/getting-started-index?in=vagrant/getting-started)
- [Docs](https://www.vagrantup.com/docs/index)
## Instalation
```
1. download from https://www.vagrantup.com/downloads zip archive.
2. unpack it and copy to /usr/bin/
3. Check version:
   $ vagrant version
4. Vagrant provides the ability to autocomplete commands
   $ vagrant autocomplete install --bash --zsh

```

*By default, Vagrant shares your project directory (the one containing the Vagrantfile) to the /vagrant directory in your guest machine.*
## Vagrant ENV:
- VAGRANT_ALIAS_FILE [click me](https://www.vagrantup.com/docs/cli/aliases)
- VAGRANT_DEFAULT_PROVIDER

## VAGRANT CLI:
```
vagrant autocomplete install --bash
sudo vagrant destroy --force && sudo vagrant up
vagrant status
vagrant ssh node1
vagrant ssh node2

sudo vagrant global-status
sudo vagrant destroy d688e4a
vagrant init hashicorp/bionic64
vagrant up
vagrant up --provider=docker|vmware_desktop|
vagrant reload --provision
vagrant reload
vagrant suspend
	vagrant up
	*Suspending the virtual machine will stop it and save its current running state.
vagrant halt
	vagrant up
	*Halting the virtual machine will gracefully shut down the guest operating system and power down the guest machine. 
vagrant destroy

vagrant snapshot
	push
	pop
	save
	restore
	list
	delete

vagrant share
	The share command initializes a Vagrant Share session, allowing you to share your Vagrant environment with anyone in the world, enabling 
	collaboration directly in your Vagrant environment in almost any network environment.
	https://www.vagrantup.com/docs/cli/share
```
## Vagrant box catalog [click me](https://app.vagrantup.com/boxes/search)
```
vagrant box add hashicorp/bionic64
vagrant box list
vagrant box remove hashicorp/bionic64
vagrant box remove hashicorp/bionic64 --provider vmware_desktop
vagrant box outdated --forced
vagrant box prune
	This command removes old versions of installed boxes. If the box is currently in use vagrant will ask for confirmation.
	--dry-run
	--provider NAME
	--force [--keep-active-boxes]
	--name NAME
vagrant box remove NAME
	This command removes a box from Vagrant that matches the given name.

vagrant plugin list
vagrant plugin install vagrant-vmware-desktop
vagrant plugin install vagrant-share
	https://learn.hashicorp.com/tutorials/vagrant/getting-started-share?in=vagrant/getting-started
vagrant plugin uninstall vagrant-vmware-desktop
```

When you run any `vagrant` command, Vagrant climbs up the directory tree looking for the first Vagrantfile it can find, starting first in 
the current directory. So if you run `vagrant` in `/home/mitchellh/projects/foo`, it will search the following paths in order for a Vagrantfile, 
until it finds one:
```
/home/mitchellh/projects/foo/Vagrantfile
/home/mitchellh/projects/Vagrantfile
/home/mitchellh/Vagrantfile
/home/Vagrantfile
/Vagrantfile
```

`You can change the starting directory where Vagrant looks for a Vagrantfile by setting the VAGRANT_CWD environmental variable to some other path.`

#### from book
```

https://atlas.hashicorp.com/
https://atlas.hashicorp.com/boxes/search
export VAGRANT_HOME=/some/shared/directory #~/.vagrant.d
VAGRANT_FORCE_COLOR
VAGRANT_LOG # "debug," "info," "warn," and "error." 
VAGRANT_VAGRANTFILE # Vargantfile
VAGRANTFILE_API_VERSION = "2"

$ vagrant status
$ vagrant global-status
$ vagrant up
$ vagrant halt
$ vagrant suspend
$ vagrant destroy
$ vagrant reload

vagrant init -m ubuntu/trusty32
puppetlabs/centos-7.0-64-nocm
hashicorp/precise64
ubuntu/trusty32
chef/centos-6.5

VAGRANTFILE_API_VERSION = "2"
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty32"
end

Vagrant.configure(2) do |config|
  config.vm.box = "http://boxes.gajdaw.pl/sinatra/sinatra-v1.0.0.box"
  config.vm.network :forwarded_port, guest: 4567, host: 45670, host_ip: "127.0.0.1"
end

config.vm.box = "/net/drive/mounted/first-box-jekyll.box"


config.vm.synced_folder [HOST-PATH], [GUEST-PATH]
config.vm.synced_folder "/dir/on/host/Mac/or/Linux", "/dir/on/guest/ubuntu"

ssh-keygen -t rsa -C johnny@example.net -f johhny
config.ssh.private_key_path = "/path/to/the/key/johnny"
vagrant reload

$ vagrant package --output first-box-jekyll.box
* When run without any parameters, the command creates a file named package.box
$ vagrant box repackage first-box-jekyll
$ vagrant box help
$ vagrant package help
vagrant box add first-box-jekyll first-box-jekyll.box
vagrant box list

$ vagrant up --provision
$ vagrant up --no-provision
$ vagrant up --provision-with x, y, z
```

