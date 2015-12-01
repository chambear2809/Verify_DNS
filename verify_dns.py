#!/usr/bin/env python
'''
Python 2.7.x only
verify_DNS


Copyright (C) 2015 Cisco Systems Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

'''
__appname__ = 'verify_dns'
__version__ = '1.0.0'
__author__ = 'Alec Chamberlain aleccham@cisco.com>'

import sys
import paramiko
HtmldomainInfo = []
forHtmlString = ""
indent = '   '

class SSH:
    def ssh_Connection(self,apicIP,userID,pw):
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(apicIP,username=userID,password=pw)
 
        except Exception, e:
            print "================================================"
            print 'ERROR: Remote connection failed with %s' % e
            print "================================================"
    ###----------------------------------------------------------------------------------------------------###
    def ssh_Commands(self,cmd):
        DNS = []
        forHtmlString = ""

        try:
            ###-------------------------------------------execute command -----------------------------------###
            stdin, stdout, stderr = self.ssh.exec_command(cmd)
            for line in stdout:               
                print indent+line.strip('\n')
                linez = indent+line.strip('\n')
                forHtmlString += linez+"<br>"

                lineNo = line.split(" ")
                for i in lineNo:
                    if ('.com' in i) or ('.local' in i):
                        DNS.append(i)
#                       print indent+i
#                       linez = indent+i
#                       forHtmlString += linez+"<br>"
                    else:
                        pass
            ###----------------------------------------------- print errors ---------------------------------###
            for line in stderr:
                print indent+line.strip('\n')
                linez = indent+line.strip('\n')
                forHtmlString += linez+"<br>"                                

        except Exception, e:
            print "================================================"
            print 'ERROR: Commands Execution failed with %s' % e
            print "================================================"
        
        return DNS, forHtmlString

    ###-------------------------------------------------------------------------------------------------------###
    def ssh_Commands_ping(self,cmd):
        forHtmlString = ""
        try:
            stdin, stdout, stderr = self.ssh.exec_command(cmd)
            for line in stdout:
                print indent+line.strip('\n')
                linez = indent+line.strip('\n')
                forHtmlString += linez+"<br>"                   

            for line in stderr:
                print indent+line.strip('\n')
                linez = indent+line.strip('\n')
                forHtmlString += linez+"<br>"                   

        except Exception, e:
            print "================================================"
            print 'ERROR: Commands Execution failed with %s' % e
            print "================================================"
        return forHtmlString
###------------------------------------------------------------------------------------------------------------###
def main(apicIP, userID, pw):
    HtmldomainInfo = []
    forHtmlString = ""

    forHtmlString += '<pre>'
    forHtmlString += '<!DOCTYPE>'
    forHtmlString += '<html>'
    forHtmlString += '<body>'
    linez = '<br><b>                 Verifying DNS configuration on APIC'
    forHtmlString += linez+"<br>"
    print   '=========================================================================='
    linez = '=========================================================================='
    forHtmlString += linez+"<br>"+"<br>"
    HtmldomainInfo.append(forHtmlString)
    forHtmlString = ""
    ###------------------------------------------------------------------------------------------------###   
    ssh = SSH()

    ###------------------------------------- Connect to the APIC --------------------------------------###
    ssh.ssh_Connection(apicIP,userID,pw)

    ###------------------------------------------------------------------------------------------------###
    cmd = 'cat /etc/resolv.conf'
    DNS, forHtmlString = ssh.ssh_Commands(cmd)
    HtmldomainInfo.append(forHtmlString)
    forHtmlString = ""
    ###------------------------------------------------------------------------------------------------###
    for i in DNS:
        print   '\n--------------------------------------------------------------------------\n'
        linez = '--------------------------------------------------------------------------'
        forHtmlString += "<br>"+linez+"<br>"+"<br>"

        print indent+'DNS: ' + i
        DNS_name = indent+'DNS: ' + i
        linez = str(DNS_name)
        forHtmlString += linez+"<br>"
           
        cmd = 'ping -c 5 ' + i
        print indent+'ping -c 5 ' + i
        linez = indent+str(cmd)
        forHtmlString += linez+"<br>"
        HtmldomainInfo.append(forHtmlString)
        forHtmlString = ""

        ###----------------------------------------------------------------------------------------------###
        forHtmlString = ssh.ssh_Commands_ping(cmd)
        HtmldomainInfo.append(forHtmlString)
        forHtmlString = ""
        
    ssh.ssh.close()
    
    forHtmlString += '</body>'
    forHtmlString += '</html>'
    forHtmlString += '</pre>'
    HtmldomainInfo.append(forHtmlString)

    return  HtmldomainInfo

if __name__ == "__main__":
    apicIP, userID, pw = '', '',''
    main(sys.argv[1],sys.argv[2],sys.argv[3])
