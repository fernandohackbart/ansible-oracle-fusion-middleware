# Oracle Fusion Middleware 12.2 installation and configuration

This playbook is aimed to support the installtion of the Oracle Fusion Middleware 12.2 over the Linux technical standard 4.0.

## Usage:
* In the case the download is required the variables should defined in the group variables
  * mediassource: "webserver"
  * mediasurl : 'https://medias.xpto.com/pub/omid'

## Documentation reference:

* **Oracle Weblogic**, this module is developed based on the Oracle documentation available at 

* **Ansible**
  * http://docs.ansible.com/ansible/template_module.html
  * http://docs.ansible.com/ansible/shell_module.html
  * http://docs.ansible.com/ansible/apt_module.html
  * http://docs.ansible.com/ansible/expect_module.html
  * http://docs.ansible.com/ansible/fail_module.html
  * http://docs.ansible.com/ansible/yum_module.html
  * http://docs.ansible.com/ansible/intro_inventory.html

* Define variables by environment
  * https://www.digitalocean.com/community/tutorials/how-to-manage-multistage-environments-with-ansible
  
* Encrypt passwords
  * https://gist.github.com/tristanfisher/e5a306144a637dc739e7
  * https://www.digitalocean.com/community/tutorials/how-to-use-vault-to-protect-sensitive-ansible-data-on-ubuntu-16-04

* Check for exaples
