{% for host in groups['hadoop-servers'] %}
echo "starting ssh configuration in {{hostvars[host].ansible_host}}......"
sshpass -p {{hostvars[host].ansible_ssh_pass}} scp /root/.ssh/id_rsa.pub {{hostvars[host].ansible_ssh_user}}@{{hostvars[host].ansible_host}}:/data/{{ansible_host}}.pub
sshpass -p {{hostvars[host].ansible_ssh_pass}} ssh {{hostvars[host].ansible_ssh_user}}@{{hostvars[host].ansible_host}} "cat /data/{{ansible_host}}.pub >> ~/.ssh/authorized_keys" 

{% endfor %}
