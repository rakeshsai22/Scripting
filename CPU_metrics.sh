#!/bin/bash
timestamp=$(date +"%Y%m%d_%H%M%S")
performance_data_file="/home/rise/models/scripts/python/gguf/results/metrics/llm_temp/75/T01_topp05_k10_mt128_t4_18_nctx128_llama2_7b_perf_data_$timestamp.csv"

# sampling interval : sec
sampling_interval=1
if [ ! -f "$performance_data_file" ]; then
  echo "elapsed_time,CPU_Frequency_Hz,CPU_Voltage,CPU_Temperature,CPU_Usage,Free_Memory_MB,Used_Memory_MB,Total_Memory_MB,Buffers_Cache_MB,Available_Memory_MB,Throttling_Status" > "$performance_data_file"
fi
start_time=$SECONDS
while true; do
  elapsed_time=$((SECONDS - start_time))
  cpu_frequency="$(vcgencmd measure_clock arm | awk 'BEGIN { FS="=" } { printf("%.0f", $2) }')"
  cpu_voltage="$(vcgencmd measure_volts core | awk 'BEGIN { FS="=" } { printf("%.2f", $2) }')"
  
  cpu_temperature="$(vcgencmd measure_temp | awk 'BEGIN { FS="=" } { printf("%.1f", $2) }')"
  cpu_usage="$(top -b -n 1 | grep 'Cpu(s):' | awk '{print $2}' | cut -d "%" -f1)"
  free_output=$(free -m)
  total_memory=$(echo "$free_output" | awk 'NR==2{printf("%.0f", $2)}')
  used_memory=$(echo "$free_output" | awk 'NR==2{printf("%.0f", $3)}')
  free_memory=$(echo "$free_output" | awk 'NR==2{printf("%.0f", $4)}')
  buffers_cache=$(echo "$free_output" | awk 'NR==2{printf("%.0f", $6)}')
  available_memory=$(echo "$free_output" | awk 'NR==2{printf("%.0f", $7)}')
  throttling_status="$(vcgencmd get_throttled | awk 'BEGIN { FS="=" } { print $2 }')"

  echo "$elapsed_time,$cpu_frequency,$cpu_voltage,$cpu_temperature,$cpu_usage,$free_memory,$used_memory,$total_memory,$buffers_cache,$available_memory,$throttling_status" >> "$performance_data_file"
  sleep_time=$(($start_time + ($elapsed_time + 1) * $sampling_interval - SECONDS))
  [ $sleep_time -gt 0 ] && sleep $sleep_time
done

