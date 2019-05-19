# Griffin Notes

Data Quality Model Engine: Apache Griffin is a model driven solution, users can choose various data quality dimension to execute their data quality validation based on selected target data-set or source data-set ( as the golden reference data). It has corresponding library supporting in back-end for the following measurement:

- Accuracy - reflects the real-world objects or a verifiable source into data
- Completeness - keeps all necessary data present
- Validity - corrects all data values within the data domains specified by the business
- Timeliness - keeps the data available at the time needed
- Anomaly detection - pre-built algorithm functions for the identification of items, events or observations which do not conform to an expected pattern or other items in a dataset
- Data Profiling - applies statistical analysis and assessment of data values within a dataset for consistency, uniqueness and logic.

## Data Collection Layer


- Batch Mode : data source from hadoop from kafka
- Real Time Mode: connect with Message System like kafka for real time analysis
- How about CDC for real time anaysis for data quality
  
## Data Process and Storage Layer

- Batch Mode: data quality model compute data quality metrics by spark cluster on data source on hadoop
- Near Real time analysis: consume data from message system,compute data quality metrics in spark cluster
- Data Storage: elastic search
- Restful Service: data-sets, create data quality measures, publish metrics, retrieve metrics, add subscription, etc. So, the developers can develop their own user interface based on these web services


## Diagram for Apache Griffin

![img](https://github.com/apache/griffin/blob/master/griffin-doc/img/arch.png)