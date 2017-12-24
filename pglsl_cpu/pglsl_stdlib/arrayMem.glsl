#ifndef __ARRAY_MEM_H_
#define __ARRAY_MEM_H_

const int arrDef = 0;
const int useableMem = 1;
const int heapInitBlockSize = 5;

#define initialize_heap_array( arr, arrSize ) \
    /*Initializes an array or array subsection for use with malloc/free.*/ \
    arr[0] = arrDef;\
    arr[1] = 4; \
    arr[2] = arrSize; \
    arr[3] = arrSize-5; \
    arr[4] = useableMem

#define _find_first_empty_space(arr, arrSize, sizeRequested, loc) \
    /*Sets loc to the first large enough empty space in array arr.*/ \
    loc=0; \
    while(arr[loc] == arrDef ){ \
        if(arr[loc+3] < sizeRequested+heapInitBlockSize){ \
            loc = arr[loc+1]; \
        }else{ \
            loc = arr[loc+2]; \
        } \
        if(loc >=arrSize){ \
            break; \
        } \
    }



#define malloc(arr, arrSize, sizeRequested, loc) \
    _find_first_empty_space(arr, arrSize, sizeRequested, loc);

#endif