# Button positions and radius
button_radius = 35
up_button_center = (100, 50)
hover_button_center = (100, 120)
down_button_center = (100, 190)
pause_center = (240, 220)
pause_dimensions = (80, 40)
button_dimensions = (120, 60)




def user_update(x, y, state_counter, paused):
    if pause_center[0] - (pause_dimensions[0]/2) <= x <= pause_center[0] + (pause_dimensions[0]/2) and pause_center[1] - (pause_dimensions[1]/2) <= y <= pause_center[1] + (pause_dimensions[1]/2):
        paused = True
    elif up_button_center[0] - (button_dimensions[0]/2) <= x <= up_button_center[0] + (button_dimensions[0]/2) and up_button_center[1] - (button_dimensions[1]/2) <= y <= up_button_center[1] + (button_dimensions[1]/2):
        state_counter = 1  # Up
        paused = False
        print("Up button pressed!")
    elif hover_button_center[0] - (button_dimensions[0]/2) <= x <= hover_button_center[0] + (button_dimensions[0]/2) and hover_button_center[1] - (button_dimensions[1]/2) <= y <= hover_button_center[1] + (button_dimensions[1]/2):
        state_counter = 0  # Hover
        paused = False
        print("Hover button pressed!")
    elif down_button_center[0] - (button_dimensions[0]/2) <= x <= down_button_center[0] + (button_dimensions[0]/2) and down_button_center[1] - (button_dimensions[1]/2) <= y <= down_button_center[1] + (button_dimensions[1]/2):
        state_counter = 2  # Down
        paused = False
        print("Down button pressed!")

    return state_counter, paused


