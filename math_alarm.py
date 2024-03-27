from winsdk.windows.ui.notifications.management import UserNotificationListener
from winsdk.windows.ui.notifications import KnownNotificationBindings, NotificationKinds
from winsdk.windows.ui.notifications.management import UserNotificationListenerAccessStatus
from winsdk.windows.foundation.metadata import ApiInformation
from winsdk.windows.ui.notifications import ToastNotificationManager
import random
import winsdk.windows.ui.notifications as notifications
import winsdk.windows.data.xml.dom as dom
from time import sleep
import asyncio
from win11toast import toast
import tkinter as tk
from tkinter import filedialog,messagebox
import vlc




def get_file_path():
    messagebox.showinfo("Info","Please Select a Music File")
    root = tk.Tk()
    root.withdraw()
    filepath = filedialog.askopenfilename()
    while not filepath:
            filepath = filedialog.askopenfilename
    return filepath

player = vlc.MediaPlayer(get_file_path())

def generate_problem():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operators = ['+', '-', '*', '/']
    operator = random.choice(operators)

    if operator == '/':
        while num1 % num2 != 0:
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)

    question = f"{num1} {operator} {num2}"
    answer = eval(question)
    return question, answer

def solve_to_dismiss():
    while True:
        questions = []
        answers = []
        user_inputs = []
        player.play()
        for _ in range(3):
            question, answer = generate_problem()
            questions.append(question)
            answers.append(answer)

        problems_str = "\n".join([f"{idx + 1}. {q} = ?" for idx, q in enumerate(questions)])

        response = toast('Solve these math problems to dismiss', problems_str, input='Your answers (comma separated)', button='Submit')

        if response:
            try:
                user_input_str = response.get('user_input', {}).get('Your answers (comma separated)', '')
                user_inputs = list(map(float, user_input_str.split(',')))
                if len(user_inputs) != 3:
                    print("You must provide all 3 answers, separated by commas.")
                    continue
            except ValueError:
                print("Invalid input, try again.")
                continue
            except AttributeError:
                print("notification closed trying again")
                continue

            if all([a == b for a, b in zip(user_inputs, answers)]):
                print("Congratulations! You solved all the problems correctly.")
                break
            else:
                print("Incorrect! Starting over.")
                sleep(1)

def dismiss_and_resend_notification(listener, target_app_name,notification):
    
    print(f"Would dismiss and resend notification for {notification.app_info.display_info.display_name}")
    
 
    if hasattr(notification, 'app_info') and notification.app_info.display_info.display_name == "Clock":
        listener.remove_notification(notification.id)

        #creates a notification that must be solved with math to dismiss.
        solve_to_dismiss()




async def main():
     
    if not ApiInformation.is_type_present("Windows.UI.Notifications.Management.UserNotificationListener"):
        print("UserNotificationListener is not supported on this device.")
        
        exit()


    listener = UserNotificationListener.current
    accessStatus = await listener.request_access_async()

    if accessStatus != UserNotificationListenerAccessStatus.ALLOWED:
        print("Access to UserNotificationListener is not allowed.")
        print("To enable Access go to Settings in Windows, Go to Privacy & Security , then Go to notifications, then check Notification Access and let apps access your notifications ")
        exit()
    else:
        print("Access status allowed")

    def handler(listener, event):
        notification = listener.get_notification(event.user_notification_id)
        #print("Event type:", type(event))
        #print("Event properties:", dir(event))
        
        change_kind = event.change_kind
        print(f"ChangeKind: {change_kind}")
                
        if change_kind == 1:  # Replace 'your_value_for_removed_notification' with the actual value
            print("Notification removed detected")
            is_notification_dismissed_from_app(notification, "Clock")

        if hasattr(notification, "app_info"):
            app_name = notification.app_info.display_info.display_name
            print("App Name: ", notification.app_info.display_info.display_name)
            print("ID", notification.id)
        if(notification.app_info.display_info.display_name == "Clock"):
            dismiss_and_resend_notification(listener, "Clock",notification)
                #listener.remove_notification(notification.id)



    def is_notification_dismissed_from_app(notification, app_name):
        if hasattr(notification, "app_info") and notification.app_info.display_info.display_name == app_name:
            print(f"Notification from {app_name} has been dismissed.")

    listener.add_notification_changed(handler)

    while True:
        await asyncio.sleep(1)  # Sleep for 1 second to prevent high CPU usage

if __name__ == "__main__":
    asyncio.run(main())
