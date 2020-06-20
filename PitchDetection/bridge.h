#pragma once
#include "TunerStream.h"

extern "C"
{
    TunerStream* create_stream(int sample_rate);
    void start_stream(TunerStream* handle); //DO NOT CALL TWICE!!!!!!!!!
    void pause_stream(TunerStream* handle);
    void resume_stream(TunerStream* handle);
    void stop_stream(TunerStream* handle);
    bool read_stream(TunerStream* handle, double* val);
}