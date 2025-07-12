import pulumi
from pulumi_aws import ec2

ami = ec2.get_ami(
    most_recent=True,
    owners=["amazon"],
    filters=[
        {"name": "name", "values": ["amzn2-ami-hvm-*-x86_64-gp2"]},
        {"name": "virtualization-type", "values": ["hvm"]},
    ],
)
server_name = ["appsedr", "sekmdc","dsfjndfff" ]

default_vpc = ec2.get_vpc(default=True)

group = ec2.SecurityGroup(
    "web-secgrp",
    description="Enable SSH & HTTP",
    vpc_id=default_vpc.id,
    ingress=[
        {"protocol": "tcp", "from_port": 22, "to_port": 22, "cidr_blocks": ["0.0.0.0/0"]},
        {"protocol": "tcp", "from_port": 80, "to_port": 80, "cidr_blocks": ["0.0.0.0/0"]},
    ],
)


servers = {}
for name in server_names:
    servers[name] = ec2.Instance(
        f"{name}-server",
        instance_type="t2.micro",
        ami=ami.id,
        vpc_security_group_ids=[group.id],
        tags={"Name": name}
    )

pulumi.export(f"{name}_public_dns", servers[name].public_dns)
pulumi.export(f"{name}_public_ip", servers[name].public_ip)
pulumi.export(f"{name}_ami_id", ami.id)