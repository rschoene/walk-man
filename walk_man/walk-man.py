import pygame

pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag

pygame.init()

pygame.mixer.init()

crouch_sound = pygame.mixer.Sound("../sounds/crouch.wav")
jump_sound = pygame.mixer.Sound("../sounds/jump.wav")
getup_sound = pygame.mixer.Sound("../sounds/getup.wav")
hit_sound = pygame.mixer.Sound("../sounds/hit.wav")

left_sound = pygame.mixer.Sound("../sounds/left.wav")
right_sound = pygame.mixer.Sound("../sounds/right.wav")
back_sound = pygame.mixer.Sound("../sounds/backward.wav")
forward_sound = pygame.mixer.Sound("../sounds/forward.wav")

def main():
    # Set the width and height of the screen (width, height), and name the window.
    screen = pygame.display.set_mode((100, 100))
    pygame.display.set_caption("Joystick example")

    # Used to manage how fast the screen updates.
    clock = pygame.time.Clock()


    # This dict can be left as-is, since pygame will generate a
    # pygame.JOYDEVICEADDED event for every joystick connected
    # at the start of the program.
    joysticks = {}

    # Sounds for buttons
    button_actions = {
        0 : jump_sound, # 0 is A under Windows
        2 : hit_sound, # 2 is X under Windows
    }
    # Sounds looped on button
    button_loop_actions = {
        1 : [crouch_sound,getup_sound], # 1 is B under Windows
    }
    

    done = False
    while not done:
        # Event processing step.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True  # Flag that we are done so we exit this loop.

            if event.type == pygame.JOYBUTTONDOWN:
                print("Joystick button pressed.", event.button)
                for action in button_actions:
                    if action == event.button:
                        if button_actions[action].get_num_channels() == 0:
                            button_actions[action].play()

                for action in button_loop_actions:
                    if action == event.button:
                        if button_loop_actions[action][0].get_num_channels() == 0:
                            button_loop_actions[action][0].play(loops=-1)

            if event.type == pygame.JOYBUTTONUP:
                print("Joystick button released.", event.button)
                for action in button_loop_actions:
                    if action == event.button:
                         button_loop_actions[action][0].stop()
                         button_loop_actions[action][1].play()

            # Handle hotplugging
            if event.type == pygame.JOYDEVICEADDED:
                # This event will be generated when the program starts for every
                # joystick, filling up the list without needing to create them manually.
                joy = pygame.joystick.Joystick(event.device_index)
                joysticks[joy.get_instance_id()] = joy
                print(f"Joystick {joy.get_instance_id()} connencted")

            if event.type == pygame.JOYDEVICEREMOVED:
                del joysticks[event.instance_id]
                print(f"Joystick {event.instance_id} disconnected")

        # For each joystick:
        for joystick in joysticks.values():

            axes = joystick.get_numaxes()

            # we are only interested in axis 0 and 1 (left stick)
            # 2,3 would be right stick and 4,5 would be LT/RT
            for i in [0,1]:
                axis = joystick.get_axis(i)
                #if (axis > 0.5 or axis < -0.5): # and (i == 0 or i == 1) :
                #    print("axis ",i,axis)
                if i == 0:
                    if axis > 0.5:
                        if right_sound.get_num_channels() == 0:
                            right_sound.play()
                    if axis < -0.5:
                        if left_sound.get_num_channels() == 0:
                            left_sound.play()
                if i == 1:
                    if axis > 0.5:
                        if back_sound.get_num_channels() == 0:
                            back_sound.play()
                    if axis < -0.5:
                        if forward_sound.get_num_channels() == 0:
                            forward_sound.play()


            hats = joystick.get_numhats()
            for hat_nr in range(1):
                x, y = joystick.get_hat(hat_nr)
                #print('hat',hat_nr,x,y)
                if x == -1:
                    if left_sound.get_num_channels() == 0:
                        left_sound.play()
                if x == 1:
                        if right_sound.get_num_channels() == 0:
                            right_sound.play()
                if y == -1:
                        if back_sound.get_num_channels() == 0:
                            back_sound.play()
                if y == 1:
                        if forward_sound.get_num_channels() == 0:
                            forward_sound.play()
                    
                
        # Limit to 60 frames per second.
        clock.tick(60)


if __name__ == "__main__":
    main()
    pygame.quit()
