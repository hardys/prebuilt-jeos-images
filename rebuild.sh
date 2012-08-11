#!/bin/bash

heat-jeos -y create F16-i386-cfntools-jeos
heat-jeos -y create F16-x86_64-cfntools-jeos
heat-jeos -y create F17-i386-cfntools-jeos
heat-jeos -y create F17-x86_64-cfntools-jeos
heat-jeos -y create U10-x86_64-cfntools-jeos
python upload.py
