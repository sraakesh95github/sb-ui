resource "aws_instance" "sb-ui" {
  ami           = "ami-0cf2b4e024cdb6960" # Example AMI ID
  instance_type = "t2.micro"
  key_name = aws_key_pair.deployer.key_name
  vpc_security_group_ids = [aws_security_group.allow_ssh.id]
  iam_instance_profile = aws_iam_instance_profile.ec2_ecr_profile.name
  connection {
    type        = "ssh"
    host        = self.public_ip
    user        = "ubuntu"
    private_key = var.private_key
    timeout = "4m"
  }
  tags = {
    usecase = "ui"
    name = "sb-ui"
  }
}

resource "aws_iam_instance_profile" "ec2_ecr_profile" {
  name = "ec2_ecr_profile"
  role = "ec2-ecr-register"
}

resource "aws_security_group" "allow_ssh" { 
  egress = {
    from_port = 0
    to_port = 0
    protocol = "-1"
    description = "Allow all egress traffic"
    cidr_blocks = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
    prefix_list_ids = []
    protocol = "-1"
    security_groups = []
  }
  ingress = [{
    from_port = 22
    to_port = 22
    protocol = "tcp"
    description = "Allow SSH access"
    cidr_blocks = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
    prefix_list_ids = []
    protocol = "tcp"
    security_groups = []
  },
  {
    from_port = 80
    to_port = 80
    protocol = "tcp"
    description = "Allow HTTP access"
    cidr_blocks = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
    prefix_list_ids = []
    protocol = "tcp"
    security_groups = []
  }]
}

resource "aws_key_pair" "deployer" {
  key_name = var.key_name
  public_key = var.public_key
}

output "instance_public_ip" {
  value = aws_instance.server.public_ip
  sensitive = true
}
