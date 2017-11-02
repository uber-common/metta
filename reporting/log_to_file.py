#logging from https://gist.github.com/ColinDuquesnoy/8296508

#: HTML header (starts the document


_START_OF_DOC_FMT = """<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>%(title)s</title>
<style type="text/css">
body, html {
background: #000000;
width: 1500px;
font-family: Arial;
font-size: 16px;
color: #C0C0C0;
}
h1 {
color : #FFFFFF;
border-bottom : 1px dotted #888888;
}
pre {
font-family : arial;
margin : 0;
}
.box {
border : 1px dotted #818286;
padding : 5px;
margin: 5px;
width: 1300px;
background-color : #292929;
}
.err {
color: #EE1100;
font-weight: bold
}
.warn {
color: #FFCC00;
font-weight: bold
}
.info {
color: #C0C0C0;
}
.debug {
color: #CCA0A0;
}
</style>
</head>
<body>
<h1>%(title)s</h1>
<h3>%(version)s</h3>
<div class="box">
<table>
<tr>
<th>Time</th>
<th>Rule Name</th>
<th>Action</th>
<th>Mitre Phase</th>
<th>Mitre Technique</th>
<th>Host</th>
</tr>
"""

_END_OF_DOC_FMT = """</table>
</div>
</body>
</html>
"""

_MSG_FMT = """

<tr align="center">
<td>%(time)s</td>
<td>%(rule_name)s</td>
<td>%(action)s</td>
<td>%(mitre_phase)s</td>
<td>%(mitre_tech)s</td>
<td>%(host)s</td>
<tr>
"""



def start_log(title, version):
    # Write header
    f = open("log.html","w+")
    f.write(_START_OF_DOC_FMT % {"title": title, "version": version})
    f.close()

def close_log():
    # finish document
    f = open("log.html","a+")
    f.write(_END_OF_DOC_FMT)
    f.close()

def write_row(time, rule_name, action, mitre_phase, mitre_tech, host):
	f = open("log.html","a+")
	f.write(_MSG_FMT % {"time": time, "action": action, "rule_name": rule_name, "mitre_phase": mitre_phase, "mitre_tech":mitre_tech, "host":host})
	f.close()
