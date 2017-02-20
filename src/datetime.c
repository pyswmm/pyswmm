//-----------------------------------------------------------------------------
//   datetime.c
//
//   Project:  EPA SWMM5
//   Version:  5.1
//   Date:     03/20/14   (Build 5.1.001)
//   Author:   L. Rossman
//
//   DateTime functions.
//-----------------------------------------------------------------------------
#define _CRT_SECURE_NO_DEPRECATE

#include <math.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include "datetime.h"

// Macro to convert charcter x to upper case
#define UCHAR(x) (((x) >= 'a' && (x) <= 'z') ? ((x)&~32) : (x))

//-----------------------------------------------------------------------------
//  Constants
//-----------------------------------------------------------------------------
static const char* MonthTxt[] =
    {"JAN", "FEB", "MAR", "APR",
     "MAY", "JUN", "JUL", "AUG",
     "SEP", "OCT", "NOV", "DEC"};
static const int DaysPerMonth[2][12] =      // days per month
    {{31, 28, 31, 30, 31, 30,               // normal years
      31, 31, 30, 31, 30, 31},
     {31, 29, 31, 30, 31, 30,               // leap years
      31, 31, 30, 31, 30, 31}};
static const int DateDelta = 693594;        // days since 01/01/00
static const double SecsPerDay = 86400.;    // seconds per day

//-----------------------------------------------------------------------------
//  Shared variables
//-----------------------------------------------------------------------------
static int DateFormat;


//=============================================================================

void divMod(int n, int d, int* result, int* remainder)

//  Input:   n = numerator
//           d = denominator
//  Output:  result = integer part of n/d
//           remainder = remainder of n/d
//  Purpose: finds integer part and remainder of n/d.

{
    if (d == 0)
    {
        *result = 0;
        *remainder = 0;
    }
    else
    {
        *result = n/d;
        *remainder = n - d*(*result);
    }
}

//=============================================================================

int isLeapYear(int year)

//  Input:   year = a year
//  Output:  returns 1 if year is a leap year, 0 if not
//  Purpose: determines if year is a leap year.

{
    if ((year % 4   == 0)
    && ((year % 100 != 0)
    ||  (year % 400 == 0))) return 1;
    else return 0;
}

//=============================================================================

int  datetime_findMonth(char* month)

//  Input:   month = month of year as character string
//  Output:  returns: month of year as a number (1-12)
//  Purpose: finds number (1-12) of month.

{
    int i;
    for (i = 0; i < 12; i++)
    {
        if (UCHAR(month[0]) == MonthTxt[i][0]
        &&  UCHAR(month[1]) == MonthTxt[i][1]
        &&  UCHAR(month[2]) == MonthTxt[i][2]) return i+1;
    }
    return 0;
}

//=============================================================================

DateTime datetime_encodeDate(int year, int month, int day)

//  Input:   year = a year
//           month = a month (1 to 12)
//           day = a day of month
//  Output:  returns encoded value of year-month-day
//  Purpose: encodes year-month-day to a DateTime value.

{
    int i, j;
    i = isLeapYear(year);
    if ((year >= 1)
    && (year <= 9999)
    && (month >= 1)
    && (month <= 12)
    && (day >= 1)
    && (day <= DaysPerMonth[i][month-1]))
    {
        for (j = 0; j < month-1; j++) day += DaysPerMonth[i][j];
        i = year - 1;
        return i*365 + i/4 - i/100 + i/400 + day - DateDelta;
    }
    else return -DateDelta;
}

//=============================================================================

DateTime datetime_encodeTime(int hour, int minute, int second)

//  Input:   hour = hour of day (0-24)
//           minute = minute of hour (0-60)
//           second = seconds of minute (0-60)
//  Output:  returns time encoded as fractional part of a day
//  Purpose: encodes hour:minute:second to a DateTime value

{
    int s;
    if ((hour >= 0)
    && (minute >= 0)
    && (second >= 0))
    {
        s = (hour * 3600 + minute * 60 + second);
        return (double)s/SecsPerDay;
    }
    else return 0.0;
}

//=============================================================================

void datetime_decodeDate(DateTime date, int* year, int* month, int* day)

//  Input:   date = encoded date/time value
//  Output:  year = 4-digit year
//           month = month of year (1-12)
//           day   = day of month
//  Purpose: decodes DateTime value to year-month-day.

{
    int  D1, D4, D100, D400;
    int  y, m, d, i, k, t;

    D1 = 365;              //365
    D4 = D1 * 4 + 1;       //1461
    D100 = D4 * 25 - 1;    //36524
    D400 = D100 * 4 + 1;   //146097

    t = (int)(floor (date)) + DateDelta;
    if (t <= 0)
    {
        *year = 0;
        *month = 1;
        *day = 1;
    }
    else
    {
        t--;
        y = 1;
        while (t >= D400)
        {
            t -= D400;
            y += 400;
        }
        divMod(t, D100, &i, &d);
        if (i == 4)
        {
            i--;
            d += D100;
        }
        y += i*100;
        divMod(d, D4, &i, &d);
        y += i*4;
        divMod(d, D1, &i, &d);
        if (i == 4)
        {
            i--;
            d += D1;
        }
        y += i;
        k = isLeapYear(y);
        m = 1;
        for (;;)
        {
            i = DaysPerMonth[k][m-1];
            if (d < i) break;
            d -= i;
            m++;
        }
        *year = y;
        *month = m;
        *day = d + 1;
    }
}

//=============================================================================

void datetime_decodeTime(DateTime time, int* h, int* m, int* s)

//  Input:   time = decimal fraction of a day
//  Output:  h = hour of day (0-23)
//           m = minute of hour (0-59)
//           s = second of minute (0-59)
//  Purpose: decodes DateTime value to hour:minute:second.

{
    int secs;
    int mins;
    secs = (int)(floor((time - floor(time))*SecsPerDay + 0.5));
    divMod(secs, 60, &mins, s);
    divMod(mins, 60, h, m);
    if ( *h > 23 ) *h = 0;
}

//=============================================================================

void DLLEXPORT datetime_dateToStr(DateTime date, char* s)

//  Input:   date = encoded date/time value
//  Output:  s = formatted date string
//  Purpose: represents DateTime date value as a formatted string.

{
    int  y, m, d;
    char dateStr[DATE_STR_SIZE];
    datetime_decodeDate(date, &y, &m, &d);
    switch (DateFormat)
    {
      case Y_M_D:
        sprintf(dateStr, "%4d-%3s-%02d", y, MonthTxt[m-1], d);
        break;

      case M_D_Y:
        sprintf(dateStr, "%3s-%02d-%4d", MonthTxt[m-1], d, y);
        break;

      default:
        sprintf(dateStr, "%02d-%3s-%4d", d, MonthTxt[m-1], y);
    }
    strcpy(s, dateStr);
}

//=============================================================================

void DLLEXPORT datetime_timeToStr(DateTime time, char* s)

//  Input:   time = decimal fraction of a day
//  Output:  s = time in hr:min:sec format
//  Purpose: represents DateTime time value as a formatted string.

{
    int  hr, min, sec;
    char timeStr[TIME_STR_SIZE];
    datetime_decodeTime(time, &hr, &min, &sec);
    sprintf(timeStr, "%02d:%02d:%02d", hr, min, sec);
    strcpy(s, timeStr);
}

//=============================================================================

int datetime_strToDate(char* s, DateTime* d)

//  Input:   s = date as string
//  Output:  d = encoded date;
//           returns 1 if conversion successful, 0 if not
//  Purpose: converts string date s to DateTime value.
//
{
    int  yr = 0, mon = 0, day = 0, n;
    char month[4];
    char sep1, sep2;
    *d = -DateDelta;
    if (strchr(s, '-') || strchr(s, '/'))
    {
        switch (DateFormat)
        {
          case Y_M_D:
            n = sscanf(s, "%d%c%d%c%d", &yr, &sep1, &mon, &sep2, &day);
            if ( n < 3 )
            {
                mon = 0;
                n = sscanf(s, "%d%c%3s%c%d", &yr, &sep1, month, &sep2, &day);
                if ( n < 3 ) return 0;
            }
            break;

          case D_M_Y:
            n = sscanf(s, "%d%c%d%c%d", &day, &sep1, &mon, &sep2, &yr);
            if ( n < 3 )
            {
                mon = 0;
                n = sscanf(s, "%d%c%3s%c%d", &day, &sep1, month, &sep2, &yr);
                if ( n < 3 ) return 0;
            }
            break;

          default: // M_D_Y
            n = sscanf(s, "%d%c%d%c%d", &mon, &sep1, &day, &sep2, &yr);
            if ( n < 3 )
            {
                mon = 0;
                n = sscanf(s, "%3s%c%d%c%d", month, &sep1, &day, &sep2, &yr);
                if ( n < 3 ) return 0;
            }
        }
        if (mon == 0) mon = datetime_findMonth(month);
        *d = datetime_encodeDate(yr, mon, day);
    }
    if (*d == -DateDelta) return 0;
    else return 1;
}

//=============================================================================

int datetime_strToTime(char* s, DateTime* t)

//  Input:   s = time as string
//  Output:  t = encoded time,
//           returns 1 if conversion successful, 0 if not
//  Purpose: converts a string time to a DateTime value.
//  Note:    accepts time as hr:min:sec or as decimal hours.

{
    int  n, hr, min = 0, sec = 0;
    char *endptr;

    // Attempt to read time as decimal hours
    *t = strtod(s, &endptr);
    if ( *endptr == 0 )
    {
        *t /= 24.0;
        return 1;
    }

    // Read time in hr:min:sec format
    *t = 0.0;
    n = sscanf(s, "%d:%d:%d", &hr, &min, &sec);
    if ( n == 0 ) return 0;
    *t = datetime_encodeTime(hr, min, sec);
    if ( (hr >= 0) && (min >= 0) && (sec >= 0) ) return 1;
    else return 0;
}

//=============================================================================

void datetime_setDateFormat(int fmt)

//  Input:   fmt = date format code
//  Output:  none
//  Purpose: sets date format

{
    if ( fmt >= Y_M_D && fmt <= M_D_Y) DateFormat = fmt;
}

//=============================================================================

DateTime datetime_addSeconds(DateTime date1, double seconds)

//  Input:   date1 = an encoded date/time value
//           seconds = number of seconds to add to date1
//  Output:  returns updated value of date1
//  Purpose: adds a given number of seconds to a date/time.

{
    double d = floor(date1);
    int h, m, s;
    datetime_decodeTime(date1, &h, &m, &s);
    return d + (3600.0*h + 60.0*m + s + seconds)/SecsPerDay;
}

//=============================================================================

DateTime datetime_addDays(DateTime date1, DateTime date2)

//  Input:   date1 = an encoded date/time value
//           date2 = decimal days to be added to date1
//  Output:  returns date1 + date2
//  Purpose: adds a given number of decimal days to a date/time.

{
    double d1 = floor(date1);
    double d2 = floor(date2);
    int h1, m1, s1;
    int h2, m2, s2;
    datetime_decodeTime(date1, &h1, &m1, &s1);
    datetime_decodeTime(date2, &h2, &m2, &s2);
    return d1 + d2 + datetime_encodeTime(h1+h2, m1+m2, s1+s2);
}

//=============================================================================

long datetime_timeDiff(DateTime date1, DateTime date2)

//  Input:   date1 = an encoded date/time value
//           date2 = an encoded date/time value
//  Output:  returns date1 - date2 in seconds
//  Purpose: finds number of seconds between two dates.

{
    double d1 = floor(date1);
    double d2 = floor(date2);
    int    h, m, s;
    long   s1, s2, secs;
    datetime_decodeTime(date1, &h, &m, &s);
    s1 = 3600*h + 60*m + s;
    datetime_decodeTime(date2, &h, &m, &s);
    s2 = 3600*h + 60*m + s;
    secs = (int)(floor((d1 - d2)*SecsPerDay + 0.5));
    secs += (s1 - s2);
    return secs;
}

//=============================================================================

int  datetime_monthOfYear(DateTime date)

//  Input:   date = an encoded date/time value
//  Output:  returns index of month of year (1..12)
//  Purpose: finds month of year (Jan = 1 ...) for a given date.

{
    int year, month, day;
    datetime_decodeDate(date, &year, &month, &day);
    return month;
}

//=============================================================================

int  datetime_dayOfYear(DateTime date)

//  Input:   date = an encoded date/time value
//  Output:  returns day of year (1..365)
//  Purpose: finds day of year (Jan 1 = 1) for a given date.

{
    int year, month, day;
    DateTime startOfYear;
    datetime_decodeDate(date, &year, &month, &day);
    startOfYear = datetime_encodeDate(year, 1, 1);
    return (int)(floor(date - startOfYear)) + 1;
}

//=============================================================================

int datetime_dayOfWeek(DateTime date)

//  Input:   date = an encoded date/time value
//  Output:  returns index of day of week (1..7)
//  Purpose: finds day of week (Sun = 1, ... Sat = 7) for a given date.

{
    int t = (int)(floor(date)) + DateDelta;
    return (t % 7) + 1;
}

//=============================================================================

int  datetime_hourOfDay(DateTime date)

//  Input:   date = an encoded date/time value
//  Output:  returns hour of day (0..23)
//  Purpose: finds hour of day (0 = 12 AM, ..., 23 = 11 PM) for a given date.

{
    int hour, min, sec;
    datetime_decodeTime(date, &hour, &min, &sec);
    return hour;
}

//=============================================================================

int  datetime_daysPerMonth(int year, int month)

//  Input:   year = year in which month falls
//           month = month of year (1..12)
//  Output:  returns number of days in the month
//  Purpose: finds number of days in a given month of a specified year.

{
    if ( month < 1 || month > 12 ) return 0;
    return DaysPerMonth[isLeapYear(year)][month-1];
}

//=============================================================================
