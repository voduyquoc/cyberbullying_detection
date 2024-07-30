## Virtual Machine EC2 SSH Setup

The first few minutes of [this video by Alexey](https://www.youtube.com/watch?v=IXSiYkP23zo) is recommended for understanding how it's done. You can then follow the below steps.

Launch a new EC2 instance. An Ubuntu OS (Ubuntu Server 24.04 LTS (HVM), SSD Volume Type, Architecture 64-bit (x86)) and a t2.micro instance type, a 30Gb gp2 storage are recommended. 

**Note** - Billing will start as soon as the instance is created and run.

Create a new [key pair](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/create-key-pairs.html) so later you can connect to the new instance using SSH.

Save the .pem file in the ~/.ssh directory.

Create a config file in your `.ssh` folder

```bash
code ~/.ssh/config
```

Copy the following snippet and replace with External IP of the Virtual Machine. Username and path to the ssh private key

```bash
Host mlops-zoomcamp
    HostName <ec2_public_ip>
    User ubuntu
    IdentityFile ~/.ssh/<key_pair_name>.pem
    StrictHostKeyChecking no
```

Once you are setup, you can simply SSH into the servers using the below commands in separate terminals. Do not forget to change the IP address of VM restarts.

```bash
ssh mlops-zoomcamp
```

You will have to forward ports from your VM to your local machine for you to be able to see Mage UI. Check how to do that [here](https://youtu.be/ae-CV2KfoN0?t=1074)

## Virtual Machine EC2 SSH Setup

Make sure `make` and `git` are installed on the EC2 instance. If not, install them using the following command:

```bash
sudo apt update
sudo apt install -y make git
```

Clone the repository in your virtual machine.

```bash
git clone https://github.com/voduyquoc/cyberbullying_detection.git && \
cd cyberbullying_detection
```

Install all the tools and dependencies

```bash
make set_up_ec2
```

Configure the AWS CLI using the command `aws configure`. You'll need to provide the `AWS_ACCESS_KEY` and `AWS_SECRET_ACCESS_KEY` along with the `AWS_REGION` and `AWS_OUTPUT_FORMAT` (optional). 
    - AWS Access Key ID [None]: The access key id from IAM 
    - AWS Secret Access Key [None]: The Secret key id from IAM
    - default region name should be the similar format as: `eu-north-1`



#### [Installation Reference - Ankur Chavda](https://github.com/ankurchavda/streamify/blob/main/setup/ssh.md)