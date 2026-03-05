# 📊 Auto Mini EDA Report

**File**: `stackoverflow_developer_data.csv`

**Total rows**: 89,184

**Total columns**: 84

**Memory usage**: 476 MB

## 🎯 Dataset Quality Score

### Overall Grade: 🚨 **F** - Critical Issues

**Score**: 56.6 / 100.0 (56.6%)

#### Score Breakdown

| Category | Score | Max | Percentage |
|----------|-------|-----|------------|
| Completeness | 16.6 | 25 | 66.4% |
| Data Quality | 6.0 | 25 | 24.0% |
| Feature Quality | 12.0 | 25 | 48.0% |
| Ml Readiness | 22.0 | 25 | 88.0% |

#### 💡 Recommendations

- ⚠️ Handle missing values: Consider imputation or removal
- ⚠️ Address 46 data quality warnings
- ⚠️ Review and handle outliers in 4 columns
- ⚠️ Remove 1 ID-like columns before training
- ⚠️ Consider removing 44 sparse columns

## 🎯 Target Variable Suggestions

### 🌟 Top Candidate: `MainBranch`

- **Score**: 25/100
- **Task Type**: Multi Class Classification
- **Unique Values**: 6
- **Data Type**: str
- **Reasons**:
  - 6 classes (classification)
  - No missing values

### Other Candidates

| Column | Score | Task Type | Unique Values |
|--------|-------|-----------|---------------|
| `Age` | 25 | Multi Class Classification | 8 |
| `TBranch` | 25 | Binary Classification | 2 |
| `SurveyLength` | 25 | Multi Class Classification | 3 |
| `SurveyEase` | 25 | Multi Class Classification | 3 |

## 🚨 Feature Leakage Detection

**Total Warnings**: 2
- 🚨 High Severity: 0
- ⚠️ Medium Severity: 1
- ℹ️ Low Severity: 1

### ⚠️ Medium Severity (Review Recommended)

- **`ResponseId`**: Every row unique - possible ID or timestamp leakage

### ℹ️ Low Severity (Informational)

- `Q120`: Constant value - no information

## 🔍 Outlier Detection Summary

- **Columns with outliers**: 4
- **Total outliers detected**: 11571
- **Detection methods used**: iqr, zscore, modified_zscore, isolation_forest

## ⚠️ Data Quality Warnings

- Column 'ResponseId' is high cardinality (unique/rows = 1.00); likely an ID column.
- Column 'Q120' has a single unique value (no predictive power).
- Column 'LearnCodeCoursesCert' has high missing values (58.43%).
- Column 'TechList' has high missing values (31.77%).
- Column 'CompTotal' has significant outliers (16.4% by IQR method).
- Column 'CompTotal' has high missing values (45.93%).
- Column 'DatabaseWantToWorkWith' has high missing values (31.7%).
- Column 'PlatformWantToWorkWith' has high missing values (42.47%).
- Column 'WebframeWantToWorkWith' has high missing values (36.38%).
- Column 'MiscTechHaveWorkedWith' has high missing values (36.07%).
- Column 'MiscTechWantToWorkWith' has high missing values (47.47%).
- Column 'OfficeStackAsyncWantToWorkWith' has high missing values (39.74%).
- Column 'AISearchHaveWorkedWith' has high missing values (36.84%).
- Column 'AISearchWantToWorkWith' has high missing values (48.25%).
- Column 'AIDevHaveWorkedWith' has high missing values (70.95%).
- Column 'AIDevWantToWorkWith' has high missing values (78.04%).
- Column 'SOAI' has high missing values (46.34%).
- Column 'AISent' has high missing values (31.04%).
- Column 'AIAcc' has high missing values (56.73%).
- Column 'AIBen' has high missing values (31.16%).
- Column 'AIToolInterested in Using' has high missing values (63.24%).
- Column 'AIToolCurrently Using' has high missing values (59.48%).
- Column 'AIToolNot interested in Using' has high missing values (76.38%).
- Column 'AINextVery different' has high missing values (85.8%).
- Column 'AINextNeither different nor similar' has high missing values (92.6%).
- Column 'AINextSomewhat similar' has high missing values (93.01%).
- Column 'AINextVery similar' has high missing values (97.06%).
- Column 'AINextSomewhat different' has high missing values (73.87%).
- Column 'ICorPM' has high missing values (51.04%).
- Column 'WorkExp' has high missing values (51.14%).
- Column 'Knowledge_1' has high missing values (52.31%).
- Column 'Knowledge_2' has high missing values (53.28%).
- Column 'Knowledge_3' has high missing values (53.13%).
- Column 'Knowledge_4' has high missing values (53.26%).
- Column 'Knowledge_5' has high missing values (53.44%).
- Column 'Knowledge_6' has high missing values (53.44%).
- Column 'Knowledge_7' has high missing values (53.5%).
- Column 'Knowledge_8' has high missing values (53.57%).
- Column 'Frequency_1' has high missing values (53.0%).
- Column 'Frequency_2' has high missing values (52.99%).
- Column 'Frequency_3' has high missing values (53.97%).
- Column 'TimeSearching' has high missing values (52.03%).
- Column 'TimeAnswering' has high missing values (52.2%).
- Column 'ProfessionalTech' has high missing values (53.15%).
- Column 'Industry' has high missing values (58.77%).
- Column 'ConvertedCompYearly' has high missing values (46.16%).

## 📊 Column Type Distribution

- **Numeric**: 4
- **Categorical**: 80
- **Object**: 80

## 🎯 Columns with Detected Outliers

| Column | Outlier Count | Outlier % | Methods Detected |
|--------|---------------|-----------|------------------|
| `ResponseId` | 0 | 0.00% | isolation_forest, consensus |
| `CompTotal` | 7902 | 16.39% | iqr, iqr_extreme, zscore, modified_zscore, isolation_forest, consensus |
| `WorkExp` | 1463 | 3.36% | iqr, iqr_extreme, zscore, modified_zscore, isolation_forest, consensus |
| `ConvertedCompYearly` | 2206 | 4.59% | iqr, iqr_extreme, zscore, modified_zscore, isolation_forest, consensus |

## 🔑 ID-like Columns (Consider Removing)

- `ResponseId` (reasons: near_unique_integer, unique_ratio: 1.00)

## 🕳️ Sparse Columns (Low Information)

- `Q120` (reasons: dominant_value, null%: 0)
- `LearnCodeCoursesCert` (reasons: missing_heavy, null%: 58.43)
- `TechList` (reasons: missing_heavy, null%: 31.77)
- `CompTotal` (reasons: missing_heavy, null%: 45.93)
- `DatabaseWantToWorkWith` (reasons: missing_heavy, null%: 31.7)
- `PlatformWantToWorkWith` (reasons: missing_heavy, null%: 42.47)
- `WebframeWantToWorkWith` (reasons: missing_heavy, null%: 36.38)
- `MiscTechHaveWorkedWith` (reasons: missing_heavy, null%: 36.07)
- `MiscTechWantToWorkWith` (reasons: missing_heavy, null%: 47.47)
- `OfficeStackAsyncWantToWorkWith` (reasons: missing_heavy, null%: 39.74)
- `AISearchHaveWorkedWith` (reasons: missing_heavy, null%: 36.84)
- `AISearchWantToWorkWith` (reasons: missing_heavy, null%: 48.25)
- `AIDevHaveWorkedWith` (reasons: missing_heavy, null%: 70.95)
- `AIDevWantToWorkWith` (reasons: missing_heavy, null%: 78.04)
- `SOAI` (reasons: missing_heavy, null%: 46.34)
- `AISent` (reasons: missing_heavy, null%: 31.04)
- `AIAcc` (reasons: missing_heavy, null%: 56.73)
- `AIBen` (reasons: missing_heavy, null%: 31.16)
- `AIToolInterested in Using` (reasons: missing_heavy, null%: 63.24)
- `AIToolCurrently Using` (reasons: missing_heavy, null%: 59.48)
- `AIToolNot interested in Using` (reasons: missing_heavy, null%: 76.38)
- `AINextVery different` (reasons: missing_heavy, null%: 85.8)
- `AINextNeither different nor similar` (reasons: missing_heavy, null%: 92.6)
- `AINextSomewhat similar` (reasons: missing_heavy, null%: 93.01)
- `AINextVery similar` (reasons: missing_heavy, null%: 97.06)
- `AINextSomewhat different` (reasons: missing_heavy, null%: 73.87)
- `ICorPM` (reasons: missing_heavy, null%: 51.04)
- `WorkExp` (reasons: missing_heavy, null%: 51.14)
- `Knowledge_1` (reasons: missing_heavy, null%: 52.31)
- `Knowledge_2` (reasons: missing_heavy, null%: 53.28)
- `Knowledge_3` (reasons: missing_heavy, null%: 53.13)
- `Knowledge_4` (reasons: missing_heavy, null%: 53.26)
- `Knowledge_5` (reasons: missing_heavy, null%: 53.44)
- `Knowledge_6` (reasons: missing_heavy, null%: 53.44)
- `Knowledge_7` (reasons: missing_heavy, null%: 53.5)
- `Knowledge_8` (reasons: missing_heavy, null%: 53.57)
- `Frequency_1` (reasons: missing_heavy, null%: 53)
- `Frequency_2` (reasons: missing_heavy, null%: 52.99)
- `Frequency_3` (reasons: missing_heavy, null%: 53.97)
- `TimeSearching` (reasons: missing_heavy, null%: 52.03)
- `TimeAnswering` (reasons: missing_heavy, null%: 52.2)
- `ProfessionalTech` (reasons: missing_heavy, null%: 53.15)
- `Industry` (reasons: missing_heavy, null%: 58.77)
- `ConvertedCompYearly` (reasons: missing_heavy, null%: 46.16)

---

## 📋 Detailed Column Analysis

### Age

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 0
- **null_percent**: 0
- **unique_count**: 8
- **dominant_value_ratio**: 0.3728
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: False
- **warnings**:
- **top_values**:
  - `25-34 years old`: 33247
  - `35-44 years old`: 20532
  - `18-24 years old`: 17931
  - `45-54 years old`: 8334
  - `Under 18 years old`: 4128

### AIAcc

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 50590
- **null_percent**: 56.7254
- **unique_count**: 60
- **dominant_value_ratio**: 0.1704
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'AIAcc' has high missing values (56.73%).
- **top_values**:
  - `Increase productivity;Greater efficiency;Speed up learning`: 6576
  - `Increase productivity;Greater efficiency;Speed up learning;Improve accuracy in coding`: 5252
  - `Increase productivity;Greater efficiency`: 4877
  - `Increase productivity;Speed up learning`: 4349
  - `Increase productivity`: 3114

### AIBen

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 27788
- **null_percent**: 31.1581
- **unique_count**: 5
- **dominant_value_ratio**: 0.393
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'AIBen' has high missing values (31.16%).
- **top_values**:
  - `Somewhat trust`: 24128
  - `Neither trust nor distrust`: 18837
  - `Somewhat distrust`: 13330
  - `Highly distrust`: 3350
  - `Highly trust`: 1751

### AIDevHaveWorkedWith

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 63280
- **null_percent**: 70.9544
- **unique_count**: 166
- **dominant_value_ratio**: 0.6854
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'AIDevHaveWorkedWith' has high missing values (70.95%).
- **top_values**:
  - `GitHub Copilot`: 17754
  - `GitHub Copilot;Tabnine`: 2248
  - `Tabnine`: 2160
  - `AWS CodeWhisperer;GitHub Copilot`: 813
  - `AWS CodeWhisperer`: 674

### AIDevWantToWorkWith

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 69597
- **null_percent**: 78.0375
- **unique_count**: 233
- **dominant_value_ratio**: 0.6855
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'AIDevWantToWorkWith' has high missing values (78.04%).
- **top_values**:
  - `GitHub Copilot`: 13426
  - `AWS CodeWhisperer;GitHub Copilot`: 1463
  - `Tabnine`: 804
  - `GitHub Copilot;Tabnine`: 751
  - `AWS CodeWhisperer`: 657

### AINextNeither different nor similar

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 82585
- **null_percent**: 92.6007
- **unique_count**: 222
- **dominant_value_ratio**: 0.2811
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'AINextNeither different nor similar' has high missing values (92.6%).
- **top_values**:
  - `Writing code`: 1855
  - `Debugging and getting help`: 772
  - `Learning about a codebase`: 553
  - `Documenting code`: 455
  - `Project planning`: 331

### AINextSomewhat different

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 65881
- **null_percent**: 73.8709
- **unique_count**: 326
- **dominant_value_ratio**: 0.2807
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'AINextSomewhat different' has high missing values (73.87%).
- **top_values**:
  - `Writing code`: 6540
  - `Writing code;Debugging and getting help`: 2072
  - `Debugging and getting help`: 1541
  - `Learning about a codebase`: 1383
  - `Writing code;Documenting code`: 1148

### AINextSomewhat similar

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 82946
- **null_percent**: 93.0055
- **unique_count**: 197
- **dominant_value_ratio**: 0.3562
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'AINextSomewhat similar' has high missing values (93.01%).
- **top_values**:
  - `Writing code`: 2222
  - `Debugging and getting help`: 517
  - `Learning about a codebase`: 398
  - `Writing code;Debugging and getting help`: 361
  - `Writing code;Documenting code`: 301

### AINextVery different

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 76523
- **null_percent**: 85.8035
- **unique_count**: 349
- **dominant_value_ratio**: 0.1234
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'AINextVery different' has high missing values (85.8%).
- **top_values**:
  - `Writing code`: 1563
  - `Debugging and getting help`: 1331
  - `Documenting code`: 1187
  - `Writing code;Debugging and getting help`: 798
  - `Learning about a codebase`: 750

### AINextVery similar

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 86563
- **null_percent**: 97.0611
- **unique_count**: 159
- **dominant_value_ratio**: 0.3602
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'AINextVery similar' has high missing values (97.06%).
- **top_values**:
  - `Writing code`: 944
  - `Debugging and getting help`: 188
  - `Documenting code`: 126
  - `Writing code;Documenting code`: 124
  - `Learning about a codebase`: 124

### AISearchHaveWorkedWith

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 32856
- **null_percent**: 36.8407
- **unique_count**: 323
- **dominant_value_ratio**: 0.5708
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'AISearchHaveWorkedWith' has high missing values (36.84%).
- **top_values**:
  - `ChatGPT`: 32150
  - `Bing AI;ChatGPT`: 6537
  - `ChatGPT;WolframAlpha`: 3855
  - `ChatGPT;Google Bard AI`: 2274
  - `Bing AI;ChatGPT;Google Bard AI`: 1758

### AISearchWantToWorkWith

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 43034
- **null_percent**: 48.253
- **unique_count**: 399
- **dominant_value_ratio**: 0.4682
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'AISearchWantToWorkWith' has high missing values (48.25%).
- **top_values**:
  - `ChatGPT`: 21609
  - `ChatGPT;Google Bard AI`: 4269
  - `Bing AI;ChatGPT`: 4213
  - `Bing AI;ChatGPT;Google Bard AI`: 3374
  - `ChatGPT;WolframAlpha`: 2573

### AISelect

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 1211
- **null_percent**: 1.3579
- **unique_count**: 3
- **dominant_value_ratio**: 0.4438
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: False
- **warnings**:
- **top_values**:
  - `Yes`: 39042
  - `No, and I don't plan to`: 26221
  - `No, but I plan to soon`: 22710

### AISent

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 27683
- **null_percent**: 31.0403
- **unique_count**: 6
- **dominant_value_ratio**: 0.4856
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'AISent' has high missing values (31.04%).
- **top_values**:
  - `Favorable`: 29863
  - `Very favorable`: 17050
  - `Indifferent`: 10147
  - `Unsure`: 2471
  - `Unfavorable`: 1698

### AIToolCurrently Using

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 53047
- **null_percent**: 59.4804
- **unique_count**: 533
- **dominant_value_ratio**: 0.1787
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'AIToolCurrently Using' has high missing values (59.48%).
- **top_values**:
  - `Writing code`: 6459
  - `Writing code;Debugging and getting help`: 3741
  - `Writing code;Documenting code`: 2363
  - `Learning about a codebase;Writing code;Debugging and getting help`: 1673
  - `Writing code;Documenting code;Debugging and getting help`: 1528

### AIToolInterested in Using

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 56401
- **null_percent**: 63.2412
- **unique_count**: 640
- **dominant_value_ratio**: 0.0382
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'AIToolInterested in Using' has high missing values (63.24%).
- **top_values**:
  - `Learning about a codebase;Project planning;Writing code;Documenting code;Debugging and getting help;Testing code;Committing and reviewing code;Deployment and monitoring;Collaborating with teammates `: 1252
  - `Learning about a codebase;Project planning;Documenting code;Debugging and getting help;Testing code;Committing and reviewing code;Deployment and monitoring;Collaborating with teammates `: 742
  - `Learning about a codebase`: 624
  - `Documenting code`: 610
  - `Learning about a codebase;Project planning;Documenting code;Testing code;Committing and reviewing code;Deployment and monitoring;Collaborating with teammates `: 476

### AIToolNot interested in Using

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 68115
- **null_percent**: 76.3758
- **unique_count**: 535
- **dominant_value_ratio**: 0.0991
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'AIToolNot interested in Using' has high missing values (76.38%).
- **top_values**:
  - `Collaborating with teammates `: 2087
  - `Project planning`: 1397
  - `Project planning;Collaborating with teammates `: 1297
  - `Deployment and monitoring;Collaborating with teammates `: 1039
  - `Project planning;Deployment and monitoring;Collaborating with teammates `: 986

### BuyNewTool

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 6175
- **null_percent**: 6.9239
- **unique_count**: 231
- **dominant_value_ratio**: 0.149
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: False
- **warnings**:
- **top_values**:
  - `Start a free trial;Ask developers I know/work with;Visit developer communities like Stack Overflow`: 12371
  - `Start a free trial;Ask developers I know/work with`: 7910
  - `Start a free trial;Ask developers I know/work with;Visit developer communities like Stack Overflow;Read ratings or reviews on third party sites like G2 Crowd`: 6302
  - `Start a free trial`: 4712
  - `Ask developers I know/work with;Visit developer communities like Stack Overflow`: 4358

### CodingActivities

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 15420
- **null_percent**: 17.2901
- **unique_count**: 116
- **dominant_value_ratio**: 0.2075
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: False
- **warnings**:
- **top_values**:
  - `Hobby`: 15308
  - `I don’t code outside of work`: 8809
  - `Hobby;Professional development or self-paced learning from online courses`: 8232
  - `Hobby;Contribute to open-source projects`: 5363
  - `Professional development or self-paced learning from online courses`: 3920

### CompTotal

- **dtype**: float64
- **inferred_dtype**: floating
- **null_count**: 40959
- **null_percent**: 45.9264
- **unique_count**: 3828
- **mean**: 1036806635562467391394372602402550216392704
- **median**: 115000
- **std**: 227684720124393382684674544505631345205051392
- **min**: 0
- **q1**: 63000
- **q3**: 230000
- **max**: 49999999999999992051087350427974655758076739584
- **dominant_value_ratio**: 0.0281
- **zero_ratio**: 0.0027
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'CompTotal' has significant outliers (16.4% by IQR method).
  - Column 'CompTotal' has high missing values (45.93%).
- **Outlier Detection Results**:
  - **IQR Method**: 7902 outliers (16.39%)
    - Bounds: [-187500.00, 480500.00]
    - Sample: 1320000.00, 490000.00, 2000000.00, 1560000.00, 500000.00...
  - **Z-Score Method**: 1 outliers (0.00%)
  - **Modified Z-Score**: 8107 outliers (16.81%)
  - **Consensus**: 5306 avg outliers (11.00%)

### ConvertedCompYearly

- **dtype**: float64
- **inferred_dtype**: floating
- **null_count**: 41165
- **null_percent**: 46.1574
- **unique_count**: 8784
- **mean**: 103110.0817
- **median**: 74963
- **std**: 681418.8387
- **min**: 1
- **q1**: 43907
- **q3**: 121641
- **max**: 74351432
- **dominant_value_ratio**: 0.0163
- **zero_ratio**: 0
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'ConvertedCompYearly' has high missing values (46.16%).
- **Outlier Detection Results**:
  - **IQR Method**: 2206 outliers (4.59%)
    - Bounds: [-72694.00, 238242.00]
    - Sample: 285000.00, 250000.00, 240000.00, 280000.00, 350000.00...
  - **Z-Score Method**: 26 outliers (0.05%)
  - **Modified Z-Score**: 1496 outliers (3.12%)
  - **Consensus**: 1834 avg outliers (3.82%)

### Country

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 1211
- **null_percent**: 1.3579
- **unique_count**: 185
- **dominant_value_ratio**: 0.212
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: False
- **warnings**:
- **top_values**:
  - `United States of America`: 18647
  - `Germany`: 7328
  - `India`: 5625
  - `United Kingdom of Great Britain and Northern Ireland`: 5552
  - `Canada`: 3507

### Currency

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 23850
- **null_percent**: 26.7425
- **unique_count**: 144
- **dominant_value_ratio**: 0.2702
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: False
- **warnings**:
- **top_values**:
  - `EUR European Euro`: 17651
  - `USD	United States dollar`: 16729
  - `GBP	Pound sterling`: 4473
  - `INR	Indian rupee`: 3615
  - `CAD	Canadian dollar`: 2647

### DatabaseHaveWorkedWith

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 15749
- **null_percent**: 17.659
- **unique_count**: 11096
- **dominant_value_ratio**: 0.0592
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: False
- **warnings**:
- **top_values**:
  - `PostgreSQL`: 4350
  - `Microsoft SQL Server`: 3322
  - `MySQL`: 3116
  - `SQLite`: 2299
  - `MongoDB`: 1663

### DatabaseWantToWorkWith

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 28273
- **null_percent**: 31.7019
- **unique_count**: 10485
- **dominant_value_ratio**: 0.079
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'DatabaseWantToWorkWith' has high missing values (31.7%).
- **top_values**:
  - `PostgreSQL`: 4815
  - `Microsoft SQL Server`: 2180
  - `SQLite`: 1771
  - `MySQL`: 1754
  - `PostgreSQL;SQLite`: 1631

### DevType

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 12312
- **null_percent**: 13.8052
- **unique_count**: 33
- **dominant_value_ratio**: 0.3348
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: False
- **warnings**:
- **top_values**:
  - `Developer, full-stack`: 25735
  - `Developer, back-end`: 13745
  - `Developer, front-end`: 5071
  - `Developer, desktop or enterprise applications`: 3904
  - `Other (please specify):`: 3080

### EdLevel

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 1211
- **null_percent**: 1.3579
- **unique_count**: 8
- **dominant_value_ratio**: 0.4172
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: False
- **warnings**:
- **top_values**:
  - `Bachelor’s degree (B.A., B.S., B.Eng., etc.)`: 36706
  - `Master’s degree (M.A., M.S., M.Eng., MBA, etc.)`: 20543
  - `Some college/university study without earning a degree`: 11753
  - `Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)`: 8897
  - `Professional degree (JD, MD, Ph.D, Ed.D, etc.)`: 3887

### Employment

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 1286
- **null_percent**: 1.442
- **unique_count**: 106
- **dominant_value_ratio**: 0.6115
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: False
- **warnings**:
- **top_values**:
  - `Employed, full-time`: 53748
  - `Student, full-time`: 7430
  - `Independent contractor, freelancer, or self-employed`: 7076
  - `Employed, full-time;Independent contractor, freelancer, or self-employed`: 4354
  - `Not employed, but looking for work`: 2553

### Frequency_1

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 47268
- **null_percent**: 53.0005
- **unique_count**: 5
- **dominant_value_ratio**: 0.609
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'Frequency_1' has high missing values (53.0%).
- **top_values**:
  - `1-2 times a week`: 25528
  - `Never`: 10707
  - `3-5 times a week`: 4100
  - `6-10 times a week`: 847
  - `10+ times a week`: 734

### Frequency_2

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 47259
- **null_percent**: 52.9904
- **unique_count**: 5
- **dominant_value_ratio**: 0.4515
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'Frequency_2' has high missing values (52.99%).
- **top_values**:
  - `1-2 times a week`: 18930
  - `3-5 times a week`: 9809
  - `10+ times a week`: 4794
  - `6-10 times a week`: 4383
  - `Never`: 4009

### Frequency_3

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 48130
- **null_percent**: 53.9671
- **unique_count**: 5
- **dominant_value_ratio**: 0.523
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'Frequency_3' has high missing values (53.97%).
- **top_values**:
  - `1-2 times a week`: 21470
  - `Never`: 12107
  - `3-5 times a week`: 5125
  - `6-10 times a week`: 1280
  - `10+ times a week`: 1072

### ICorPM

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 45516
- **null_percent**: 51.0361
- **unique_count**: 2
- **dominant_value_ratio**: 0.863
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'ICorPM' has high missing values (51.04%).
- **top_values**:
  - `Individual contributor`: 37685
  - `People manager`: 5983

### Industry

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 52410
- **null_percent**: 58.7661
- **unique_count**: 12
- **dominant_value_ratio**: 0.4938
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'Industry' has high missing values (58.77%).
- **top_values**:
  - `Information Services, IT, Software Development, or other Technology`: 18159
  - `Financial Services`: 4421
  - `Other`: 4011
  - `Manufacturing, Transportation, or Supply Chain`: 2607
  - `Healthcare`: 2216

### Knowledge_1

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 46649
- **null_percent**: 52.3065
- **unique_count**: 5
- **dominant_value_ratio**: 0.4658
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'Knowledge_1' has high missing values (52.31%).
- **top_values**:
  - `Agree`: 19812
  - `Strongly agree`: 15502
  - `Neither agree nor disagree`: 3593
  - `Disagree`: 2603
  - `Strongly disagree`: 1025

### Knowledge_2

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 47514
- **null_percent**: 53.2764
- **unique_count**: 5
- **dominant_value_ratio**: 0.3231
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'Knowledge_2' has high missing values (53.28%).
- **top_values**:
  - `Agree`: 13464
  - `Neither agree nor disagree`: 10636
  - `Disagree`: 9186
  - `Strongly agree`: 5220
  - `Strongly disagree`: 3164

### Knowledge_3

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 47386
- **null_percent**: 53.1328
- **unique_count**: 5
- **dominant_value_ratio**: 0.4035
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'Knowledge_3' has high missing values (53.13%).
- **top_values**:
  - `Agree`: 16865
  - `Neither agree nor disagree`: 11096
  - `Disagree`: 7786
  - `Strongly agree`: 4056
  - `Strongly disagree`: 1995

### Knowledge_4

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 47500
- **null_percent**: 53.2607
- **unique_count**: 5
- **dominant_value_ratio**: 0.4553
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'Knowledge_4' has high missing values (53.26%).
- **top_values**:
  - `Agree`: 18978
  - `Neither agree nor disagree`: 10715
  - `Disagree`: 6029
  - `Strongly agree`: 4756
  - `Strongly disagree`: 1206

### Knowledge_5

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 47657
- **null_percent**: 53.4367
- **unique_count**: 5
- **dominant_value_ratio**: 0.5329
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'Knowledge_5' has high missing values (53.44%).
- **top_values**:
  - `Agree`: 22131
  - `Neither agree nor disagree`: 7579
  - `Strongly agree`: 7235
  - `Disagree`: 3805
  - `Strongly disagree`: 777

### Knowledge_6

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 47664
- **null_percent**: 53.4446
- **unique_count**: 5
- **dominant_value_ratio**: 0.3654
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'Knowledge_6' has high missing values (53.44%).
- **top_values**:
  - `Agree`: 15171
  - `Neither agree nor disagree`: 11353
  - `Disagree`: 8576
  - `Strongly agree`: 5128
  - `Strongly disagree`: 1292

### Knowledge_7

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 47717
- **null_percent**: 53.504
- **unique_count**: 5
- **dominant_value_ratio**: 0.3776
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'Knowledge_7' has high missing values (53.5%).
- **top_values**:
  - `Agree`: 15659
  - `Neither agree nor disagree`: 9938
  - `Disagree`: 7843
  - `Strongly agree`: 6501
  - `Strongly disagree`: 1526

### Knowledge_8

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 47780
- **null_percent**: 53.5746
- **unique_count**: 5
- **dominant_value_ratio**: 0.3968
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'Knowledge_8' has high missing values (53.57%).
- **top_values**:
  - `Agree`: 16430
  - `Neither agree nor disagree`: 10958
  - `Disagree`: 7007
  - `Strongly agree`: 4606
  - `Strongly disagree`: 2403

### LanguageHaveWorkedWith

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 2044
- **null_percent**: 2.2919
- **unique_count**: 32641
- **dominant_value_ratio**: 0.0171
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: False
- **warnings**:
- **top_values**:
  - `HTML/CSS;JavaScript;TypeScript`: 1487
  - `Python`: 1132
  - `HTML/CSS;JavaScript`: 735
  - `HTML/CSS;JavaScript;PHP;SQL`: 718
  - `C#`: 649

### LanguageWantToWorkWith

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 8475
- **null_percent**: 9.5028
- **unique_count**: 29602
- **dominant_value_ratio**: 0.0178
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: False
- **warnings**:
- **top_values**:
  - `Rust`: 1438
  - `Python`: 1182
  - `HTML/CSS;JavaScript;TypeScript`: 1071
  - `C#`: 736
  - `Go`: 618

### LearnCode

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 1521
- **null_percent**: 1.7055
- **unique_count**: 790
- **dominant_value_ratio**: 0.0556
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: False
- **warnings**:
- **top_values**:
  - `Other online resources (e.g., videos, blogs, forum)`: 4873
  - `Books / Physical media;Other online resources (e.g., videos, blogs, forum)`: 3300
  - `Other online resources (e.g., videos, blogs, forum);School (i.e., University, College, etc)`: 3070
  - `Books / Physical media;Online Courses or Certification;Other online resources (e.g., videos, blogs, forum)`: 3024
  - `Online Courses or Certification;Other online resources (e.g., videos, blogs, forum)`: 2871

### LearnCodeCoursesCert

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 52108
- **null_percent**: 58.4275
- **unique_count**: 210
- **dominant_value_ratio**: 0.2008
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'LearnCodeCoursesCert' has high missing values (58.43%).
- **top_values**:
  - `Udemy`: 7445
  - `Other`: 3230
  - `Udemy;Coursera`: 2612
  - `Udemy;Pluralsight`: 1958
  - `Codecademy;Udemy`: 1837

### LearnCodeOnline

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 19100
- **null_percent**: 21.4164
- **unique_count**: 7940
- **dominant_value_ratio**: 0.0169
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: False
- **warnings**:
- **top_values**:
  - `Formal documentation provided by the owner of the tech;Blogs with tips and tricks;Written Tutorials;Click to write Choice 20;Stack Overflow`: 1182
  - `Formal documentation provided by the owner of the tech;Blogs with tips and tricks;Written Tutorials;Stack Overflow`: 977
  - `Formal documentation provided by the owner of the tech;Blogs with tips and tricks;Stack Overflow`: 802
  - `Formal documentation provided by the owner of the tech;Blogs with tips and tricks;How-to videos;Written Tutorials;Click to write Choice 20;Stack Overflow`: 770
  - `Formal documentation provided by the owner of the tech;Blogs with tips and tricks;Books;Written Tutorials;Click to write Choice 20;Stack Overflow`: 768

### MainBranch

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 0
- **null_percent**: 0
- **unique_count**: 6
- **dominant_value_ratio**: 0.7539
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: False
- **warnings**:
- **top_values**:
  - `I am a developer by profession`: 67237
  - `I am not primarily a developer, but I write code sometimes as part of my work/studies`: 8954
  - `I am learning to code`: 4961
  - `I code primarily as a hobby`: 4960
  - `I used to be a developer by profession, but no longer am`: 1861

### MiscTechHaveWorkedWith

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 32165
- **null_percent**: 36.0659
- **unique_count**: 10322
- **dominant_value_ratio**: 0.0676
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'MiscTechHaveWorkedWith' has high missing values (36.07%).
- **top_values**:
  - `.NET (5+) ;.NET Framework (1.0 - 4.8)`: 3854
  - `.NET (5+) `: 3663
  - `Spring Framework`: 2179
  - `Flutter`: 1614
  - `React Native`: 1613

### MiscTechWantToWorkWith

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 42336
- **null_percent**: 47.4704
- **unique_count**: 11775
- **dominant_value_ratio**: 0.0765
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'MiscTechWantToWorkWith' has high missing values (47.47%).
- **top_values**:
  - `.NET (5+) `: 3582
  - `Flutter`: 1353
  - `Spring Framework`: 1173
  - `.NET (5+) ;.NET Framework (1.0 - 4.8)`: 1079
  - `React Native`: 967

### NEWCollabToolsHaveWorkedWith

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 3320
- **null_percent**: 3.7226
- **unique_count**: 21262
- **dominant_value_ratio**: 0.102
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: False
- **warnings**:
- **top_values**:
  - `Visual Studio Code`: 8754
  - `Visual Studio;Visual Studio Code`: 3430
  - `Notepad++;Visual Studio;Visual Studio Code`: 2167
  - `IntelliJ IDEA;Visual Studio Code`: 1654
  - `Vim;Visual Studio Code`: 1602

### NEWCollabToolsWantToWorkWith

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 12535
- **null_percent**: 14.0552
- **unique_count**: 13659
- **dominant_value_ratio**: 0.133
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: False
- **warnings**:
- **top_values**:
  - `Visual Studio Code`: 10193
  - `Visual Studio;Visual Studio Code`: 3145
  - `Neovim`: 2309
  - `Notepad++;Visual Studio;Visual Studio Code`: 1674
  - `Vim;Visual Studio Code`: 1667

### NEWSOSites

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 1211
- **null_percent**: 1.3579
- **unique_count**: 16
- **dominant_value_ratio**: 0.5828
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: False
- **warnings**:
- **top_values**:
  - `Stack Overflow;Stack Exchange`: 51270
  - `Stack Overflow`: 25606
  - `Stack Overflow;Stack Exchange;Collectives on Stack Overflow`: 4119
  - `Stack Overflow;Stack Exchange;Stack Overflow for Teams (private knowledge sharing & collaboration platform for companies)`: 2239
  - `Stack Overflow;Collectives on Stack Overflow`: 1045

### OfficeStackAsyncHaveWorkedWith

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 20094
- **null_percent**: 22.5309
- **unique_count**: 6258
- **dominant_value_ratio**: 0.0841
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: False
- **warnings**:
- **top_values**:
  - `Jira`: 5810
  - `Confluence;Jira`: 5779
  - `Markdown File`: 2500
  - `Azure Devops`: 2446
  - `GitHub Discussions`: 2044

### OfficeStackAsyncWantToWorkWith

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 35441
- **null_percent**: 39.7392
- **unique_count**: 3754
- **dominant_value_ratio**: 0.0831
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'OfficeStackAsyncWantToWorkWith' has high missing values (39.74%).
- **top_values**:
  - `Jira`: 4467
  - `Markdown File`: 3699
  - `Confluence;Jira`: 3630
  - `Azure Devops`: 2548
  - `GitHub Discussions`: 2255

### OfficeStackSyncHaveWorkedWith

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 5745
- **null_percent**: 6.4417
- **unique_count**: 6925
- **dominant_value_ratio**: 0.0841
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: False
- **warnings**:
- **top_values**:
  - `Microsoft Teams`: 7018
  - `Slack;Zoom`: 2631
  - `Discord`: 2614
  - `Microsoft Teams;Slack`: 2309
  - `Slack`: 2308

### OfficeStackSyncWantToWorkWith

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 19408
- **null_percent**: 21.7618
- **unique_count**: 4078
- **dominant_value_ratio**: 0.083
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: False
- **warnings**:
- **top_values**:
  - `Microsoft Teams`: 5790
  - `Slack`: 4903
  - `Discord`: 4557
  - `Google Meet;Slack`: 2770
  - `Slack;Zoom`: 2701

### OpSysPersonal use

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 2627
- **null_percent**: 2.9456
- **unique_count**: 3050
- **dominant_value_ratio**: 0.2044
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: False
- **warnings**:
- **top_values**:
  - `Windows`: 17688
  - `MacOS`: 10022
  - `Ubuntu`: 4137
  - `Windows;Windows Subsystem for Linux (WSL)`: 3436
  - `Ubuntu;Windows`: 3259

### OpSysProfessional use

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 10597
- **null_percent**: 11.8822
- **unique_count**: 2470
- **dominant_value_ratio**: 0.2029
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: False
- **warnings**:
- **top_values**:
  - `Windows`: 15943
  - `MacOS`: 12928
  - `Ubuntu`: 5201
  - `Windows;Windows Subsystem for Linux (WSL)`: 3934
  - `Ubuntu;Windows`: 2795

### OrgSize

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 24141
- **null_percent**: 27.0688
- **unique_count**: 10
- **dominant_value_ratio**: 0.2057
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: False
- **warnings**:
- **top_values**:
  - `20 to 99 employees`: 13380
  - `100 to 499 employees`: 12218
  - `10,000 or more employees`: 7929
  - `1,000 to 4,999 employees`: 7235
  - `2 to 9 employees`: 6439

### PlatformHaveWorkedWith

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 25556
- **null_percent**: 28.6554
- **unique_count**: 5920
- **dominant_value_ratio**: 0.1541
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: False
- **warnings**:
- **top_values**:
  - `Amazon Web Services (AWS)`: 9804
  - `Microsoft Azure`: 5945
  - `Google Cloud`: 2495
  - `Amazon Web Services (AWS);Microsoft Azure`: 2192
  - `Amazon Web Services (AWS);Google Cloud`: 1810

### PlatformWantToWorkWith

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 37876
- **null_percent**: 42.4695
- **unique_count**: 4963
- **dominant_value_ratio**: 0.1417
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'PlatformWantToWorkWith' has high missing values (42.47%).
- **top_values**:
  - `Amazon Web Services (AWS)`: 7269
  - `Microsoft Azure`: 4239
  - `Amazon Web Services (AWS);Microsoft Azure`: 2023
  - `Google Cloud`: 1885
  - `Amazon Web Services (AWS);Google Cloud`: 1695

### ProfessionalTech

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 47401
- **null_percent**: 53.1497
- **unique_count**: 284
- **dominant_value_ratio**: 0.1166
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'ProfessionalTech' has high missing values (53.15%).
- **top_values**:
  - `None of these`: 4871
  - `DevOps function;Microservices;Automated testing;Observability tools;Developer portal or other central places to find tools/services;Continuous integration (CI) and (more often) continuous delivery`: 2618
  - `DevOps function;Microservices;Automated testing;Observability tools;Continuous integration (CI) and (more often) continuous delivery`: 2271
  - `DevOps function;Microservices;Automated testing;Continuous integration (CI) and (more often) continuous delivery`: 1656
  - `DevOps function;Automated testing;Continuous integration (CI) and (more often) continuous delivery`: 1524

### PurchaseInfluence

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 24220
- **null_percent**: 27.1573
- **unique_count**: 3
- **dominant_value_ratio**: 0.4126
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: False
- **warnings**:
- **top_values**:
  - `I have some influence`: 26805
  - `I have little or no influence`: 22734
  - `I have a great deal of influence`: 15425

### Q120

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 0
- **null_percent**: 0
- **unique_count**: 1
- **dominant_value_ratio**: 1
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'Q120' has a single unique value (no predictive power).
- **top_values**:
  - `I agree`: 89184

### RemoteWork

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 15374
- **null_percent**: 17.2385
- **unique_count**: 3
- **dominant_value_ratio**: 0.4218
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: False
- **warnings**:
- **top_values**:
  - `Hybrid (some remote, some in-person)`: 31131
  - `Remote`: 30566
  - `In-person`: 12113

### ResponseId

- **dtype**: int64
- **inferred_dtype**: integer
- **null_count**: 0
- **null_percent**: 0
- **unique_count**: 89184
- **mean**: 44592.5
- **median**: 44592.5
- **std**: 25745.3475
- **min**: 1
- **q1**: 22296.75
- **q3**: 66888.25
- **max**: 89184
- **dominant_value_ratio**: 0
- **zero_ratio**: 0
- **is_id_like**: True
- **is_sparse**: False
- **flags**:
  - id_like
- **warnings**:
  - Column 'ResponseId' is high cardinality (unique/rows = 1.00); likely an ID column.
- **Outlier Detection Results**:
  - **IQR Method**: 0 outliers (0.00%)
  - **Z-Score Method**: 0 outliers (0.00%)
  - **Modified Z-Score**: 0 outliers (0.00%)
  - **Consensus**: 8901 avg outliers (9.98%)

### SOAccount

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 1332
- **null_percent**: 1.4935
- **unique_count**: 3
- **dominant_value_ratio**: 0.7545
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: False
- **warnings**:
- **top_values**:
  - `Yes`: 66282
  - `No`: 14618
  - `Not sure/can't remember`: 6952

### SOAI

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 41326
- **null_percent**: 46.3379
- **unique_count**: 43061
- **dominant_value_ratio**: 0.0044
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'SOAI' has high missing values (46.34%).
- **top_values**:
  - `No opinion`: 210
  - `Yes`: 194
  - `Good`: 154
  - `yes`: 133
  - `good`: 100

### SOComm

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 1492
- **null_percent**: 1.6729
- **unique_count**: 6
- **dominant_value_ratio**: 0.3318
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: False
- **warnings**:
- **top_values**:
  - `No, not really`: 29100
  - `Neutral`: 19033
  - `Yes, somewhat`: 19026
  - `No, not at all`: 11598
  - `Yes, definitely`: 7996

### SOPartFreq

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 23123
- **null_percent**: 25.9273
- **unique_count**: 6
- **dominant_value_ratio**: 0.5247
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: False
- **warnings**:
- **top_values**:
  - `Less than once per month or monthly`: 34661
  - `I have never participated in Q&A on Stack Overflow`: 16961
  - `A few times per month or weekly`: 9160
  - `A few times per week`: 3285
  - `Daily or almost daily`: 1309

### SOVisitFreq

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 2044
- **null_percent**: 2.2919
- **unique_count**: 5
- **dominant_value_ratio**: 0.3223
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: False
- **warnings**:
- **top_values**:
  - `A few times per week`: 28085
  - `Daily or almost daily`: 22124
  - `A few times per month or weekly`: 20312
  - `Multiple times per day`: 11952
  - `Less than once per month or monthly`: 4667

### SurveyEase

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 2630
- **null_percent**: 2.949
- **unique_count**: 3
- **dominant_value_ratio**: 0.625
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: False
- **warnings**:
- **top_values**:
  - `Easy`: 54092
  - `Neither easy nor difficult`: 31088
  - `Difficult`: 1374

### SurveyLength

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 2699
- **null_percent**: 3.0263
- **unique_count**: 3
- **dominant_value_ratio**: 0.7627
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: False
- **warnings**:
- **top_values**:
  - `Appropriate in length`: 65962
  - `Too long`: 18605
  - `Too short`: 1918

### TBranch

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 23416
- **null_percent**: 26.2558
- **unique_count**: 2
- **dominant_value_ratio**: 0.6671
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: False
- **warnings**:
- **top_values**:
  - `Yes`: 43872
  - `No`: 21896

### TechList

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 28333
- **null_percent**: 31.7692
- **unique_count**: 3
- **dominant_value_ratio**: 0.8087
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'TechList' has high missing values (31.77%).
- **top_values**:
  - `Investigate`: 49212
  - `Given a list`: 7935
  - `Other`: 3704

### TimeAnswering

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 46555
- **null_percent**: 52.2011
- **unique_count**: 5
- **dominant_value_ratio**: 0.3209
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'TimeAnswering' has high missing values (52.2%).
- **top_values**:
  - `15-30 minutes a day`: 13678
  - `30-60 minutes a day`: 13013
  - `Less than 15 minutes a day`: 8321
  - `60-120 minutes a day`: 5674
  - `Over 120 minutes a day`: 1943

### TimeSearching

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 46406
- **null_percent**: 52.034
- **unique_count**: 5
- **dominant_value_ratio**: 0.3819
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'TimeSearching' has high missing values (52.03%).
- **top_values**:
  - `30-60 minutes a day`: 16338
  - `15-30 minutes a day`: 11773
  - `60-120 minutes a day`: 7626
  - `Less than 15 minutes a day`: 3959
  - `Over 120 minutes a day`: 3082

### ToolsTechHaveWorkedWith

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 11300
- **null_percent**: 12.6704
- **unique_count**: 33133
- **dominant_value_ratio**: 0.0162
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: False
- **warnings**:
- **top_values**:
  - `Visual Studio Solution`: 1264
  - `Docker`: 1200
  - `npm`: 1166
  - `Pip`: 935
  - `Maven (build tool)`: 556

### ToolsTechWantToWorkWith

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 20869
- **null_percent**: 23.3999
- **unique_count**: 27456
- **dominant_value_ratio**: 0.0195
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: False
- **warnings**:
- **top_values**:
  - `Docker`: 1331
  - `Visual Studio Solution`: 960
  - `npm`: 880
  - `Cargo`: 817
  - `Docker;Kubernetes`: 667

### WebframeHaveWorkedWith

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 22246
- **null_percent**: 24.9439
- **unique_count**: 15144
- **dominant_value_ratio**: 0.0301
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: False
- **warnings**:
- **top_values**:
  - `React`: 2017
  - `Spring Boot`: 1479
  - `Node.js`: 1452
  - `Node.js;React`: 1161
  - `Flask`: 1069

### WebframeWantToWorkWith

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 32443
- **null_percent**: 36.3776
- **unique_count**: 14620
- **dominant_value_ratio**: 0.0275
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'WebframeWantToWorkWith' has high missing values (36.38%).
- **top_values**:
  - `React`: 1561
  - `Spring Boot`: 1200
  - `Node.js`: 973
  - `ASP.NET CORE`: 841
  - `Svelte`: 840

### WorkExp

- **dtype**: float64
- **inferred_dtype**: floating
- **null_count**: 45605
- **null_percent**: 51.1359
- **unique_count**: 51
- **mean**: 11.4051
- **median**: 9
- **std**: 9.052
- **min**: 0
- **q1**: 5
- **q3**: 16
- **max**: 50
- **dominant_value_ratio**: 0.0757
- **zero_ratio**: 0.006
- **is_id_like**: False
- **is_sparse**: True
- **flags**:
  - sparse
- **warnings**:
  - Column 'WorkExp' has high missing values (51.14%).
- **Outlier Detection Results**:
  - **IQR Method**: 1463 outliers (3.36%)
    - Bounds: [-11.50, 32.50]
    - Sample: 39.00, 38.00, 40.00, 34.00, 35.00...
  - **Z-Score Method**: 592 outliers (1.36%)
  - **Modified Z-Score**: 1189 outliers (2.73%)
  - **Consensus**: 1479 avg outliers (3.39%)

### YearsCode

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 1749
- **null_percent**: 1.9611
- **unique_count**: 52
- **dominant_value_ratio**: 0.0746
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: False
- **warnings**:
- **top_values**:
  - `10`: 6521
  - `5`: 5415
  - `6`: 4893
  - `8`: 4879
  - `7`: 4800

### YearsCodePro

- **dtype**: str
- **inferred_dtype**: string
- **null_count**: 23048
- **null_percent**: 25.8432
- **unique_count**: 52
- **dominant_value_ratio**: 0.0725
- **zero_ratio**: None
- **is_id_like**: False
- **is_sparse**: False
- **warnings**:
- **top_values**:
  - `5`: 4792
  - `10`: 4594
  - `2`: 4464
  - `3`: 4378
  - `4`: 3970

