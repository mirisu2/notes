[Переменные](https://ansible-for-network-engineers.readthedocs.io/ru/latest/book/02_playbook_basics/variables.html)  
Docs » User Guide » Working with command line tools » [ansible-playbook](https://docs.ansible.com/ansible/latest/cli/ansible-playbook.html)  
Docs » User Guide » Working with playbooks » Templating (Jinja2) » [Using filters to manipulate data](https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html)
```
ansible all -i kubernetes_inventory.yml -m shell -a 'timedatectl set-time 2021-01-26 15:30:00'
ansible all -i kubernetes_inventory.yml -m shell -a 'timedatectl set-time 15:30:00'
```
#### Проверка форматирования YAML
```
pip3 install yamllint
yamllint hosts.yaml
```
#### [Ansible-lint](https://github.com/ansible/ansible-lint) checks playbooks for practices and behaviour that could potentially be improved.
```
pip3 install ansible-lint
ansible-lint vmware_guest_create.yaml
```
#### Проверка синтаксиса сценария. Запуск сценария в тестовом режиме.
```
ansible-playbook –i inventory <playbook_path> --check-syntax
ansible-playbook –i inventory <playbook_path> --check
```
## Install ansible
```
pip3 install ansible
vim .bashrc
export ANSIBLE_HOST_KEY_CHECKING=False
export PATH=$PATH:/home/user/.local/bin
```
## Installing argcomplete with pip
```pip3 install argcomplete```
## Configuring argcomplete
```activate-global-python-argcomplete```

## Check version and installation
```
ansible --version
ansible 2.9.6
  config file = None
```

1. ANSIBLE_CONFIG (environment variable)
2. ansible.cfg (per directory)
3. ~/.ansible.cfg (home directory)
4. /etc/ansible/ansible.cfg (global)
```
cat ansible.cfg
[defaults]
inventory = $HOME/hosts
log_path = ansible.log

ansible all --list-hosts
ansible webservers --list-hosts
```
## List of available modules using:
```ansible-doc -l```

## Documentation for each module can be found at [url](http://docs.ansible.com/ansible/latest/modules_by_category.html)
## You can find out what arguments the copy module requires using:
```ansible-doc copy

ansible staging_ALL -m setup #сбор информации о хостах
ansible vm2 -m setup #сбор информации о хосте
```
> Ansible is not primarily used to run ad hoc commands against hosts. 
> It is designed to run “playbooks.” Playbooks are YAML files that describe “tasks.”
> In more complex settings, instead of listing tasks in the playbooks, these will be delegated to roles.
```
ansible-doc -l #show modules
ansible --version
ansible localhost -m ping
ansible all -m ping
ansible all -m shell -a "uptime"
ansible staging_ALL -m copy -a "src=/home/user1/copyMe.txt dest=/var/www/ mode=755" -b #-b стать суперпользователем
ansible staging_ALL -m file -a "path=/home/user1/copyMe.txt state=absent" -b #удалить файл
ansible staging_ALL -m get_url -a "url=http://server.com/file.txt dest=/home/user1/" -b
ansible staging_ALL -m yum/apt -a "name=stress state=latest" -b #latest/installed/removed
ansible staging_ALL -m uri -a "url=http://www.server.com returm_content=yes"
ansible staging_ALL -m service -a "name=httpd state=started enabled=yes" -b

$ ansible-playbook playbook.yml --list-hosts
$ ansible app -b -a "service ntpd restart" --limit "192.168.60.4"
$ ansible-playbook playbook.yml --limit webservers
$ ansible-playbook playbook.yml --limit xyz.example.com
$ ansible-playbook playbook.yml --become --become-user=janedoe --ask-become-pass
$ ansible-playbook playbook.yml -i inventory/staging
$ ansible-playbook playbook.yml -i inventory/production

--forks=NUM (-f NUM)
--extra-vars=VARS
-v -vv -vvv -vvvv #debuging
-a MODULE_ARGS
-h, --help
-m MODULE_NAME
-i INVENTORY
--inventory=PATH (-i PATH)
--syntax-check #Perform a syntax check on the playbook, but do not execute it
-u REMOTE_USER

ansible-inventory --list
ansible-inventory --graph
```
## Ansible Vault [url1](https://www.youtube.com/watch?v=20g9BNilDvg&list=PLg5SS_4L6LYufspdPupdynbMQTBnZd31N) [url2](https://docs.ansible.com/ansible/latest/user_guide/vault.html)
```
ansible-vault create foo.yml
ansible-vault encrypt foo.yml bar.yml baz.yml
ansible-vault decrypt foo.yml bar.yml baz.yml
ansible-vault view foo.yml bar.yml baz.yml
ansible-vault edit foo.yml
ansible-vault rekey foo.yml bar.yml baz.yml
ansible-vault encrypt_string
ansible-playbook pb_deploy-vm-from-template.yaml --extra-vars 'vm_number=118' --ask-vault-pass
ansible-playbook pb_deploy-vm-from-template.yaml --extra-vars 'vm_number=119' --vault-password-file .secret
ansible-playbook pb_deploy_nodejs_app.yaml --limit 192.168.198.120 --tags install_pm2
ansible-playbook pb_deploy-vm.yaml --extra-vars 'vm_number=120' --skip-tags 'create_vm,powerup_vm,sleep'
```
## [Conditionals](https://docs.ansible.com/ansible/latest/user_guide/playbooks_conditionals.html)
```
ansible-playbook example.yml --tags "configuration,packages"
ansible-playbook example.yml --skip-tags "packages"
```

Another special tag is `never`, which will prevent a task from running unless a tag is specifically requested.
### Example:
```
tasks:
  - debug: msg="{{ showmevar }}"
    tags: [ never, debug ]
```
In this example, the task will only run when the `debug` or `never` tag is explicitly requested.
There are another 3 special keywords for tags: `tagged`, `untagged` and `all`, which run only tagged, only untagged and all tasks respectively.
> By default, Ansible runs as if `--tags all` had been specified.

## How variables are merged:
* all group (because it is the ‘parent’ of all other groups)
* parent group
* child group
* host

## The order of precedence from least to greatest (the last listed variables winning prioritization):
* command line values (eg “-u user”)
* role defaults [1]
* inventory file or script group vars [2]
* inventory group_vars/all [3]
* playbook group_vars/all [3]
* inventory group_vars/* [3]
* playbook group_vars/* [3]
* inventory file or script host vars [2]
* inventory host_vars/* [3]
* playbook host_vars/* [3]
* host facts / cached set_facts [4]
* play vars
* play vars_prompt
* play vars_files
* role vars (defined in role/vars/main.yml)
* block vars (only for tasks in block)
* task vars (only for the task)
* include_vars
* set_facts / registered vars
* role (and include_role) params
* include params
* extra vars (always win precedence)

## [Roles](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html#playbooks-reuse-roles)
* **tasks** - contains the main list of tasks to be executed by the role.
* **handlers** - contains handlers, which may be used by this role or even anywhere outside this role.
* **defaults** - default variables for the role (see Using Variables for more information).
* **vars** - other variables for the role (see Using Variables for more information).
* **files** - contains files which can be deployed via this role.
* **templates** - contains templates which can be deployed via this role.
* **meta** - defines some meta data for this role. See below for more details.

## [inventory parameters](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#connecting-to-hosts-behavioral-inventory-parameters)
