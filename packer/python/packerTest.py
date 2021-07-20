>>> from packerlicious import builder, provisioner, Template
>>> template = Template()
>>> template.add_builder(
        builder.AmazonEbs(
            access_key="...",
            secret_key="...",
            region = "us-east-1",
            source_ami="ami-fce3c696",
            instance_type="t2.micro",
            ssh_username="ubuntu",
            ami_name="packer {{timestamp}}"
        )
    )
<packerlicious.builder.AmazonEbs object at 0x104e87ad0>
>>> template.add_provisioner(
        provisioner.Shell(
            script="setup_things.sh"
        )
    )
<packerlicious.provisioner.Shell object at 0x1048c08d0>
>>> print(template.to_json())
{
  "builders": [
    {
      "access_key": "...",
      "ami_name": "packer {{timestamp}}",
      "instance_type": "t2.micro",
      "region": "us-east-1",
      "secret_key": "...",
      "source_ami": "ami-fce3c696",
      "ssh_username": "ubuntu",
      "type": "amazon-ebs"
    }
  ],
  "provisioners": [
    {
      "script": "setup_things.sh",
      "type": "shell"
    }
  ]
}