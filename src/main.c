/*
* main.c
* TODO
*	Error handling from getID functions (and check other error handling)
*
*/

#define _CRTDBG_MAP_ALLOC
#include <stdlib.h>
//#include <crtdbg.h>



#include <stdio.h>
//#include <stdlib.h>
#include <string.h>
#include "outputAPI.h"




#undef WINDOWS
#ifdef _WIN32
#define WINDOWS
#endif
#ifdef __WIN32__
#define WINDOWS
#endif

// #ifdef WINDOWS
// #define DLLEXPORT __declspec(dllimport) __cdecl
// #else
// #define DLLEXPORT
// #endif

#undef DLLEXPORT

int main(int argc, char* argv[])
{
	SMOutputAPI* smoapi = NULL; 
	//char path[MAXFNAME] = "C:\\Users\\cbarr02\\Desktop\\GitHub\\Storm-Water-Plugin\\outputAPI\\Example3.out"; // no pollutants
	//char path[MAXFNAME] = "C:\\PROJECTCODE\\SWMMOutputAPI\\testing\\OutputTestModel_LargeOutput.out";
	char path[MAXFNAME] = "C:\\PROJECTCODE\\SWMMOutputAPI\\testing\\OutputTestModel522_SHORT.out";

	char pathout[MAXFNAME] = "C:\\PROJECTCODE\\SWMMOutputAPI\\testing\\testingexeout.txt";
	FILE *FOut;
	
	int count, count2, count3;
	//int units;
	//puts("Here");
	//double time;
	int numperiods;

	float* array0;
	float* series0;
	//double* arraytime;
	//int errortime;
	//long alength0;
	long length;
	int error0;//, error1, error2, error3;
	//puts("Here1");
	struct IDentry *subcatchids;
	//struct IDentry *nodeids;
	//struct IDentry *linkids;
	//struct IDentry *pollutids;

	int errBEM = SMR_open(path, &smoapi);
	printf("Here2 %i\n", errBEM);
	SMO_getProjectSize(smoapi, subcatchCount, &count); // 7 subcatchments
	printf("Subcatch Count: %i\n", count);	
	SMO_getProjectSize(smoapi, nodeCount, &count2); // 12 junctions + 1 outfall + 1 storage
	printf("Node Count: %i\n", count2);	
	SMO_getProjectSize(smoapi, linkCount, &count3); // 12 conduits + 3 orifices + 1 weir
	printf("Link Count: %i\n", count3);	

	//SMO_getUnits(smoapi, flow_rate, &units); // 0 corresponds to CFS

	//SMO_getStartTime(smoapi, &time); // decimal days since 12 AM on 12/30/1899
	SMO_getTimes(smoapi, numPeriods, &numperiods); // report time step is 60 seconds
	//arraytime = SMO_newOutTimeList(smoapi, &errortime);
	//SMO_getTimeList(smoapi, arraytime); // first value will be start time + one reporting period (in decimal days)
	//puts("Here3");
	series0 = SMO_newOutValueSeries(smoapi, 0, numperiods, &length, &error0);
	SMO_getLinkSeries(smoapi, 0, 0, 0, numperiods, series0); 

	array0 = SMO_newOutValueArray(smoapi, getAttribute, link, &length, &error0);
	SMO_getLinkAttribute(smoapi, 1, 0, array0);

	//subcatchids = SMO_getSubcatchIDs(smoapi, &error0);
	//printf("Subcatch %i\n", error0);
	
	
	FOut = fopen(pathout,"w");
	int i = 0;
	for(i = 0; i < numperiods; i++)
	{
		fprintf(FOut, "%d\t%f\n", i, series0[i]);
	}
	fclose(FOut);

	//nodeids = SMO_getNodeIDs(smoapi, &error1);
	//linkids = SMO_getLinkIDs(smoapi, &error2);
	//pollutids = SMO_getPollutIDs(smoapi, &error3);

	//SMO_free(array0);
	//puts("Here4");
	//SMO_freeIDList(subcatchids);
	//SMO_freeIDList(nodeids);
	//SMO_freeIDList(linkids);
	//SMO_freeIDList(pollutids);

	//SMO_freeTimeList(arraytime);

	SMO_free(series0);

	SMO_close(smoapi);
	//puts("Here5");
//#ifdef WINDOWS 
//	_CrtSetReportMode(_CRT_ERROR, _CRTDBG_MODE_DEBUG);
//	_CrtDumpMemoryLeaks();
//	return 0;

//#else
	
	return 0;

//#endif
}
