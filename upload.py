#!/usr/bin/python
import os
from pygithub3 import Github
from pygithub3.services.repos import Downloads

repo_user_name = 'heat-api'
repo_name = 'prebuilt-jeos-images'

jeos_names = ('F16-x86_64-cfntools-jeos',
              'F16-i386-cfntools-jeos',
              'F17-x86_64-cfntools-jeos',
              'F17-i386-cfntools-jeos',
              'U10-x86_64-cfntools-jeos')

gh = Github(login='PUT_YOUR_GITHUB_NAME_HERE', password='PUT_YOUR_PASSWORD_HERE')

upload_dicts=[]
for jeos_name in jeos_names:
    try: 
        filename = '/var/lib/libvirt/images/%s.qcow2' % jeos_name
        statinfo = os.stat(filename)
        size = statinfo.st_size
        upload_dicts.append(dict(name='%s.qcow2' % jeos_name, size='%d' % size,
                            filename=filename))
    except:
        print "Can't find file '%s' to upload to github." % filename

print "Uploading files to github user '%s' repo '%s'" % (repo_user_name, repo_name)
for upload_dict in upload_dicts:
    # Delete an existing upload
    files = gh.repos.downloads.list(user=repo_user_name, repo=repo_name).all()
    for file in files:
        if file.name == upload_dict["name"]:
            print 'Deleting existing upload %s' % upload_dict["name"]
            gh.repos.downloads.delete(id=file.id, user=repo_user_name,
                repo=repo_name)
            break

    print 'Uploading file %s - size %d mb' % (upload_dict["name"],
           int(upload_dict["size"]) / (1024*1024))
    download = gh.repos.downloads.create(upload_dict, user=repo_user_name,
                                          repo=repo_name)
    download.upload(upload_dict["filename"])
