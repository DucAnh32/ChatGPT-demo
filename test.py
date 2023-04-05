import pandas as pd
import re
def get_list_idx(s,c):
    idxs = [pos for pos, char in enumerate(s) if char == c]
    return idxs


idxs=[pos for pos, char in enumerate(s) if char == ',']
for idx in idxs:
    open_bra_before=get_list_idx(s[0:idx],'(')
    close_bra_before = get_list_idx(s[0:idx], ')')
    open_bra_after = get_list_idx(s[idx:], '(')
    close_bra_after = get_list_idx(s[idx:], ')')
    subtract_before=abs(len(open_bra_before)-len(close_bra_before))
    subtract_after=abs(len(open_bra_after) - len(close_bra_after))
    if subtract_before==0:
        continue
    elif subtract_after==subtract_before:
        s=s[:idx] + s[idx+1:]
