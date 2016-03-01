#!-*- coding=utf-8 -*-

import user
import sql
import irc

def check(buffer, msg, i, s):
    u_info = msg[0]
    i_msg = buffer[buffer.find(buffer.split()[3])+1:]
    spker = user.user()
    spker.l_name = u_info[1:u_info.find("!")]
    spker.n_name = u_info[(u_info.find("!")+2):u_info.find("@")]
    if "[enter]#" in buffer:
        j_ch = buffer[buffer.find("[enter]")+7:].split()[0]
        i.join(j_ch)
        with s:
            s.insert_channel(j_ch)
    if "[exit]#" in buffer:
        e_ch = buffer[buffer.find("[exit]")+6:]
        i.part(e_ch)
    with s:
        s.insert_channel(msg[2])
        s.insert_log(spker.l_name, msg[1], msg[2], i_msg)
