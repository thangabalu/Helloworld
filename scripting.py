import os
import commands

print "just writing hello world"
os.system("echo hello world ")

#using commands to store the output 

output = commands.getoutput("ls")
print output

