/*
* outputAPI.h
*
*      Author: Colleen Barr
*
*
*/

#ifndef OUTPUTAPI_H_
#define OUTPUTAPI_H_

#undef WINDOWS
#ifdef _WIN32
#define WINDOWS
#endif
#ifdef __WIN32__
#define WINDOWS
#endif

/*
//#define DLLEXPORT __declspec(dllexport) __cdecl
#ifdef WINDOWS
#define DLLEXPORT __declspec(dllexport)
#else
#define DLLEXPORT
#endif
*/
#define DLLEXPORT __declspec(dllexport) __cdecl

#define MAXFILENAME     259   //
#define MAXELENAME       45   // Max characters in element name

#include <stdbool.h>


/*------------------- Error Messages --------------------*/
#define ERR411 "Input Error 411: no memory allocated for results."
#define ERR412 "Input Error 412: no results; binary file hasn't been opened."
#define ERR421 "Input Error 421: invalid parameter code."
#define ERR434 "File Error  434: unable to open binary output file."
#define ERR435 "File Error  435: run terminated; no results in binary file."
#define ERR441 "Error 441: need to call SMO_open before calling this function"

typedef struct SMOutputAPI SMOutputAPI; // opaque pointer

typedef enum {
	subcatchCount,
	nodeCount,
	linkCount,
	pollutantCount

} SMO_elementCount;

typedef enum {
	flow_rate,
	concentration

} SMO_unit;

typedef enum {
	//getSeries,
	getAttribute,
	getResult

} SMO_apiFunction;

typedef enum {
	subcatch,
	node,
	link,
	sys

} SMO_elementType;

typedef enum {
//	reportStart,
	reportStep,
	numPeriods

} SMO_time;

typedef enum {
	rainfall_subcatch,  	// (in/hr or mm/hr),
	snow_depth_subcatch,	// (in or mm),
	evap_loss, 				// (in/hr or mm/hr),
	infil_loss,				// (in/hr or mm/hr),
	runoff_rate,     		// (flow units),
	gwoutflow_rate,  		// (flow units),
	gwtable_elev,    		// (ft or m),
	soil_moisture,			// unsaturated zone moisture content (-),
	pollutant_conc_subcatch	// first pollutant

} SMO_subcatchAttribute;

typedef enum {
	invert_depth,          	// (ft or m),
	hydraulic_head,        	// (ft or m),
	stored_ponded_volume,  	// (ft3 or m3),
	lateral_inflow,        	// (flow units),
	total_inflow,          	// lateral + upstream (flow units),
	flooding_losses,       	// (flow units),
	pollutant_conc_node     // first pollutant,

} SMO_nodeAttribute;

typedef enum {
	flow_rate_link,      	// (flow units),
	flow_depth,     		// (ft or m),
	flow_velocity,  		// (ft/s or m/s),
	flow_volume,			// (ft3 or m3),
	capacity,       		// (fraction of conduit filled),
	pollutant_conc_link  	// first pollutant,

} SMO_linkAttribute;

typedef enum {
	air_temp,              	// (deg. F or deg. C),
	rainfall_system,        // (in/hr or mm/hr),
	snow_depth_system,      // (in or mm),
	evap_infil_loss,	  	// (in/hr or mm/hr),
	runoff_flow,           	// (flow units),
	dry_weather_inflow,    	// (flow units),
	groundwater_inflow,    	// (flow units),
	RDII_inflow,           	// (flow units),
	direct_inflow,         	// user defined (flow units),
	total_lateral_inflow,  	// (sum of variables 4 to 8) //(flow units),
	flood_losses,       	// (flow units),
	outfall_flows,         	// (flow units),
	volume_stored,         	// (ft3 or m3),
	evap_rate             	// (in/day or mm/day),
	//p_evap_rate		    // (in/day or mm/day)
} SMO_systemAttribute;


SMOutputAPI* DLLEXPORT SMO_init(void);
int DLLEXPORT SMO_open(SMOutputAPI* smoapi, const char* path);


DLLEXPORT int SMO_getProjectSize(SMOutputAPI* smoapi, SMO_elementCount code, int* count);
DLLEXPORT int SMO_getUnits(SMOutputAPI* smoapi, SMO_unit code, int* unitFlag);
DLLEXPORT int SMO_getStartTime(SMOutputAPI* smoapi, double* time);
DLLEXPORT int SMO_getTimes(SMOutputAPI* smoapi, SMO_time code, int* time);

int DLLEXPORT SMO_getElementName(SMOutputAPI* smoapi, SMO_elementType type,
		int elementIndex, char* elementName, int* length);

DLLEXPORT float* SMO_newOutValueSeries(SMOutputAPI* smoapi, long seriesStart,
	long seriesLength, long* length, int* errcode);
DLLEXPORT float* SMO_newOutValueArray(SMOutputAPI* smoapi, SMO_apiFunction func,
	SMO_elementType type, long* length, int* errcode);

DLLEXPORT int SMO_getSubcatchSeries(SMOutputAPI* smoapi, int subcatchIndex,
	SMO_subcatchAttribute attr, long timeIndex, long length, float* outValueSeries);
DLLEXPORT int SMO_getNodeSeries(SMOutputAPI* smoapi, int nodeIndex, SMO_nodeAttribute attr,
	long timeIndex, long length, float* outValueSeries);
DLLEXPORT int SMO_getLinkSeries(SMOutputAPI* smoapi, int linkIndex, SMO_linkAttribute attr,
	long timeIndex, long length, float* outValueSeries);
DLLEXPORT int SMO_getSystemSeries(SMOutputAPI* smoapi, SMO_systemAttribute attr,
	long timeIndex, long length, float *outValueSeries);

DLLEXPORT int SMO_getSubcatchAttribute(SMOutputAPI* smoapi, long timeIndex,
	SMO_subcatchAttribute attr, float* outValueArray);
DLLEXPORT int SMO_getNodeAttribute(SMOutputAPI* smoapi, long timeIndex,
	SMO_nodeAttribute attr, float* outValueArray);
DLLEXPORT int SMO_getLinkAttribute(SMOutputAPI* smoapi, long timeIndex,
	SMO_linkAttribute attr, float* outValueArray);
DLLEXPORT int SMO_getSystemAttribute(SMOutputAPI* smoapi, long timeIndex,
	SMO_systemAttribute attr, float* outValueArray);

DLLEXPORT int SMO_getSubcatchResult(SMOutputAPI* smoapi, long timeIndex, int subcatchIndex,
	float* outValueArray);
DLLEXPORT int SMO_getNodeResult(SMOutputAPI* smoapi, long timeIndex, int nodeIndex,
	float* outValueArray);
DLLEXPORT int SMO_getLinkResult(SMOutputAPI* smoapi, long timeIndex, int linkIndex,
	float* outValueArray);
DLLEXPORT int SMO_getSystemResult(SMOutputAPI* smoapi, long timeIndex, float* outValueArray);

DLLEXPORT void SMO_free(float *array);

DLLEXPORT int SMO_close(SMOutputAPI* smoapi);
DLLEXPORT int SMO_errMessage(int errcode, char* errmsg, int n);


#endif /* OUTPUTAPI_H_ */
