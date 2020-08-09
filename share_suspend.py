import time
from global_vars import get_ss_holder, get_cnl, get_loco, set_ss_holder
from helper import *

def share_suspend(cp, prev_list):
    com_name_list = get_cnl()
    list_of_companies = get_loco()
    choice = cp.recv(512).decode('utf-8')
    if choice != str(0):
        company = com_name_list[int(choice) - 1]
        if company.company_owner:
            company.company_owner.player_connection.send(str.encode("RC {}".format(company.company_name)))
            choice = company.company_owner.player_connection.recv(512).decode('utf-8')
            if choice == "Y":
                company.company_current_price = list_of_companies[company.company_name]
                return 1
            else:
                company.company_current_price = prev_list[company.company_name]
                list_of_companies[company.company_name] = prev_list[company.company_name]
                broadcast("{} share suspended".format(company.company_name))
                return 1
        else:
            company.company_current_price = prev_list[company.company_name]
            list_of_companies[company.company_name] = prev_list[company.company_name]
            return 1
    else:
        return 0

def share_suspend_check(prev_list):
    share_suspend_holder = get_ss_holder()
    if share_suspend_holder:
        share_suspend_holder.player_connection.send(str.encode('suspend'))
        time.sleep(1)
        share_suspend(share_suspend_holder.player_connection, prev_list)
        set_ss_holder(None)