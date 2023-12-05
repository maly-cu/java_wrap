import time
from jnius import autoclass, cast
from kivy.app import App
from kivy.lang import Builder
from kivy.utils import platform
from kivy.logger import Logger


if platform == 'android':
    Intent = autoclass('android.content.Intent')
    KivyAlarmReceiver = autoclass('org.kivy.android.KivyAlarmReceiver')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    mActivity = PythonActivity.mActivity
    Intent = autoclass('android.content.Intent')
    AlarmManager = autoclass('android.app.AlarmManager')
    PendingIntent = autoclass('android.app.PendingIntent')
    Context = autoclass('android.content.Context')


KV = """
FloatLayout:
    TextInput:
        id: t
        pos_hint: {'center': (.5, .65)}
        size_hint: .3, .05
        filter: int
    Label:
        pos_hint: {'center': (.5, .6)}
        text: 'after how many minutes should be fired'
    Button:
        pos_hint: {'center': (.3, .45)}
        size_hint: .3, .075
        text: 'schedule alarm'
        on_release: app.start_alarm(t.text)
    Button:
        text: 'stop service'
        pos_hint: {'center': (.7, .45)}
        size_hint: .3, .075
        on_release: app.stop_service()
    Label:
        id: lbl
        pos_hint: {'center': (.5, .35)}
        text: 'kivy alarm manger with service'
"""


class Application(App):

    def build(self):
        return Builder.load_string(KV)

    def start_alarm(self, min):
        try:
            min = int(min)
        except Exception:
            Logger.info('Not a valid number: Minutes set to 1')
            min = 1
        context = mActivity.getApplicationContext()
        alarmSetTime = int(round(time.time() * 1000)) + 1000 * 60 * int(min)
        alarmIntent = Intent()
        alarmIntent.setClass(context, KivyAlarmReceiver)
        alarmIntent.setAction("org.kivy.android.ACTION_START_ALARM")
        pendingIntent = PendingIntent.getBroadcast(
            context, 18, alarmIntent, PendingIntent.FLAG_UPDATE_CURRENT)
        alarm = cast(
            AlarmManager, context.getSystemService(Context.ALARM_SERVICE))
        alarm.setExactAndAllowWhileIdle(
            AlarmManager.RTC_WAKEUP, alarmSetTime, pendingIntent)

    def stop_service(self):
        mActivity.stop_service()


if __name__ == "__main__":
    app = Application()
    app.run()
# from jnius import autoclass, cast
# from kivy.app import App
# from kivy.uix.button import Button
# import time
#
# # # Gets the current running instance of the app so as to speak
# # mActivity = autoclass("org.kivy.android.PythonActivity").mActivity
# # context = mActivity.getApplicationContext()
# #
# #
# # # Autoclass necessary java classes so they can be used in python
# # RingtoneManager = autoclass("android.media.RingtoneManager")
# # Uri = autoclass("android.net.Uri")
# # AudioAttributesBuilder = autoclass("android.media.AudioAttributes$Builder")
# # AudioAttributes = autoclass("android.media.AudioAttributes")
# # AndroidString = autoclass("java.lang.String")
# # NotificationManager = autoclass("android.app.NotificationManager")
# # NotificationChannel = autoclass("android.app.NotificationChannel")
# # NotificationCompat = autoclass("androidx.core.app.NotificationCompat")
# # NotificationCompatBuilder = autoclass("androidx.core.app.NotificationCompat$Builder")
# # NotificationManagerCompat = autoclass("androidx.core.app.NotificationManagerCompat")
# # func_from = getattr(NotificationManagerCompat, "from")
# #
# # # Unique id for a notification channel. Is used to send notification through
# # # this channel
# # channel_id = AndroidString("Scream_Channel")
# #
# #
# # def create_notification(instance):
# #     pass
# #
# #
# #
# #     def create_channel(self):
# #         print("Creating Channel now")
# #         # create an object that represents the sound type of the notification
# #         sound = cast(Uri, RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION))
# #         att = AudioAttributesBuilder()
# #         att.setUsage(AudioAttributes.USAGE_NOTIFICATION)
# #         att.setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION)
# #         att = cast(AudioAttributes, att.build())
# #
# #         # Name of the notification channel
# #         name = cast("java.lang.CharSequence", AndroidString("Scream"))
# #         # Description for the notification channel
# #         description = AndroidString("Sends reminder for user to reapply sunscreen")
# #
# #         # Importance level of the channel
# #         importance = NotificationManager.IMPORTANCE_HIGH
# #
# #         # Create Notification Channel
# #         channel = NotificationChannel(channel_id, name, importance)
# #         channel.setDescription(description)
# #         channel.enableLights(True)
# #         channel.enableVibration(True)
# #         channel.setSound(sound, att)
# #         # Get android's notification manager
# #         notificationManager = context.getSystemService(NotificationManager)
# #         # Register the notification channel
# #         notificationManager.createNotificationChannel(channel)
# #
# #
# #     def create_notification(self, instance): # instance is for the button press done through python, if in kv file, no need
# #
# #         self.create_channel()
# #
# #         print("Sending Notification")
# #         # Set notification sound
# #         sound = cast(Uri, RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION))
# #         # Create the notification builder object
# #         builder = NotificationCompatBuilder(context, channel_id)
# #         # Sets the small icon of the notification
# #         builder.setSmallIcon(context.getApplicationInfo().icon)
# #         # Sets the title of the notification
# #         builder.setContentTitle(
# #             cast("java.lang.CharSequence", AndroidString("Notification Title"))
# #         )
# #         # Set text of notification
# #         builder.setContentText(
# #             cast("java.lang.CharSequence", AndroidString("Notification text"))
# #         )
# #         # Set sound
# #         builder.setSound(sound)
# #         # Set priority level of notification
# #         builder.setPriority(NotificationCompat.PRIORITY_HIGH)
# #         # If notification is visble to all users on lockscreen
# #         builder.setVisibility(NotificationCompat.VISIBILITY_PUBLIC)
# #
# #         # Create a notificationcompat manager object to add the new notification
# #         compatmanager = NotificationManagerCompat.func_from(context)
# #         # Pass an unique notification_id. This can be used to access the notification
# #         # _______________________ NOTIFICATION ID - "scream_1" _________________________
# #         compatmanager.notify("scream_1", builder.build())
#
#
# # Gets the current running instance of the app so as to speak
# mActivity = autoclass("org.kivy.android.PythonActivity").mActivity
# Reminder_Service = autoclass('org.org.myapp.Reminder_Service')
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
#         alarm = cast(
#             AlarmManager, context.getSystemService(Context.ALARM_SERVICE)
#         ).setExactAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, ring_time, pending_intent)
#         print(f'Cast - {alarm}')
#         # Here we use RTC_WAKEUP which uses the real time of the device to figure out when to fire the alarm
#
#
# # Finally, we run the app
# if __name__ == "__main__":
#     MyApp().run()
