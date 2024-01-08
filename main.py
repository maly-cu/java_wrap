import time
import json
from datetime import datetime

from jnius import autoclass

from kivy.app import App
from kivy.uix.button import Button
from kivy import platform
from kivy.logger import Logger
from kivy.properties import ObjectProperty
from kivymd.app import MDApp

# Gets the current running instance of the app so as to speak
mActivity = autoclass("org.kivy.android.PythonActivity").mActivity
context = mActivity.getApplicationContext()

# Autoclass necessary java classes so they can be used in python
PythonActivity = autoclass('org.kivy.android.PythonActivity')
TaskScheduler = autoclass('org.test.myapp.TaskScheduler')


class MyApp(App):
    # The only thing this class will need is a build function
    def build(self):
        # create_channel()  # putting it in create_notification funtion to see if it'll work

        button = Button(text="Send Notification",
                        size_hint=(.5, .5),
                        pos_hint={'center_x': .5, 'center_y': .5},
                        background_color='teal',
                        background_normal='')
        button.bind(on_press=self.create_notification)
        return button

    def convert_time_to_millis(time: datetime):
        """Convert a datetime object to time in milliseconds"""
        return int(time.timestamp() * 1000)

    def schedule_alarm(self, task_time, title='Task title', message='Scheduled Task Activity'):
        Logger.debug('App: scheduling todo item')
        if platform == 'android':
            Logger.info('App: scheduling task')

            """
            Schedules a task by calling the schedule task method of the TaskScheduler class
            The task itself is to run a service defined in the buildozer.spec file

            The current activity is passed when initializing the class because it is a
            requirement when using getSystemService() which is required to get the
            alarm manager.
            """
            task_details = {'title': title, 'message': message}
            python_activity = PythonActivity.mActivity

            # task_time = self.convert_time_to_millis(task_time)
            task_time = (time.time_ns() // 1_000_000) + 120_000
            task_scheduler = TaskScheduler(python_activity)
            task_scheduler.scheduleTask(task_time, json.dumps(task_details))
            # import schedule_task
            #
            # schedule_task.schedule_task(self.selected_task_time, title, message)

# # Gets the current running instance of the app so as to speak
# mActivity = autoclass("org.kivy.android.PythonActivity").mActivity
# Reminder_Service = autoclass('org.test.myapp.Reminder_Service')
#
# context = mActivity.getApplicationContext()
# Context = autoclass("android.content.Context")
# Intent = autoclass("android.content.Intent")
# PendingIntent = autoclass("android.app.PendingIntent")
# String = autoclass("java.lang.String")
# Int = autoclass("java.lang.Integer")
# AlarmManager = autoclass('android.app.AlarmManager')
#
#
#
#
#
# class MyApp(App):
#     # The only thing this class will need is a build function
#     def build(self):
#         # create_channel()  # putting it in create_notification funtion to see if it'll work
#
#         button = Button(text="Send Notification",
#                         size_hint=(.5, .5),
#                         pos_hint={'center_x': .5, 'center_y': .5},
#                         background_color='teal',
#                         background_normal='')
#         button.bind(on_press=self.create_notification)
#         return button
#
#     def create_notification(self, instance):  # instance is for the button press done thru python, if kv file, no need
#         print('NOTIFICATION TRIGGERED')
#         intent = Intent()
#         intent.setClass(context, Reminder_Service)
#         # Here change the "org.org.test" to whatever package domain you have set.
#         # Here my buildozer file has the package domain of "org.test".
#         # After that "NOTIFY" is the custom action we have set. This custom action is
#         # also defined in the manifest file(check README file). You can use any name here
#         # just make sure you use the same name while registering the action event
#         intent.setAction("org.org.test.REMIND")
#         # Create a pending intent to be fired later in time by the alarm Manager
#         # Here the intent_id is a variable holding a numeric value that uniquely identifies the
#         # pending intent. Keep this id so that you can cancel scheduled alarms later on.
#
#         # There are various types of pending intent flags that can be set based on what you want.
#         # Here the `FLAG_CANCEL_CURRENT` will cancel any other pending intent with the same id before
#         # setting itself.
#         pending_intent = PendingIntent.getBroadcast(
#             context, 1, intent, PendingIntent.FLAG_UPDATE_CURRENT  # FLAG_CANCEL_CURRENT
#         )
#         # This gets the current system time since epoch in milliseconds(works only in python 3.7+)
#         ring_time = (time.time_ns() // 1_000_000) + 120_000  # plus 2 minutes
#         # We now create the alarm and assign it to the system alarm manager. Some methods assign
#         # an alarm manager instance to a variable and then scheduling a task. But if you need to
#         # later cancel this alarm from another python file or from another launch of your app(as
#         # every time you relaunch a kivy the app ,the code is rerun thus creating a new instance of
#         # the alarm manager rather than the one we used before to schedule the alarm). THIS IS IMPORTANT
#         # AS WE NEED TO USE THE SAME ALARM MANAGER INSTANCE TO CANCEL AN ALARM
#         print(f'Ring time is {ring_time} of type {type(ring_time)}')
#
#         alarm = cast(AlarmManager, context.getSystemService(Context.ALARM_SERVICE))
#         alarm.setExactAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, ring_time, pending_intent)
#         print(f'Cast - {alarm}')
#         # Here we use RTC_WAKEUP which uses the real time of the device to figure out when to fire the alarm


# Finally, we run the app
if __name__ == "__main__":
    MyApp().run()