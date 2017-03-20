import boto, time, os

access_key    = os.environ['AWS_ACCESS_KEY']
secret_key    = os.environ['AWS_SECRET_ACCESS_KEY']
keypair_name  = 'mydemokey'

user_data = """#!/bin/bash
# Install saltstack
curl -L http://bootstrap.saltstack.org | sudo sh -s -- -M stable

echo '''### This is controlled by the hosts file
master: localhost
id: localhost
file_roots:
  base:
    - /srv/salt/states
log_file: /var/log/salt/minion
log_level: debug
log_level_logfile: garbage
''' > /etc/salt/minion

# Set salt master location and start minion
sed -i 's/#master: salt/master: localhost/' /etc/salt/minion
salt-minion -d
  """

conn  = boto.connect_ec2(access_key, secret_key)
try:
  key   = conn.create_key_pair(keypair_name)
  key.save("./")
except:
  True # Key already created

group_name = "quickstart"
try:
  groups = [g for g in conn.get_all_security_groups() if g.name == group_name]
  group = groups[0] if groups else None
  if not group:
    group = conn.create_security_group(group_name, "A group for %s"%(group_name,))
  group.authorize(ip_protocol='tcp',
                  from_port=str(22),
                  to_port=str(22),
                  cidr_ip='0.0.0.0/0')
  group.authorize(ip_protocol='tcp',
                  from_port=str(80),
                  to_port=str(80),
                  cidr_ip='0.0.0.0/0')
except:
  True

reservation = conn.run_instances(image_id='ami-0cdf4965',
                                 key_name=keypair_name,
                                 security_groups=[group_name],
                                 user_data=user_data)

running_instance = reservation.instances[0]
status = running_instance.update()
while status == 'pending':
    time.sleep(10)
    status = running_instance.update()
print(running_instance.ip_address)
