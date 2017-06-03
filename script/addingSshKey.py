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
        print "The script missing parameter: [script name] [ec2 name]"


# The function installs the public key in a remote machine's authorized_keys.
def update_public_key(hostname):
    try:
        os.system("ssh-copy-id " + hostname)
    except Exception as e:
        print e.message
    print "authorized_keys updated for " + hostname + "."


if __name__ == '__main__':

    # checking if the input is valid.
    argv_validation()

    # getting the ec2 name.
    ec2_name = sys.argv[1]

    # getting the instances list of the EC2.
    conn = boto.ec2.connect_to_region(ec2_name)
    reservations = conn.get_all_instances()
    for res in reservations:
        for inst in res.instances:
            if 'Name' in inst.tags:
                # print "%s (%s) [%s]" % (inst.tags['Name'], inst.id, inst.state)
                currentServer = inst.tags['Name']
                update_public_key(currentServer)
    print "Done"
