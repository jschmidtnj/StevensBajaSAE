use StevensBajaSAEData;
select speed,fuel_level,temp_1,temp_2,lap_distance,total_distance,driving_mode,previous_lap_time,current_lap_time,total_time,lap_count,current_time from realtimedata
into outfile '/tmp/data.csv'
fields terminated by ','
enclosed by '"'
lines terminated by '\n';
exit