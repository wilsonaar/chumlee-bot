import re
import time

import dbfunctions
import resources.medalprices
medalprices = resources.medalprices

dealcooldown = 900

def is_valid_userid(id):
    return re.match("<@!?[0-9]*>", id)

def in_cooldown_period(id):
    now = int(time.time())
    lastdeal = dbfunctions.last_deal_time(id)

    return (now - lastdeal) >= dealcooldown

def buy_medal(user, medal):
    medal = str.lower(medal)
    price = medalprices.get_medal_price(medal)
    if price is None:
        return "There isn't a medal called " + medal + "."
    else:
        if dbfunctions.check_for_funds(user.id, price):
            dbfunctions.withdraw(user.id, price)
            dbfunctions.award_medal(user.id, medal)
            return "Alright! Here's a " + medal + " medal for you " + user.mention + "!\n\n" + user.mention + "  :arrow_right:  <:chumcoin:337841443907305473> x" + str(medalprices.get_medal_price(medal)) + "  :arrow_right:  <:chumlee:337842115931537408>"
        else:
            return "You don't have enough Chumcoins for a " + medal + " medal!"
