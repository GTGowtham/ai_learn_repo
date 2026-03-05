import os
import logging
from typing import Dict, Any, Optional, List, Tuple
import re
import warnings

import pandas as pd
import numpy as np
from pandas.api import types as ptypes


class OutlierDetectionEngine:
    """
    Comprehensive outlier detection using multiple methods:
    1. IQR (Interquartile Range) Method
    2. Z-Score Method
    3. Modified Z-Score (MAD - Median Absolute Deviation)
    4. Isolation Forest (if scikit-learn available)
    5. Statistical tests for specific distributions
    """
    
    def __init__(self):
        self.methods_available = ['iqr', 'zscore', 'modified_zscore']
        try:
            from sklearn.ensemble import IsolationForest
            self.methods_available.append('isolation_forest')
            self._IsolationForest = IsolationForest
        except ImportError:
            self._IsolationForest = None
            logging.warning("scikit-learn not available. Isolation Forest method disabled.")
    
    def detect_outliers_iqr(self, series: pd.Series, multiplier: float = 1.5) -> Dict[str, Any]:
        """IQR Method: Values outside [Q1 - multiplier*IQR, Q3 + multiplier*IQR]"""
        clean_series = series.dropna()
        if len(clean_series) == 0:
            return self._empty_result()
        
        Q1 = clean_series.quantile(0.25)
        Q3 = clean_series.quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - multiplier * IQR
        upper_bound = Q3 + multiplier * IQR
        
        outlier_mask = (clean_series < lower_bound) | (clean_series > upper_bound)
        outliers = clean_series[outlier_mask]
        
        return {
            'method': 'iqr',
            'outlier_count': int(len(outliers)),
            'outlier_percent': float(len(outliers) / len(clean_series) * 100),
            'lower_bound': float(lower_bound),
            'upper_bound': float(upper_bound),
            'Q1': float(Q1),
            'Q3': float(Q3),
            'IQR': float(IQR),
            'outlier_values': list(outliers.head(10).values),
            'has_outliers': len(outliers) > 0
        }
    
    def detect_outliers_zscore(self, series: pd.Series, threshold: float = 3.0) -> Dict[str, Any]:
        """Z-Score Method: Values with |z-score| > threshold"""
        clean_series = series.dropna()
        if len(clean_series) < 2:
            return self._empty_result()
        
        mean = clean_series.mean()
        std = clean_series.std()
        
        if std == 0:
            return self._empty_result()
        
        z_scores = np.abs((clean_series - mean) / std)
        outlier_mask = z_scores > threshold
        outliers = clean_series[outlier_mask]
        
        return {
            'method': 'zscore',
            'outlier_count': int(len(outliers)),
            'outlier_percent': float(len(outliers) / len(clean_series) * 100),
            'threshold': float(threshold),
            'mean': float(mean),
            'std': float(std),
            'max_zscore': float(z_scores.max()),
            'outlier_values': list(outliers.head(10).values),
            'has_outliers': len(outliers) > 0
        }
    
    def detect_outliers_modified_zscore(self, series: pd.Series, threshold: float = 3.5) -> Dict[str, Any]:
        """Modified Z-Score using MAD (Median Absolute Deviation)"""
        clean_series = series.dropna()
        if len(clean_series) < 2:
            return self._empty_result()
        
        median = clean_series.median()
        mad = np.median(np.abs(clean_series - median))
        
        if mad == 0:
            return self._empty_result()
        
        modified_z_scores = 0.6745 * (clean_series - median) / mad
        outlier_mask = np.abs(modified_z_scores) > threshold
        outliers = clean_series[outlier_mask]
        
        return {
            'method': 'modified_zscore',
            'outlier_count': int(len(outliers)),
            'outlier_percent': float(len(outliers) / len(clean_series) * 100),
            'threshold': float(threshold),
            'median': float(median),
            'mad': float(mad),
            'max_modified_zscore': float(np.abs(modified_z_scores).max()),
            'outlier_values': list(outliers.head(10).values),
            'has_outliers': len(outliers) > 0
        }
    
    def detect_outliers_isolation_forest(self, series: pd.Series, contamination: float = 0.1) -> Dict[str, Any]:
        """Isolation Forest Method: Machine learning approach"""
        if self._IsolationForest is None:
            return {'method': 'isolation_forest', 'error': 'scikit-learn not available'}
        
        clean_series = series.dropna()
        if len(clean_series) < 10:
            return self._empty_result()
        
        try:
            X = clean_series.values.reshape(-1, 1)
            clf = self._IsolationForest(contamination=contamination, random_state=42)
            predictions = clf.fit_predict(X)
            
            outlier_mask = predictions == -1
            outliers = clean_series[outlier_mask]
            
            return {
                'method': 'isolation_forest',
                'outlier_count': int(len(outliers)),
                'outlier_percent': float(len(outliers) / len(clean_series) * 100),
                'contamination': float(contamination),
                'outlier_values': list(outliers.head(10).values),
                'has_outliers': len(outliers) > 0
            }
        except Exception as e:
            logging.warning(f"Isolation Forest failed: {e}")
            return {'method': 'isolation_forest', 'error': str(e)}
    
    def detect_all(self, series: pd.Series, methods: Optional[List[str]] = None) -> Dict[str, Any]:
        """Run all available outlier detection methods"""
        if methods is None:
            methods = self.methods_available
        
        results = {}
        
        if 'iqr' in methods:
            results['iqr'] = self.detect_outliers_iqr(series)
            results['iqr_extreme'] = self.detect_outliers_iqr(series, multiplier=3.0)
        
        if 'zscore' in methods:
            results['zscore'] = self.detect_outliers_zscore(series)
        
        if 'modified_zscore' in methods:
            results['modified_zscore'] = self.detect_outliers_modified_zscore(series)
        
        if 'isolation_forest' in methods and self._IsolationForest is not None:
            results['isolation_forest'] = self.detect_outliers_isolation_forest(series)
        
        consensus = self._calculate_consensus(series, results)
        results['consensus'] = consensus
        
        return results
    
    def _calculate_consensus(self, series: pd.Series, results: Dict) -> Dict[str, Any]:
        """Calculate consensus across multiple detection methods"""
        clean_series = series.dropna()
        if len(clean_series) == 0:
            return self._empty_result()
        
        outlier_sets = []
        for method_name, method_result in results.items():
            if isinstance(method_result, dict) and method_result.get('has_outliers'):
                outlier_sets.append(method_result.get('outlier_count', 0))
        
        if not outlier_sets:
            return {'method': 'consensus', 'outlier_count': 0, 'has_outliers': False}
        
        avg_outlier_count = int(np.mean(outlier_sets))
        
        return {
            'method': 'consensus',
            'outlier_count': avg_outlier_count,
            'outlier_percent': float(avg_outlier_count / len(clean_series) * 100),
            'methods_agreeing': len([x for x in outlier_sets if x > 0]),
            'total_methods': len(outlier_sets),
            'has_outliers': avg_outlier_count > 0
        }
    
    def _empty_result(self) -> Dict[str, Any]:
        """Return empty result structure"""
        return {
            'outlier_count': 0,
            'outlier_percent': 0.0,
            'has_outliers': False,
            'outlier_values': []
        }


class CorrelationAnalyzer:
    """
    Analyze correlations between features and detect multicollinearity
    """
    
    def analyze(self, df: pd.DataFrame, threshold: float = 0.8) -> Dict[str, Any]:
        """
        Perform correlation analysis
        
        Args:
            df: DataFrame with numeric columns
            threshold: Correlation threshold for high correlation warning
        
        Returns:
            Dictionary with correlation results
        """
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) < 2:
            return {
                'correlation_matrix': {},
                'high_correlations': [],
                'multicollinearity_groups': [],
                'summary': 'Insufficient numeric columns for correlation analysis'
            }
        
        # Calculate correlation matrix
        corr_matrix = df[numeric_cols].corr()
        
        # Find high correlations (excluding diagonal)
        high_corrs = []
        seen_pairs = set()
        
        for i, col1 in enumerate(numeric_cols):
            for j, col2 in enumerate(numeric_cols):
                if i < j:  # Upper triangle only
                    corr_val = corr_matrix.loc[col1, col2]
                    if abs(corr_val) >= threshold:
                        pair = tuple(sorted([col1, col2]))
                        if pair not in seen_pairs:
                            high_corrs.append({
                                'feature_1': col1,
                                'feature_2': col2,
                                'correlation': float(corr_val),
                                'abs_correlation': float(abs(corr_val)),
                                'type': 'positive' if corr_val > 0 else 'negative'
                            })
                            seen_pairs.add(pair)
        
        # Sort by absolute correlation
        high_corrs.sort(key=lambda x: x['abs_correlation'], reverse=True)
        
        # Detect multicollinearity groups (VIF-like approach)
        multicollinearity_groups = self._detect_multicollinearity_groups(corr_matrix, threshold)
        
        # Convert correlation matrix to dict
        corr_dict = {}
        for col in numeric_cols:
            corr_dict[col] = {c: float(corr_matrix.loc[col, c]) for c in numeric_cols}
        
        return {
            'correlation_matrix': corr_dict,
            'high_correlations': high_corrs,
            'high_correlation_count': len(high_corrs),
            'multicollinearity_groups': multicollinearity_groups,
            'numeric_columns_analyzed': len(numeric_cols),
            'threshold_used': threshold
        }
    
    def _detect_multicollinearity_groups(self, corr_matrix: pd.DataFrame, threshold: float) -> List[Dict]:
        """Detect groups of highly correlated features"""
        groups = []
        columns = corr_matrix.columns.tolist()
        visited = set()
        
        for col in columns:
            if col in visited:
                continue
            
            # Find all columns highly correlated with this one
            highly_correlated = []
            for other_col in columns:
                if col != other_col and abs(corr_matrix.loc[col, other_col]) >= threshold:
                    highly_correlated.append(other_col)
            
            if highly_correlated:
                group_members = [col] + highly_correlated
                # Calculate average correlation within group
                group_corrs = []
                for i, c1 in enumerate(group_members):
                    for c2 in group_members[i+1:]:
                        group_corrs.append(abs(corr_matrix.loc[c1, c2]))
                
                if group_corrs:
                    groups.append({
                        'members': group_members,
                        'size': len(group_members),
                        'avg_correlation': float(np.mean(group_corrs)),
                        'max_correlation': float(np.max(group_corrs))
                    })
                    visited.update(group_members)
        
        return sorted(groups, key=lambda x: x['size'], reverse=True)


class LeakageDetector:
    """
    Detect potential feature leakage issues
    """
    
    def detect(self, df: pd.DataFrame, target_col: Optional[str] = None) -> Dict[str, Any]:
        """
        Detect potential data leakage
        
        Args:
            df: DataFrame to analyze
            target_col: Target column name (if known)
        
        Returns:
            Dictionary with leakage detection results
        """
        leakage_warnings = []
        
        # 1. Perfect correlation detection
        if target_col and target_col in df.columns:
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if target_col in numeric_cols:
                for col in numeric_cols:
                    if col != target_col:
                        try:
                            corr = df[[col, target_col]].corr().iloc[0, 1]
                            if abs(corr) > 0.99:
                                leakage_warnings.append({
                                    'type': 'perfect_correlation',
                                    'column': col,
                                    'target': target_col,
                                    'correlation': float(corr),
                                    'severity': 'HIGH',
                                    'description': f'Near-perfect correlation ({corr:.4f}) with target - likely leakage'
                                })
                        except:
                            pass
        
        # 2. Column name analysis - detect suspicious names
        suspicious_patterns = [
            (r'.*_after.*', 'temporal leakage - "after" in name'),
            (r'.*_future.*', 'temporal leakage - "future" in name'),
            (r'.*_next.*', 'temporal leakage - "next" in name'),
            (r'.*_result.*', 'possible outcome leakage'),
            (r'.*_actual.*', 'possible outcome leakage'),
            (r'.*_final.*', 'possible outcome leakage'),
            (r'.*_outcome.*', 'direct outcome leakage'),
            (r'.*_label.*', 'possible label leakage'),
            (r'.*_target.*', 'possible target leakage'),
        ]
        
        for col in df.columns:
            col_lower = str(col).lower()
            for pattern, reason in suspicious_patterns:
                if re.match(pattern, col_lower):
                    leakage_warnings.append({
                        'type': 'suspicious_name',
                        'column': col,
                        'pattern': pattern,
                        'severity': 'MEDIUM',
                        'description': reason
                    })
                    break
        
        # 3. Constant or near-constant features
        for col in df.columns:
            unique_count = df[col].nunique()
            if unique_count == 1:
                leakage_warnings.append({
                    'type': 'constant_feature',
                    'column': col,
                    'severity': 'LOW',
                    'description': 'Constant value - no information'
                })
            elif unique_count == len(df) and len(df) > 100:
                leakage_warnings.append({
                    'type': 'unique_identifier',
                    'column': col,
                    'severity': 'MEDIUM',
                    'description': 'Every row unique - possible ID or timestamp leakage'
                })
        
        # 4. Duplicate columns
        duplicate_groups = self._find_duplicate_columns(df)
        for group in duplicate_groups:
            leakage_warnings.append({
                'type': 'duplicate_columns',
                'columns': group,
                'severity': 'LOW',
                'description': 'Duplicate columns detected'
            })
        
        return {
            'leakage_warnings': leakage_warnings,
            'total_warnings': len(leakage_warnings),
            'high_severity': len([w for w in leakage_warnings if w['severity'] == 'HIGH']),
            'medium_severity': len([w for w in leakage_warnings if w['severity'] == 'MEDIUM']),
            'low_severity': len([w for w in leakage_warnings if w['severity'] == 'LOW']),
            'has_leakage_risk': len(leakage_warnings) > 0
        }
    
    def _find_duplicate_columns(self, df: pd.DataFrame) -> List[List[str]]:
        """Find groups of duplicate columns"""
        duplicate_groups = []
        checked = set()
        
        for i, col1 in enumerate(df.columns):
            if col1 in checked:
                continue
            
            duplicates = [col1]
            for col2 in df.columns[i+1:]:
                if col2 in checked:
                    continue
                try:
                    if df[col1].equals(df[col2]):
                        duplicates.append(col2)
                        checked.add(col2)
                except:
                    pass
            
            if len(duplicates) > 1:
                duplicate_groups.append(duplicates)
                checked.add(col1)
        
        return duplicate_groups


class TargetSuggester:
    """
    Suggest potential target variables based on column characteristics
    """
    
    def suggest(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Suggest potential target columns
        
        Returns:
            Dictionary with target suggestions
        """
        suggestions = []
        
        for col in df.columns:
            score = 0
            reasons = []
            
            # 1. Name-based scoring
            col_lower = str(col).lower()
            target_keywords = ['target', 'label', 'class', 'outcome', 'result', 'prediction', 
                              'churn', 'fraud', 'default', 'risk', 'price', 'sales', 'revenue']
            
            for keyword in target_keywords:
                if keyword in col_lower:
                    score += 30
                    reasons.append(f'Name contains "{keyword}"')
                    break
            
            # 2. Data type scoring
            dtype = df[col].dtype
            unique_count = df[col].nunique()
            total_count = len(df)
            
            # Binary classification candidate
            if unique_count == 2:
                score += 25
                reasons.append('Binary values (classification)')
            
            # Multi-class classification candidate
            elif 2 < unique_count <= 20 and unique_count / total_count < 0.05:
                score += 20
                reasons.append(f'{unique_count} classes (classification)')
            
            # Regression candidate
            elif ptypes.is_numeric_dtype(dtype):
                # Check if it's continuous
                if unique_count > 20:
                    score += 15
                    reasons.append('Continuous numeric (regression)')
            
            # 3. Position scoring (targets often at end)
            col_position = list(df.columns).index(col)
            if col_position == len(df.columns) - 1:
                score += 10
                reasons.append('Last column')
            elif col_position >= len(df.columns) - 3:
                score += 5
                reasons.append('Near end of columns')
            
            # 4. Null percentage (targets usually complete)
            null_pct = df[col].isna().mean() * 100
            if null_pct == 0:
                score += 5
                reasons.append('No missing values')
            elif null_pct > 50:
                score -= 20
                reasons.append(f'High missing values ({null_pct:.1f}%)')
            
            # 5. Check if it's not obviously a feature
            id_keywords = ['id', 'index', 'key', 'timestamp', 'date']
            is_id_like = any(kw in col_lower for kw in id_keywords)
            
            if is_id_like:
                score -= 30
                reasons.append('Likely an ID/timestamp')
            
            if score > 0:
                suggestions.append({
                    'column': col,
                    'score': score,
                    'reasons': reasons,
                    'unique_values': int(unique_count),
                    'data_type': str(dtype),
                    'null_percent': float(null_pct),
                    'task_type': self._infer_task_type(df[col])
                })
        
        # Sort by score
        suggestions.sort(key=lambda x: x['score'], reverse=True)
        
        return {
            'suggestions': suggestions[:5],  # Top 5
            'top_candidate': suggestions[0] if suggestions else None,
            'total_candidates': len(suggestions)
        }
    
    def _infer_task_type(self, series: pd.Series) -> str:
        """Infer ML task type from series"""
        unique_count = series.nunique()
        
        if unique_count == 2:
            return 'binary_classification'
        elif 2 < unique_count <= 20 and unique_count / len(series) < 0.05:
            return 'multi_class_classification'
        elif ptypes.is_numeric_dtype(series.dtype) and unique_count > 20:
            return 'regression'
        else:
            return 'unknown'


class DatasetScorer:
    """
    Score the overall quality of the dataset for ML
    """
    
    def score(self, summary: Dict[str, Any], df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate overall dataset quality score
        
        Returns:
            Dictionary with scoring results
        """
        scores = {}
        
        # 1. Completeness Score (0-25 points)
        total_cells = df.shape[0] * df.shape[1]
        missing_cells = df.isna().sum().sum()
        completeness = (1 - missing_cells / total_cells) * 25 if total_cells > 0 else 0
        scores['completeness'] = {
            'score': float(completeness),
            'max': 25,
            'percent': float((completeness / 25) * 100),
            'description': f'{(completeness/25)*100:.1f}% complete'
        }
        
        # 2. Data Quality Score (0-25 points)
        quality_score = 25
        warnings = summary.get('warnings', [])
        
        # Deduct for warnings
        quality_score -= min(len(warnings) * 2, 15)
        
        # Deduct for outliers
        outlier_summary = summary.get('outlier_summary', {})
        outlier_cols = outlier_summary.get('total_columns_with_outliers', 0)
        quality_score -= min(outlier_cols, 5)
        
        quality_score = max(quality_score, 0)
        scores['data_quality'] = {
            'score': float(quality_score),
            'max': 25,
            'percent': float((quality_score / 25) * 100),
            'description': f'{len(warnings)} warnings, {outlier_cols} columns with outliers'
        }
        
        # 3. Feature Quality Score (0-25 points)
        feature_score = 25
        
        # Check for high cardinality
        id_like = summary.get('diagnostics', {}).get('id_like_columns', [])
        feature_score -= min(len(id_like) * 3, 10)
        
        # Check for sparse columns
        sparse = summary.get('diagnostics', {}).get('sparse_columns', [])
        feature_score -= min(len(sparse) * 2, 10)
        
        feature_score = max(feature_score, 0)
        scores['feature_quality'] = {
            'score': float(feature_score),
            'max': 25,
            'percent': float((feature_score / 25) * 100),
            'description': f'{len(id_like)} ID columns, {len(sparse)} sparse columns'
        }
        
        # 4. ML Readiness Score (0-25 points)
        ml_score = 25
        
        # Check for leakage
        leakage_data = summary.get('leakage_detection', {})
        high_severity_leakage = leakage_data.get('high_severity', 0)
        ml_score -= high_severity_leakage * 10
        ml_score -= leakage_data.get('medium_severity', 0) * 3
        
        # Check for multicollinearity
        corr_data = summary.get('correlation_analysis', {})
        high_corr_count = corr_data.get('high_correlation_count', 0)
        ml_score -= min(high_corr_count * 2, 10)
        
        ml_score = max(ml_score, 0)
        scores['ml_readiness'] = {
            'score': float(ml_score),
            'max': 25,
            'percent': float((ml_score / 25) * 100),
            'description': f'{high_severity_leakage} leakage risks, {high_corr_count} high correlations'
        }
        
        # Total Score
        total_score = sum(s['score'] for s in scores.values())
        total_max = sum(s['max'] for s in scores.values())
        
        # Grade assignment
        percentage = (total_score / total_max) * 100
        if percentage >= 90:
            grade = 'A'
            quality = 'Excellent'
        elif percentage >= 80:
            grade = 'B'
            quality = 'Good'
        elif percentage >= 70:
            grade = 'C'
            quality = 'Fair'
        elif percentage >= 60:
            grade = 'D'
            quality = 'Poor'
        else:
            grade = 'F'
            quality = 'Critical Issues'
        
        return {
            'scores': scores,
            'total_score': float(total_score),
            'max_score': float(total_max),
            'percentage': float(percentage),
            'grade': grade,
            'quality': quality,
            'recommendations': self._generate_recommendations(scores, summary)
        }
    
    def _generate_recommendations(self, scores: Dict, summary: Dict) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Completeness recommendations
        if scores['completeness']['percent'] < 80:
            recommendations.append('⚠️ Handle missing values: Consider imputation or removal')
        
        # Quality recommendations
        if scores['data_quality']['percent'] < 70:
            warnings = summary.get('warnings', [])
            if warnings:
                recommendations.append(f'⚠️ Address {len(warnings)} data quality warnings')
            outlier_cols = summary.get('outlier_summary', {}).get('total_columns_with_outliers', 0)
            if outlier_cols > 0:
                recommendations.append(f'⚠️ Review and handle outliers in {outlier_cols} columns')
        
        # Feature quality recommendations
        if scores['feature_quality']['percent'] < 70:
            id_cols = summary.get('diagnostics', {}).get('id_like_columns', [])
            if id_cols:
                recommendations.append(f'⚠️ Remove {len(id_cols)} ID-like columns before training')
            sparse_cols = summary.get('diagnostics', {}).get('sparse_columns', [])
            if sparse_cols:
                recommendations.append(f'⚠️ Consider removing {len(sparse_cols)} sparse columns')
        
        # ML readiness recommendations
        if scores['ml_readiness']['percent'] < 70:
            leakage = summary.get('leakage_detection', {})
            if leakage.get('high_severity', 0) > 0:
                recommendations.append('🚨 CRITICAL: Address feature leakage before modeling')
            high_corr = summary.get('correlation_analysis', {}).get('high_correlation_count', 0)
            if high_corr > 5:
                recommendations.append(f'⚠️ Handle {high_corr} highly correlated features')
        
        if not recommendations:
            recommendations.append('✅ Dataset looks good! Ready for modeling')
        
        return recommendations


class CsvProfiler:
    """
    Ultimate CSV profiler with comprehensive EDA capabilities:
    - Outlier detection
    - Correlation analysis
    - Feature leakage detection
    - Target variable suggestion
    - Dataset quality scoring
    """

    def __init__(self, csv_path: str):
        self.csv_path: str = csv_path
        self.df: Optional[pd.DataFrame] = None
        self.outlier_engine = OutlierDetectionEngine()
        self.correlation_analyzer = CorrelationAnalyzer()
        self.leakage_detector = LeakageDetector()
        self.target_suggester = TargetSuggester()
        self.dataset_scorer = DatasetScorer()

    def load(self, **read_csv_kwargs) -> "CsvProfiler":
        """Load the CSV into a DataFrame"""
        try:
            self.df = pd.read_csv(self.csv_path, **read_csv_kwargs)
            logging.info("Loaded CSV '%s' with shape %s", self.csv_path, self.df.shape)
        except Exception as e:
            logging.exception("Failed to load CSV '%s': %s", self.csv_path, e)
            raise
        return self

    def profile(
        self,
        top_n: int = 3,
        coerce_numeric: bool = False,
        include_memory: bool = True,
        missing_threshold: float = 30.0,
        high_cardinality_ratio: float = 0.8,
        id_unique_ratio: float = 0.9,
        zero_sparse_threshold: float = 0.9,
        dominant_ratio_threshold: float = 0.95,
        numeric_like_ratio: float = 0.95,
        datetime_like_ratio: float = 0.95,
        # Outlier detection settings
        detect_outliers: bool = True,
        outlier_methods: Optional[List[str]] = None,
        outlier_iqr_multiplier: float = 1.5,
        outlier_zscore_threshold: float = 3.0,
        # NEW: EDA features
        analyze_correlations: bool = True,
        correlation_threshold: float = 0.8,
        detect_leakage: bool = True,
        suggest_target: bool = True,
        target_column: Optional[str] = None,
        score_dataset: bool = True,
    ) -> Dict[str, Any]:

        if self.df is None:
            raise ValueError("DataFrame is not loaded. Call .load() first.")

        total_rows_int = int(len(self.df))

        summary: Dict[str, Any] = {
            "file": os.path.basename(self.csv_path),
            "total_rows": total_rows_int,
            "total_columns": int(self.df.shape[1]),
            "columns": {},
            "warnings": [],
            "diagnostics": {
                "id_like_columns": [],
                "sparse_columns": [],
                "dtype_warnings": [],
                "outlier_columns": [],
            },
            "type_counts": {
                "numeric": 0,
                "categorical": 0,
                "datetime": 0,
                "boolean": 0,
                "object": 0,
            },
            "outlier_summary": {
                "total_columns_with_outliers": 0,
                "total_outliers_detected": 0,
                "methods_used": outlier_methods or self.outlier_engine.methods_available
            }
        }

        if include_memory:
            try:
                summary["memory_usage_bytes"] = int(self.df.memory_usage(deep=True).sum())
            except Exception:
                summary["memory_usage_bytes"] = None

        # Column profiling (existing code)
        uuid_re = re.compile(
            r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
        )
        id_keywords = ("id", "_id", "uuid", "guid", "key", "code","ID","_ID")

        for col in self.df.columns:
            s = self.df[col]
            col_info: Dict[str, Any] = {
                "dtype": str(s.dtype),
                "null_count": int(s.isna().sum()),
                "null_percent": float(s.isna().mean() * 100.0),
                "warnings": [],
            }

            numeric_series: Optional[pd.Series] = None
            if ptypes.is_numeric_dtype(s):
                numeric_series = s
            elif coerce_numeric:
                numeric_series = pd.to_numeric(s, errors="coerce")

            if numeric_series is not None and ptypes.is_numeric_dtype(numeric_series):
                nn = numeric_series.dropna()
                col_info.update({
                    "unique_count": int(s.nunique(dropna=True)),
                    "mean": float(nn.mean()) if not nn.empty else None,
                    "std": float(nn.std(ddof=1)) if len(nn) > 1 else None,
                    "min": float(nn.min()) if not nn.empty else None,
                    "max": float(nn.max()) if not nn.empty else None,
                    "median": float(nn.median()) if not nn.empty else None,
                    "q1": float(nn.quantile(0.25)) if not nn.empty else None,
                    "q3": float(nn.quantile(0.75)) if not nn.empty else None,
                })
                
                if detect_outliers and len(nn) >= 10:
                    outlier_results = self.outlier_engine.detect_all(numeric_series, methods=outlier_methods)
                    col_info["outliers"] = outlier_results
                    
                    has_outliers = any(
                        result.get('has_outliers', False) 
                        for result in outlier_results.values() 
                        if isinstance(result, dict)
                    )
                    
                    if has_outliers:
                        summary["outlier_summary"]["total_columns_with_outliers"] += 1
                        outlier_diagnostic = {
                            "column": col,
                            "methods_detected": [
                                method_name for method_name, result in outlier_results.items()
                                if isinstance(result, dict) and result.get('has_outliers', False)
                            ]
                        }
                        if 'iqr' in outlier_results:
                            outlier_diagnostic["outlier_count"] = outlier_results['iqr'].get('outlier_count', 0)
                            outlier_diagnostic["outlier_percent"] = outlier_results['iqr'].get('outlier_percent', 0)
                            summary["outlier_summary"]["total_outliers_detected"] += outlier_results['iqr'].get('outlier_count', 0)
                        
                        summary["diagnostics"]["outlier_columns"].append(outlier_diagnostic)
                        
                        if outlier_results.get('iqr', {}).get('outlier_percent', 0) > 5.0:
                            msg = f"Column '{col}' has significant outliers ({outlier_results['iqr']['outlier_percent']:.1f}% by IQR method)."
                            col_info["warnings"].append(msg)
                            summary["warnings"].append(msg)
            else:
                vc = s.value_counts(dropna=True).head(top_n)
                top_dict = {(str(k) if not pd.isna(k) else "<NA>"): int(v) for k, v in vc.items()}
                col_info.update({
                    "unique_count": int(s.nunique(dropna=True)),
                    "top_values": top_dict,
                })

            # Warnings and diagnostics (existing code continues...)
            if col_info["null_percent"] > missing_threshold:
                pct = round(col_info["null_percent"], 2)
                msg = f"Column '{col}' has high missing values ({pct}%)."
                col_info["warnings"].append(msg)
                summary["warnings"].append(msg)

            uniq = col_info.get("unique_count", 0)
            if total_rows_int > 0:
                ratio = uniq / total_rows_int
                if ratio > high_cardinality_ratio:
                    msg = f"Column '{col}' is high cardinality (unique/rows = {ratio:.2f}); likely an ID column."
                    col_info["warnings"].append(msg)
                    summary["warnings"].append(msg)

            if uniq == 1:
                msg = f"Column '{col}' has a single unique value (no predictive power)."
                col_info["warnings"].append(msg)
                summary["warnings"].append(msg)

            # ID detection and other diagnostics (abbreviated for space - same as before)
            id_reasons = []
            unique_ratio = (uniq / total_rows_int) if total_rows_int else 0.0
            raw_col = str(col)
            lc = raw_col.lower()
            name_matches = (lc == "id" or lc.startswith("id_") or lc.endswith("_id") or 
                          any(f"_{k}_" in f"_{lc}_" for k in id_keywords))
            sample = s.dropna().astype(str).head(100)
            looks_uuid = False
            if not sample.empty:
                uuid_hits = sum(bool(uuid_re.match(val)) for val in sample)
                looks_uuid = (uuid_hits / len(sample)) >= 0.5
            is_integer = ptypes.is_integer_dtype(s)
            near_unique_int = is_integer and unique_ratio >= 0.99
            is_id_like = bool(name_matches or looks_uuid or near_unique_int)
            if is_id_like:
                if name_matches: id_reasons.append("name_matches")
                if looks_uuid: id_reasons.append("uuid_like")
                if near_unique_int: id_reasons.append("near_unique_integer")
                summary["diagnostics"]["id_like_columns"].append({
                    "column": col, "reasons": id_reasons, "unique_ratio": unique_ratio,
                })
            col_info["is_id_like"] = is_id_like
            if is_id_like:
                col_info.setdefault("flags", []).append("id_like")

            # Sparsity and dtype checks (abbreviated)
            non_null = s.dropna()
            non_null_count = int(non_null.shape[0])
            dominant_ratio = None
            if non_null_count > 0:
                dominant_ratio = int(non_null.value_counts().iloc[0]) / non_null_count
            zero_ratio = None
            if numeric_series is not None and ptypes.is_numeric_dtype(numeric_series):
                nn2 = numeric_series.dropna()
                zero_ratio = float((nn2 == 0).mean()) if len(nn2) > 0 else None
            col_info.update({
                "dominant_value_ratio": round(dominant_ratio, 4) if dominant_ratio is not None else None,
                "zero_ratio": round(zero_ratio, 4) if zero_ratio is not None else None,
            })
            sparse_reasons = []
            if col_info["null_percent"] >= missing_threshold:
                sparse_reasons.append("missing_heavy")
            if dominant_ratio is not None and dominant_ratio >= dominant_ratio_threshold:
                sparse_reasons.append("dominant_value")
            if zero_ratio is not None and zero_ratio >= zero_sparse_threshold:
                sparse_reasons.append("zero_heavy")
            is_sparse = len(sparse_reasons) > 0
            col_info["is_sparse"] = is_sparse
            if is_sparse:
                col_info.setdefault("flags", []).append("sparse")
                summary["diagnostics"]["sparse_columns"].append({
                    "column": col, "reasons": sparse_reasons,
                    "null_percent": round(col_info["null_percent"], 2),
                    "dominant_value_ratio": col_info["dominant_value_ratio"],
                    "zero_ratio": col_info["zero_ratio"],
                })

            inferred = pd.api.types.infer_dtype(s, skipna=True)
            col_info["inferred_dtype"] = inferred
            if s.dtype == "object":
                numeric_coerced = pd.to_numeric(s, errors="coerce")
                obj_numeric_ratio = float(numeric_coerced.notna().mean())
                if obj_numeric_ratio >= numeric_like_ratio:
                    summary["diagnostics"]["dtype_warnings"].append({
                        "column": col, "issue": "object_numeric_like", "ratio": round(obj_numeric_ratio, 2)
                    })
                    col_info.setdefault("flags", []).append("object_numeric_like")
                dt_coerced = pd.to_datetime(s, errors="coerce", utc=True)
                dt_ratio = float(dt_coerced.notna().mean())
                if dt_ratio >= datetime_like_ratio:
                    summary["diagnostics"]["dtype_warnings"].append({
                        "column": col, "issue": "object_datetime_like", "ratio": round(dt_ratio, 2)
                    })
                    col_info.setdefault("flags", []).append("object_datetime_like")
            if inferred.startswith("mixed"):
                summary["diagnostics"]["dtype_warnings"].append({
                    "column": col, "issue": "mixed_types", "inferred": inferred
                })
                col_info.setdefault("flags", []).append("mixed_types")

            # Type counts
            if ptypes.is_numeric_dtype(s):
                summary["type_counts"]["numeric"] += 1
            elif ptypes.is_datetime64_any_dtype(s):
                summary["type_counts"]["datetime"] += 1
            elif ptypes.is_bool_dtype(s):
                summary["type_counts"]["boolean"] += 1
            elif ptypes.is_categorical_dtype(s):
                summary["type_counts"]["categorical"] += 1
            else:
                summary["type_counts"]["categorical"] += 1
                summary["type_counts"]["object"] += 1

            summary["columns"][col] = col_info

        # ========== NEW EDA FEATURES ==========
        
        # Correlation Analysis
        if analyze_correlations:
            logging.info("Performing correlation analysis...")
            corr_results = self.correlation_analyzer.analyze(self.df, threshold=correlation_threshold)
            summary["correlation_analysis"] = corr_results
            
            # Add correlation warnings
            if corr_results['high_correlation_count'] > 0:
                msg = f"Found {corr_results['high_correlation_count']} pairs of highly correlated features (>{correlation_threshold})."
                summary["warnings"].append(msg)
        
        # Leakage Detection
        if detect_leakage:
            logging.info("Detecting potential feature leakage...")
            leakage_results = self.leakage_detector.detect(self.df, target_col=target_column)
            summary["leakage_detection"] = leakage_results
            
            # Add leakage warnings
            for warning in leakage_results['leakage_warnings']:
                if warning['severity'] == 'HIGH':
                    msg = f"🚨 LEAKAGE RISK: {warning['column']} - {warning['description']}"
                    summary["warnings"].append(msg)
        
        # Target Suggestion
        if suggest_target:
            logging.info("Suggesting potential target variables...")
            target_suggestions = self.target_suggester.suggest(self.df)
            summary["target_suggestions"] = target_suggestions
        
        # Dataset Scoring
        if score_dataset:
            logging.info("Calculating dataset quality score...")
            dataset_score = self.dataset_scorer.score(summary, self.df)
            summary["dataset_score"] = dataset_score

        logging.info("CsvProfiler completed comprehensive analysis")
        return summary