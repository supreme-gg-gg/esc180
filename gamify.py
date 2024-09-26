def initialize():
    '''Initializes the global variables needed for the simulation.
    Note: this function is incomplete, and you may want to modify it'''
    
    global cur_hedons, cur_health

    global cur_time # global timer
    global activity_history

    # Stores when each activity type last finished most recently
    activity_history = {
        "running": [0, 0], # (finish time latest, duration)
        "resting": [0,0],
        "textbooks": [0,0]
    }
    
    global bored_with_stars
    global cur_star, last_star_awarded
    
    cur_hedons = 0
    cur_health = 0
    
    cur_star = {
        "running": False,
        "textbooks": False
    }

    last_star_awarded = []
    
    bored_with_stars = False
    
    cur_time = 0

def star_can_be_taken(activity):
    global cur_star, bored_with_stars
    if cur_star[activity] and not bored_with_stars:
        return True
    
def perform_activity(activity, duration):
    global cur_health, cur_hedons, activity_history
    global cur_time, cur_star, bored_with_stars

    if activity == "resting":
        cur_time += duration
        activity_history[activity] = [cur_time, duration]
        activity_history["running"][1] = 0
        activity_history["textbooks"][1] = 0
        return

    activity_history[activity][1] += duration

    # Handle tireness
    if cur_time == 0:
        is_tired = False
    else:
        last_finished = cur_time - max(activity_history["running"][0], activity_history["textbooks"][0])
        is_tired = False if last_finished >= 120 else True

    # Handle star
    star_pts = 0
    if cur_star[activity] and not bored_with_stars:
        star_pts = 3
        cur_star[activity] = False

    hist_duration = activity_history[activity][1]

    if activity == "running":

        excess = hist_duration - 180

        if hist_duration <= 180:
            cur_health += 3 * duration
        else:
            cur_health += 3 * (duration - excess) + 1 * (excess)
        
        if not is_tired:
            if duration <= 10:
                cur_hedons += 2 * duration
            else:
                cur_hedons += 2 * 10 - 2 * (duration-10)
        else:
            cur_hedons -= 2 * duration

    if activity == "textbooks":

        cur_health += 2 * duration

        if not is_tired:
            if duration <= 20:
                cur_hedons += 1 * duration
            else:
                cur_hedons += 1 * 10 - 1 * (duration-10)
        else:
            cur_hedons -= 2 * duration
    
    if activity_history[activity][1] <= 10:
        cur_hedons += star_pts * duration
    else:
        cur_hedons += star_pts * 10

    cur_time += duration
    activity_history[activity][0] = cur_time

def get_cur_hedons():
    global cur_hedons
    return cur_hedons
    
def get_cur_health():
    global cur_health
    return cur_health
    
def offer_star(activity):
    global cur_star, last_star_awarded, cur_time, bored_with_stars
    cur_star[activity] = True
    last_star_awarded.append(cur_time)
    try:
        if cur_time - last_star_awarded[-3] < 120:
            bored_with_stars = True
    except IndexError:
        return

def most_fun_activity_minute():
    global cur_health, cur_hedons, activity_history
    global cur_time, cur_star, bored_with_stars

    # Handle tireness
    last_finished = cur_time - max(activity_history["running"][0], activity_history["textbooks"][0]) < 120
    is_tired = False if last_finished >= 120 else True

    if (cur_star["running"] and not bored_with_stars):
        return "running" # this means running is 3 + 2
    elif (cur_star["textbooks"] and not bored_with_stars):
        return "textbooks" # 1 + 3 
    elif not is_tired:
        return "running" # if not tired 2 > 1
    else:
        return "resting" # if tired both run and textbook are -2, rest = 0
        
if __name__ == '__main__':
    initialize()
    perform_activity("running", 30)    
    print(get_cur_hedons())            # -20 = 10 * 2 + 20 * (-2)             # Test 1
    print(get_cur_health())            # 90 = 30 * 3                          # Test 2           		
    print(most_fun_activity_minute())  # resting                              # Test 3
    perform_activity("resting", 30)    
    offer_star("running")              
    print(most_fun_activity_minute())  # running                              # Test 4
    perform_activity("textbooks", 30)  
    print(get_cur_health())            # 150 = 90 + 30*2                      # Test 5
    print(get_cur_hedons())            # -80 = -20 + 30 * (-2)                # Test 6
    offer_star("running")
    perform_activity("running", 20)
    print(get_cur_health())            # 210 = 150 + 20 * 3                   # Test 7
    print(get_cur_hedons())            # -90 = -80 + 10 * (3-2) + 10 * (-2)   # Test 8
    perform_activity("running", 170)
    print(get_cur_health())            # 700 = 210 + 160 * 3 + 10 * 1         # Test 9
    print(get_cur_hedons())            # -430 = -90 + 170 * (-2)              # Test 10
