"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow
from math import trunc


#  You MUST provide the following two functions
#  with these signatures. You must keep
#  these signatures even if you don't use all the
#  same arguments.
#

ending_close_times = {
   200: 13.5,
   300: 20,
   400: 27,
   600: 40,
   1000: 75
}


def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
   """
   Args:
      control_dist_km:  number, control distance in kilometers
      brevet_dist_km: number, nominal distance of the brevet
         in kilometers, which must be one of 200, 300, 400, 600,
         or 1000 (the only official ACP brevet distances)
      brevet_start_time:  An arrow object
   Returns:
      An arrow object indicating the control open time.
      This will be in the same time zone as the brevet start time.
   """
   if control_dist_km == 0:
      # the starting point opens at the starting time
      return brevet_start_time

   if 0 < control_dist_km <= 200:
      # checkpoint open times between 0 and 200km are calc with max speed 34
      shift_hours = control_dist_km / 34
      shift_minutes = round((shift_hours - trunc(shift_hours)) * 60)
      return brevet_start_time.shift(hours=shift_hours, minutes=shift_minutes)

   if 200 < control_dist_km <= 400:
      # checkpoint open times between 200 and 400km are calc with max speed 32
      shift_hours = (200 / 34) + ((control_dist_km - 200) / 32)
      shift_minutes = round((shift_hours - trunc(shift_hours)) * 60)
      return brevet_start_time.shift(hours=trunc(shift_hours), minutes=shift_minutes)

   if 400 < control_dist_km <= 600:
      # checkpoint open times between 400 and 600km are calc with max speed 30
      shift_hours = (200 / 34) + (200 / 32) + ((control_dist_km - 400) / 30)
      shift_minutes = round((shift_hours - trunc(shift_hours)) * 60)
      return brevet_start_time.shift(hours=trunc(shift_hours), minutes=shift_minutes)

   if 600 < control_dist_km <= 1000:
      # checkpoint open times between 600 and 1000km are calc with max speed 28
      shift_hours = (200 / 34) + (200 / 32) + (200 / 30) + ((control_dist_km - 600) / 28)
      shift_minutes = round((shift_hours - trunc(shift_hours)) * 60)
      return brevet_start_time.shift(hours=trunc(shift_hours), minutes=shift_minutes)

   if 1000 < control_dist_km <= 1300:
      # checkpoint open times bwteen 1k and 1300km are calc with max speed 26
      shift_hours = (200 / 34) + (200 / 32) + (200 / 30) + (400 / 28) + ((control_dist_km - 1000) / 26)
      shift_minutes = round((shift_hours - trunc(shift_hours)) * 60)
      return brevet_start_time.shift(hours=trunc(shift_hours), minutes=shift_minutes)


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
   """
   Args:
      control_dist_km:  number, control distance in kilometers
         brevet_dist_km: number, nominal distance of the brevet
         in kilometers, which must be one of 200, 300, 400, 600, or 1000
         (the only official ACP brevet distances)
      brevet_start_time:  An arrow object
   Returns:
      An arrow object indicating the control close time.
      This will be in the same time zone as the brevet start time.
   """
   if control_dist_km < 60:
      # if (checkpoint) distance is smaller than 60km, close time
      # calculation is control_dist_km / 20 + 1hr
      shift_hours = (control_dist_km / 20) + 1
      shift_minutes = round((shift_hours - trunc(shift_hours)) * 60)
      return brevet_start_time.shift(hours=trunc(shift_hours), minutes=shift_minutes)

   if control_dist_km == brevet_dist_km:
      # if the checkpoint is the finish line, the closing time is
      # hardcoded in ending_close_times.

      # shift brevet_start_time by ending_close_times[control_dist_km]
      shift_hours = ending_close_times[control_dist_km]
      shift_minutes = round((shift_hours - trunc(shift_hours)) * 60)
      return brevet_start_time.shift(hours=trunc(shift_hours), minutes=shift_minutes)

   if 60 <= control_dist_km:
      # normal calculation
      if control_dist_km <= 600:
         # close times between 60 and 600km are calculated with min speed 15
         shift_hours = control_dist_km / 15
         shift_minutes = round((shift_hours - trunc(shift_hours)) * 60)
         return brevet_start_time.shift(hours=trunc(shift_hours), minutes=shift_minutes)

      if 600 < control_dist_km <= 1000:
         # close times between 600 and 1000km are calculated with min speed 11.428
         shift_hours = (600 / 15) + ((control_dist_km - 600) / 11.428)
         shift_minutes = round((shift_hours - trunc(shift_hours)) * 60)
         return brevet_start_time.shift(hours=trunc(shift_hours), minutes=shift_minutes)

      if 1000 < control_dist_km <= 1300:
         # close times above 1000km are calculated with min speed 13.333
         shift_hours = (600 / 15) + (400 / 11.428) + ((control_dist_km - 1000) / 13.333)
         shift_minutes = round((shift_hours - trunc(shift_hours)) * 60)
         return brevet_start_time.shift(hours=trunc(shift_hours), minutes=shift_minutes)
