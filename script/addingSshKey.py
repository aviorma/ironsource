#!/bin/python

import boto.ec2
import sys
import os


# This functions check if the input is valid.
def argv_validation():
    try:
        len(sys.argv) == 2
    except ValueError:
        exit(0)
        print "The script has one parameter: [script name] [ec2 name]"


# The function installs the public key in a remote machine's authorized_keys.
# The command ssh-copy-id installs your public key in a remote machine's authorized_keys
def update_public_key(hostname):
    try:
        os.system("ssh-copy-id " + hostname)
    except Exception as e:
        print e.message
    print "authorized_keys updated for " + hostname + "."


def creating_private_key():
    os.system("	ssh-keygen -t rsa -N "" -f my.key")


if __name__ == '__main__':
    # logger of boto,
    boto.set_stream_logger('boto')

    # checking if the input is valid.
    argv_validation()

    # getting the ec2 name.
    ec2_name = sys.argv[1]

    # Creating private key, in case that there is no private in the machine already.
    creating_private_key()

    # getting the instances list of the EC2.
    try:
        conn = boto.ec2.connect_to_region(ec2_name)
        reservations = conn.get_all_instances()
    except boto.exception.NoAuthHandlerFound as e:
        print "boto cannot find credentials to use."
        exit(1)

    for res in reservations:
        for inst in res.instances:
            # if the string includes "Name" so it is a hostname.
            if 'Name' in inst.tags:
                currentServer = inst.tags['Name']

                # we updating the public key file of the server.
                update_public_key(currentServer)
    print "Done"
