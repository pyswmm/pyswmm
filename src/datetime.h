//-----------------------------------------------------------------------------
//   datetime.h
//
//   Project:  EPA SWMM5
//   Version:  5.1
//   Date:     03/20/14   (Build 5.1.001)
//   Author:   L. Rossman
//
//   The DateTime type is used to store date and time values. It is
//   equivalent to a double floating point type.
//
//   The integral part of a DateTime value is the number of days that have
//   passed since 12/31/1899. The fractional part of a DateTime value is the
//   fraction of a 24 hour day that has elapsed.
//-----------------------------------------------------------------------------
#undef WINDOWS
#ifdef _WIN32
#define WINDOWS
#endif
#ifdef __WIN32__
#define WINDOWS
#endif

/*
#ifdef WINDOWS
//#define DLLEXPORT __declspec(dllexport) __cdecl
#define DLLEXPORT __declspec(dllexport)
#else
#define DLLEXPORT
#endif
*/
#define DLLEXPORT __declspec(dllexport) __cdecl

typedef double DateTime;

#define Y_M_D 0
#define M_D_Y 1
#define D_M_Y 2
#define NO_DATE -693594 // 1/1/0001
#define DATE_STR_SIZE 12
#define TIME_STR_SIZE 9

// Functions for encoding a date or time value to a DateTime value
DateTime datetime_encodeDate(int year, int month, int day);
DateTime datetime_encodeTime(int hour, int minute, int second);

// Functions for decoding a DateTime value to a date and time
void datetime_decodeDate(DateTime date, int* y, int* m, int* d);
void datetime_decodeTime(DateTime time, int* h, int* m, int* s);

// Function for finding day of week for a date (1 = Sunday)
// month of year, days per month, and hour of day
int  datetime_monthOfYear(DateTime date);
int  datetime_dayOfYear(DateTime date);
int  datetime_dayOfWeek(DateTime date);
int  datetime_hourOfDay(DateTime date);
int  datetime_daysPerMonth(int year, int month);

// Functions for converting a DateTime value to a string
void DLLEXPORT datetime_dateToStr(DateTime date, char* s);
void DLLEXPORT datetime_timeToStr(DateTime time, char* s);

// Functions for converting a string date or time to a DateTime value
int  datetime_findMonth(char* s);
int  datetime_strToDate(char* s, DateTime* d);
int  datetime_strToTime(char* s, DateTime* t);

// Function for setting date format
void datetime_setDateFormat(int fmt);

// Functions for adding and subtracting dates
DateTime datetime_addSeconds(DateTime date1, double seconds);
DateTime datetime_addDays(DateTime date1, DateTime date2);
long     datetime_timeDiff(DateTime date1, DateTime date2);
