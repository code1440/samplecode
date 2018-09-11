- name: create ec2 instances
  hosts: localhost
  connection: local
  gather_facts: false
  tasks:

    - name: provision instances
      ec2:
        key_name: devbox
        group: launch-wizard-4
        region: us-east-1
        instance_type: t2.micro
        image: ami-0c54494f920b19106
        #exact_count: 1
        count_tag:
          Name: autospin
        instance_tags:
          Name: autospin
      register: ec2

    # - name: Wait for SSH to come up
    #   delegate_to: "{{ item.private_dns_name }}"
    #   wait_for_connection:
    #     delay: 30
    #     timeout: 320
    #   with_items: "{{ ec2.instances }}"

    - pause:
        minutes: 1

    - name: create hostlist
      add_host:
        hostname: "{{ item.private_dns_name }}"
        groupname: ubulaunched
        ansible_ssh_user: ubuntu
      with_items: "{{ ec2.instances }}"

- name: install
  hosts: ubulaunched
  become: True
  roles:
    - tomcat
    
