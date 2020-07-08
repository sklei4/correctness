#!/usr/bin/env python3
import subprocess

def apply(__option__, __logging__):
    """
    Applies an action based on set.
    If basic, verifies the basic rules.
    If enterprise, verifies that.
    If custom, verifies those rules.
    Returns False or True based on success.
    """
    if __logging__ > 0:
        __LOGGING__ == __logging__
    if __option__ == "BASIC":
        return verify_rule_set(__BASIC__)
    if __option__ == "ENTERPRISE":
        return verify_rule_set(__ENTERPRISE__)
    if __option__ == "CUSTOM":
        return verify_rule_set(__CUSTOM__)

def execute_control(__controls__):
    """
    Accepts a set of verified rules.
    Parses for known verbs.
    Runs verb against subject and predicate.
    Uses action to determine pass result.
    Returns result or error.
    """
    __verb__ = __controls__['verb']
    __subject__ = __controls__['subject']
    __predicate__ = __controls__['predicate']
    __action__ = __controls__['action']
    if __verb__ == 'check':
        if execute_grep(__subject__, __predicate__):
            return True
        else:
            if (__LOGGING__ > 1):
                print("   Check failed.")
            return False
    if __verb__ == 'find directory':
        if execute_find(__subject__, __predicate__, __directory__):
             return True
        else:
            if (__LOGGING__ > 1):
                print("   Find directory failed.")
            return False
    if __verb__ == 'find file':
        if execute_find(__subject__, __predicate__, __file__):
             return True
        else:
            if (__LOGGING__ > 1):
                print("   Find file failed.")
            return False
    else:
        if (__LOGGING__ > 1):
                print("   No matches found for verb.")
        return False ## Default if no matches found for verb.

def execute_find(__file__, __phrase__, __location__):
    """
    Tries to find as a shell process.
    Checks if you are finding a directory or file.
    Returns True if result found.
    Returns False if result cannot be found.
    Returns error if something wrong happens.
    """
    try:
        print('Obviously this needs to be written yet.')
    except:
        return False
    
def execute_grep(__file__, __phrase__):
    """
    Tries to grep as a shell process.
    Returns True if result found.
    Returns False if result cannot be found.
    Returns error if something wrong happens.
    """
    try:
        if (__LOGGING__ > 2):
            print("   * Executing: grep " + __phrase__ + " " + __file__)
        subprocess.run(['grep', __phrase__, __file__],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            check=True,
            text=True)
        return True
    except:
        if (__LOGGING__ > 1):
           print("   Grep result could not be found.")
        return False
    
def parse_rule(__line__):
    """
    Reads a line from a file.
    Output is the dictionary rule set.
    """
    __list__ = ['rule', 'verb', 'subject', 'predicate', 'action']
    __rules__ = {}
    for i, __word__ in enumerate(__list__):
        try:
            __rules__[__word__] = __line__.split(';%/')[i].rstrip()
        except:
            __rules__[__word__] = ""
        finally:
            i += 1
    return __rules__

def read_status(__file__):
    """
    Checks configuration file.
    Configuration determines what rule set should be used.
    """
    try:
        with open(__file__, "r"  ) as __config__:
            __current__ = __config__.read()
        __config__.close()
        return __current__.rstrip()
    except:
        print('Critical: configuration file missing.')
        exit()

def verify_rule_set(__ruleset__):
    """
    Accepts a ruleset.
    Output is that the rule passes or fails.
    Returns False if one error detected.
    Returns True if no errors detected.
    """
    __result__ = True
    with open(__ruleset__, "r") as __rules__:
        for __line__ in __rules__:
            __set__ = parse_rule(__line__)
            if (verify_rules(__set__) <= 0):
                if (__LOGGING__ > 1):
                    print("Checking: " + __set__['rule'])
                if execute_control(__set__):
                    if (__LOGGING__ > 1):
                        print('   ' + __set__['rule'] + ' passed.')
                    else:
                        print(__set__['rule'] + ' passed.')
                else:
                    __result__ = False
                    if (__LOGGING__ > 1):
                        print('   ' + __set__['rule'] + ' failed.')
                    else:
                        print(__set__['rule'] + ' failed.')
                    if (__LOGGING__ > 0):
                        if (verify_rules(__set__) > 0):
                            print("   " + verify_rules(__set__))
                        if (execute_control(__set__) == False):
                            print("   Result of verified rule is negative.")
    return __result__

def verify_rules(__rules__):
    """
    Verifies rule set can be executed.
    If return value is > 0, it is an invalid set.
    Common Errors:
        1: Unexpected result. Report issue.
        2: This line is the checksum line.
        3: Somehow value of rule equals boolean False.
        4: There is no rule in this line.
    """
    try:
        for __rule__ in __rules__:
            if "#CORRECTNESS_CHECKSUM:" in __rules__[__rule__]: 
                return 2
        if not __rules__['rule']:
            if __rules__['rule'] == "":
                return 4
            else:
                return 3
        if __rules__['rule'] == "":
            return 4
    except:
        return 1
    return 0

# Constants
__CONFIGURATIONFILE__ = "correctness.config"
__ENTERPRISE__ = "enterprise.rules"
__BASIC__ = "basic.rules"
__CUSTOM__ = "custom.rules"
__LOGGING__ = 0


