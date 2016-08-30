from falafel.mappers.secure import Secure
from falafel.tests import context_wrap

MSGINFO = """
Aug 24 09:31:39 localhost polkitd[822]: Loading rules from directory /etc/polkit-1/rules.d
Aug 24 09:31:39 localhost polkitd[822]: Loading rules from directory /usr/share/polkit-1/rules.d
Aug 24 09:31:39 localhost polkitd[822]: Finished loading, compiling and executing 6 rules
Aug 24 09:31:39 localhost polkitd[822]: Acquired the name org.freedesktop.PolicyKit1 on the system bus
Aug 25 13:52:54 localhost sshd[23085]: pam_unix(sshd:session): session opened for user zjj by (uid=0)
Aug 25 13:52:54 localhost sshd[23085]: error: openpty: No such file or directory
Aug 25 13:52:54 localhost sshd[23089]: error: session_pty_req: session 0 alloc failed
Aug 25 14:04:04 localhost sshd[23089]: Received disconnect from 10.66.192.100: 11: disconnected by user
Aug 25 14:04:04 localhost sshd[23085]: pam_unix(sshd:session): session closed for user zjj
""".strip()

Secure.filters.extend([
    "polkitd",
    "sshd"
])


def test_secure():
    msg_info = Secure.parse_context(context_wrap(MSGINFO))
    ssh_list = msg_info.get('sshd')
    assert 5 == len(ssh_list)
    assert ssh_list[0].get('timestamp') == "Aug 25 13:52:54"
    assert ssh_list[4].get('timestamp') == "Aug 25 14:04:04"
    polkitd = msg_info.get('Loading rules from directory')
    assert 2 == len(polkitd)
    assert polkitd[0].get('procname') == "polkitd[822]"
    assert polkitd[1].get(
        'raw_message') == "Aug 24 09:31:39 localhost polkitd[822]: Loading rules from directory /usr/share/polkit-1/rules.d"
    assert polkitd[1].get('message') == "Loading rules from directory /usr/share/polkit-1/rules.d"
    assert polkitd[1].get('hostname') == "localhost"
