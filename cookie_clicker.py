"""
Cookie Clicker Simulator
"""

import simpleplot

# Used to increase the timeout, if necessary
import codeskulptor
import math
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME =  10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """

    def __init__(self):
        self._tot_number = 0.0
        self._cur_number = 0.0
        self._cur_time = 0.0
        self._cur_cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]

    def __str__(self):
        """
        Return human readable state
        """
        state = "\n"
        state +=  "TOTAL: " + str(self._tot_number) + "\n"
        state += "CURRENT: " + str(self._cur_number) + "\n"
        state += "TIME: " + str(self._cur_time) + "\n"
        state += "CPS: " + str(self._cur_cps) + "\n"
        return state

    def get_cookies(self):
        """
        Return current number of cookies
        (not total number of cookies)

        Should return a float
        """
        return self._cur_number

    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cur_cps

    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._cur_time

    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: (0.0, None, 0.0, 0.0)
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if self._cur_number > cookies:
            return 0.0
        else:
            difference = cookies - self._cur_number
            time = difference / self._cur_cps
            return math.ceil(time)

    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0
        """
        if time <= 0:
            return
        else:
            self._cur_time += time
            self._cur_number += (self._cur_cps * time)
            self._tot_number += (self._cur_cps * time)

    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._cur_number < cost:
            pass
        else:
            self._cur_cps += additional_cps
            self._cur_number -= cost
            history_item = (self._cur_time, item_name, cost, self._tot_number)
            self._history.append(history_item)


def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to game.
    """
    new_build_info = build_info.clone()
    clicker = ClickerState()
    while clicker.get_time() <= duration:
        cookies = clicker.get_cookies()
        cps = clicker.get_cps()
        time = clicker.get_time()
        _cur_time = clicker.get_time()
        item = strategy(cookies, cps, duration - time, new_build_info)
        if (item == None):
            clicker.wait(duration-_cur_time)
            break
        cost = new_build_info.get_cost(item)
        time_until = clicker.time_until(cost)
        if  time_until + _cur_time > duration:
            clicker.wait(duration-_cur_time)
            break
        else:
            clicker.wait(time_until)
            clicker.buy_item(item, cost, new_build_info.get_cps(item))
            new_build_info.update_item(item)
    return clicker

def strategy_cursor(cookies, cps, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic strategy does not properly check whether
    it can actually buy a Cursor in the time left.  Your strategy
    functions must do this and return None rather than an item you
    can't buy in the time left.
    """
    return "Cursor"

def strategy_none(cookies, cps, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that you can use to help debug
    your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, time_left, build_info):
    """
    Docstring
    """
    items = build_info.build_items()
    item_to_buy = None
    mini = SIM_TIME
    for item in items:
        cost = build_info.get_cost(item)
        if cost < mini:
            mini = cost
            item_to_buy = item
    cost2 = build_info.get_cost(item_to_buy)
    money = cookies + time_left * cps
    if cost2 > money:
        return None
    else:
        return item_to_buy

def strategy_expensive(cookies, cps, time_left, build_info):
    """
    Docstrings
    """
    items = build_info.build_items()
    item_to_buy = None
    maxi = -1
    money = cookies + cps * time_left
    for item in items:
        cost = build_info.get_cost(item)
        if cost <= money and cost > maxi:
            item_to_buy = item
            maxi = cost
    if item_to_buy == None:
        return None
    return item_to_buy

def strategy_best(cookies, cps, time_left, build_info):
    """
    Docstring
    """
    items = build_info.build_items()
    money2 = cookies + cps * time_left * 0.07
    ratio = 1
    res = {}
    for item in items:
        cost = build_info.get_cost(item)
        cps = build_info.get_cps(item)
        ratio = cost/cps
        if cost <= money2:
            res[item] = ratio
    if res == []:
        return None
    else:
        return get_best_cps_2(res, build_info)

def get_best_cps_2(items, build_info):
    """
    Docstring
    """
    ratio = 0.0
    best_ratio_item = None
    for key in items.keys():
        _ratio = items[key]
        if _ratio > ratio:
            if best_ratio_item != None:
                cost_bri = build_info.get_cost(best_ratio_item)
                cost_k = build_info.get_cost(key)
                if cost_k > cost_bri * 180:
                    continue
                else:
                    ratio = _ratio
                    best_ratio_item = key
            else:
                ratio = _ratio
                best_ratio_item = key
    return best_ratio_item

def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation with one strategy
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    history = state.get_history()
    history = [(item[0], item[3]) for item in history]
    #simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """
    #run_strategy("Cursor", SIM_TIME, strategy_cursor)
    run_strategy("Best", SIM_TIME, strategy_best)

run()
#import user34_GhjnBEJSmI_10 as test_suite
#test_suite.run_simulate_clicker_tests(simulate_clicker,strategy_none,strategy_cursor)
#test_suite.run_clicker_state_tests(ClickerState)

#import user34_1yyodNweJj_0 as init_test
#init_test.run_test(ClickerState)

#import user34_gwOBYcB0vg_5 as wait_test
#wait_test.run_test(ClickerState)

#import user34_JegqHUeyeq_1 as time_until_test
#time_until_test.run_test(ClickerState)

#import user34_CX25TCXsrD_4 as buy_test
#buy_test.run_test(ClickerState)

#import user34_rjdKnsYfB9_2 as testsuite
#testsuite.run_tests(ClickerState, simulate_clicker,strategy_cursor, strategy_cheap, strategy_expensive, strategy_best)
