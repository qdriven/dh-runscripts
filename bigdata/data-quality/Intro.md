# Data Quality 

Intensive Data Application Build on Data, So Data Qualtiy Matters.What Data Quality Does:
- Quality Measurement
- Data Profiling
- Validation
- Visualization Data Quality accross different System

## Why 

Concurrently Evaluate Data Quality is difficult and expensive. 
Griffin Case:
```
eBay Real-Time PErsonalization:
One Data, ~600M records need to validate data quality
```

Why:
- No End-To-End view of data quality from multiple data source to target application(lineage of data),
  fix data problem is time cost.
- No measurement of data quality in streaming mode.
  The ideal workflow flow should be like:

```flow

st=>start: Start Data Quality Setting
e=>End: Job and Alert is done
define1=>operation: Define Mesurements for A DataSet/Streaming
define2=>operation: visulization defined

st->define(right)->define1->define2->ed

```

- No Unified API to Serve Others
  
## Layers

- Data Quality Model Engine
  * Various Data Quality Dimension
  * Data Quality Validation
- Data Collection Layer
- Data Process and Storage Layer

## Terms and Entities

- Measure: a process logic on certain properties of data.
- Job: an entity which represents a specific task under the evaluation rule of a Measure.
- JobSchedule:  an entity which determines how to schedule a Job
- Metric: an entity which describes the computation results of a Job
  
![img](https://cwiki.apache.org/confluence/download/attachments/70255511/main.png?version=1&modificationDate=1516095163000&api=v2)




## Data Quality Measurements: ToDO Learning from the example

- Accuracy: 
- Completeness
- Validity
- Timelines
- Anomaly Detection
- Data Profiling

## Data Quality - Accuracy Explanation

 Hive table and Avro file

DLS Translation:
DSL: 
```
source.id = target.id and source.name = target.name
```
=>
```
- get miss items from source: SELECT source.* FROM source LEFT JOIN target ON coalesce(source.id, '') = coalesce(target.id, '') and coalesce(source.name, '') = coalesce(target.name, '') WHERE (NOT (source.id IS NULL AND source.name IS NULL)) AND (target.id IS NULL AND target.name IS NULL), save as table miss_items.
- get miss count: SELECT COUNT(*) AS miss FROM miss_items, save as table miss_count.
- get total count from source: SELECT COUNT(*) AS total FROM source, save as table total_count.
- get accuracy metric: SELECT miss_count.miss AS miss, total_count.total AS total, (total_count.total - miss_count.miss) AS matched FROM miss_count FULL JOIN total_count, save as table accuracy.
```

## Data Quality - Profiling Explanation

Aggregation function:

- Support:
```
select, from, where, group-by, having, order-by, limit 
```
  SQL Directly as supplement.
-  Translation:
```sql
profiling sql rule: SELECT source.cntry, count(source.id), max(source.age) FROM source GROUP BY source.cntry, save as table profiling.
```

## Data Quality - Uniqueness

Duplication finding:
- source:
```
name, age
```
- translation to :
```
- get distinct items from source: SELECT name, age FROM source, save as table src.
- get all items from target: SELECT name, age FROM target, save as table tgt.

- join two tables: SELECT src.name, src.age FROM tgt RIGHT JOIN src ON coalesce(src.name, '') = coalesce(tgt.name, '') AND coalesce(src.age, '') = coalesce(tgt.age, ''), save as table joined.
- get items duplication: SELECT name, age, (count(*) - 1) AS dup FROM joined GROUP BY name, age, save as table grouped.
- get total metric: SELECT count(*) FROM source, save as table total_metric.
- get unique record: SELECT * FROM grouped WHERE dup = 0, save as table unique_record.
- get unique metric: SELECT count(*) FROM unique_record, save as table unique_metric.
- get duplicate record: SELECT * FROM grouped WHERE dup > 0, save as table dup_record.
- get duplicate metric: SELECT dup, count(*) AS num FROM dup_records GROUP BY dup, save as table dup_metric.
```

## Data Quality - Timelineness

For timeliness, is to measure the latency of each item, and get the statistics of the latencies. 

```
- get input and output time column: SELECT *, ts AS _bts, out_ts AS _ets FROM source, save as table origin_time.
- get latency: SELECT *, (_ets - _bts) AS latency FROM origin_time, save as table lat.
- get timeliness metric: SELECT CAST(AVG(latency) AS BIGINT) AS avg, MAX(latency) AS max, MIN(latency) AS min FROM lat, save as table time_metric.
```

## 

## Data Collection Layer

- Batch Mode
- Streaming: From Messaging System like Kakfa
  
## Data Process and Storage Layer

- Spark cluster to copute data quality metrics
- Streaming/Near Real Time: spark cluster/ES 

![img](https://github.com/apache/griffin/blob/master/griffin-doc/img/arch.png)

## High Level of Griffin API

- Measures: CRUD
- Jobs: CRUD/Trigger/Healthy Statistics
- Metrics:
   * Table Metadata
   * Table Name
   * Database MetaData
   * All Database Name
   * All Tables Metadatas



## Aliyun References

- 数据校验
- 质量监控系统
- 报警系统
- 监控分析
