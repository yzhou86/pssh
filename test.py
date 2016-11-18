import pexpect


child = pexpect.spawn("ssh root@10.224.243.20")
index = child.expect(['password:','continue connecting (yes/no)?',pexpect.EOF, pexpect.TIMEOUT])
if index == 0:
    child.sendline("Slim2012")
    child.interact()
elif index == 1:
    child.sendline('yes')
    child.expect(['password:'])
    child.sendline("Slim2012")
    child.interact()
elif index == 2:
    print "error"
    child.close()
elif index == 3:
    print "timeout"

