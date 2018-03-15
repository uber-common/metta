from base64 import b64encode
a = b64encode('Write-Host "Doing Evil stuff here"'.encode('UTF-16LE'))
print(a)
