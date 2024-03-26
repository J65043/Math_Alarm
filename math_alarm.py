import random
from time import sleep
import asyncio
from win11toast import toast
from winsdk.windows.ui.notifications.management import UserNotificationListener, UserNotificationListenerAccessStatus
from winsdk.windows.foundation.metadata import ApiInformation

NUM_PROBLEMS = 3

def generate_problem():
    num1, num2 = random.randint(1, 10), random.randint(1, 10)
    operator = random.choice(['+', '-', '*', '/'])

    if operator == '/':
        while num1 % num2 != 0:
            num1, num2 = random.randint(1, 10), random.randint(1, 10)

    question = f"{num1} {operator} {num2}"
    return question, eval(question)

def solve_to_dismiss():
    while True:
        questions, answers, user_inputs = [], [], []

        for _ in range(NUM_PROBLEMS):
            question, answer = generate_problem()
            questions.append(question)
            answers.append(answer)

        problems_str = "\n".join([f"{idx + 1}. {q} = ?" for idx, q in enumerate(questions)])
        response = toast('Solve these math problems to dismiss', problems_str, input='Your answers (comma separated)', button='Submit')

        if response:
            user_input_str = response.get('user_input', {}).get('Your answers (comma separated)', '')
            try:
                user_inputs = list(map(float, user_input_str.split(',')))
                if len(user_inputs) != NUM_PROBLEMS:
                    print("You must provide all answers, separated by commas.")
                    continue
            except ValueError:
                print("Invalid input, try again.")
                continue

            if all(a == b for a, b in zip(user_inputs, answers)):
                print("Congratulations! You solved all the problems correctly.")
                break
            else:
                print("Incorrect! Starting over.")
                sleep(1)

def dismiss_and_resend_notification(listener, target_app_name, notification):
    if hasattr(notification, 'app_info') and notification.app_info.display_info.display_name == target_app_name:
        listener.remove_notification(notification.id)
        solve_to_dismiss()

async def main():
    if not ApiInformation.is_type_present("Windows.UI.Notifications.Management.UserNotificationListener"):
        print("UserNotificationListener is not supported on this device.")
        exit()

    listener = UserNotificationListener.current
    access_status = await listener.request_access_async()

    if access_status != UserNotificationListenerAccessStatus.ALLOWED:
        print("Access to UserNotificationListener is not allowed.")
        print("To enable Access go to Settings in Windows, Go to Privacy & Security , then Go to notifications, then check Notification Access and let apps access your notifications ")
        exit()
    else:
        print("Access status allowed")

    def handler(listener, event):
        notification = listener.get_notification(event.user_notification_id)
        change_kind = event.change_kind
        #print(f"ChangeKind: {change_kind}")

        if change_kind == 1 and hasattr(notification, "app_info"):
            app_name = notification.app_info.display_info.display_name
            print("App Name:", app_name)
            print("ID", notification.id)
            dismiss_and_resend_notification(listener, "Clock", notification)

    listener.add_notification_changed(handler)

    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())