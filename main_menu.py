from time import sleep

sequence = [0,1,2,3]
sequence[0] = ("M5","BlueButton","Slider","Plug","Door","Probe-Roll-Stow","RedButton")
sequence[1] = ("M5","BlueButton","Slider","Door","Plug","Probe-Roll-Stow","RedButton")
sequence[2] = ("M5","BlueButton","RedButton","Slider","Door","Plug","Probe-Roll-Stow")
sequence[3] = ("M5","RedButton","BlueButton","Slider","Plug","Door","Probe-Roll-Stow")

    
# ==== main actions

valid_answer = 0

print("=============================================")
print("Welcome to Robothon 2023, RoboTechX MDX Dubai")
print("=============================================")
print("Options of sequence:")

while not valid_answer:
    selection = 0
    for seq in sequence:
        print(selection, end = ": ")
        for action in seq:
            print(action, end = " > ")
        print("Finish")
        selection = selection + 1
    
    prompt = "Enter sequence to execute (0 - " + str(selection - 1) + ") : "
    answer = int(input(prompt))
    if (0 <= answer <= 3):
        valid_answer = 1
        print ("You choose ", end = ": ")
        break

for action in sequence[answer]:
    print(action, end = " > ")
print("Finish")
sleep(1)
print("Connecting to camera, Arduino, EPSON...")
sleep(0.5)
print("Acquiring task board coordinate...")
sleep(0.5)
for action in sequence[answer]:
    print("Executing:", action)
    sleep(0.5)
print("Finished")

# m5()
# bb()
# slide(cam)
# plug()
# door()
# probe()
# cable()
# stow()
# rb()
