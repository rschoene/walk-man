import pygame

pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag

pygame.init()

pygame.mixer.init()

crouch_sound = pygame.mixer.Sound("crouch.wav")
jump_sound = pygame.mixer.Sound("jump.wav")

left_sound = pygame.mixer.Sound("left.wav")
right_sound = pygame.mixer.Sound("right.wav")
back_sound = pygame.mixer.Sound("backward.wav")
forward_sound = pygame.mixer.Sound("forward.wav")

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
        0 : crouch_sound,
        1 : crouch_sound,
        2 : jump_sound,
        3 : jump_sound,
        11 : left_sound,
        12 : right_sound,
        13 : forward_sound,
        14 : back_sound,
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
                            button_actions[action].play(loops=-1)

            if event.type == pygame.JOYBUTTONUP:
                print("Joystick button released.", event.button)
                for action in button_actions:
                    if action == event.button:
                        button_actions[action].stop()

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

            for i in range(axes):
                axis = joystick.get_axis(i)
                if i == 0:
                    if axis > 0.3:
                        if right_sound.get_num_channels() == 0:
                            right_sound.play()
                    if axis < -0.3:
                        if left_sound.get_num_channels() == 0:
                            left_sound.play()
                if i == 1:
                    if axis > 0.3:
                        if back_sound.get_num_channels() == 0:
                            back_sound.play()
                    if axis < -0.3:
                        if forward_sound.get_num_channels() == 0:
                            forward_sound.play()


        # Limit to 120 frames per second.
        clock.tick(120)


if __name__ == "__main__":
    main()
    pygame.quit()
