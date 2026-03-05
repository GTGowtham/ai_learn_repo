import os
import json
from typing import Dict, Any


class reportWriter:
    """
    Ultimate report writer with comprehensive EDA reporting:
    - Outlier detection results
    - Correlation analysis
    - Feature leakage warnings
    - Target variable suggestions
    - Dataset quality scoring
    """

    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def write(self, summary: Dict[str, Any], filename: str = "csv_profile_report.md") -> str:
        """Write comprehensive Markdown report with all EDA features"""
        path = os.path.join(self.output_dir, filename)

        file_name = summary.get("file", "Unknown file")
        total_rows = summary.get("total_rows", "N/A")
        total_cols = summary.get("total_columns", "N/A")
        mem_bytes = summary.get("memory_usage_bytes", None)
        warnings = summary.get("warnings", []) or []
        type_counts = summary.get("type_counts", {}) or {}
        diagnostics = summary.get("diagnostics", {}) or {}
        columns = summary.get("columns", {}) or {}
        
        # NEW: EDA sections
        outlier_summary = summary.get("outlier_summary", {}) or {}
        correlation_analysis = summary.get("correlation_analysis", {})
        leakage_detection = summary.get("leakage_detection", {})
        target_suggestions = summary.get("target_suggestions", {})
        dataset_score = summary.get("dataset_score", {})

        with open(path, "w", encoding="utf-8") as f:
            # ========== HEADER ==========
            f.write("# 📊 Auto Mini EDA Report\n\n")
            f.write(f"**File**: `{file_name}`\n\n")
            f.write(f"**Total rows**: {total_rows:,}\n\n")
            f.write(f"**Total columns**: {total_cols}\n\n")
            if mem_bytes is not None:
                f.write(f"**Memory usage**: {self._fmt_bytes(mem_bytes)}\n\n")

            # ========== DATASET QUALITY SCORE (NEW!) ==========
            if dataset_score:
                f.write("## 🎯 Dataset Quality Score\n\n")
                grade = dataset_score.get('grade', 'N/A')
                quality = dataset_score.get('quality', 'Unknown')
                percentage = dataset_score.get('percentage', 0)
                total_score = dataset_score.get('total_score', 0)
                max_score = dataset_score.get('max_score', 100)
                
                # Grade badge
                grade_emoji = {'A': '🌟', 'B': '✅', 'C': '⚠️', 'D': '❌', 'F': '🚨'}.get(grade, '❓')
                f.write(f"### Overall Grade: {grade_emoji} **{grade}** - {quality}\n\n")
                f.write(f"**Score**: {total_score:.1f} / {max_score:.1f} ({percentage:.1f}%)\n\n")
                
                # Score breakdown
                f.write("#### Score Breakdown\n\n")
                f.write("| Category | Score | Max | Percentage |\n")
                f.write("|----------|-------|-----|------------|\n")
                scores = dataset_score.get('scores', {})
                for category, score_data in scores.items():
                    cat_name = category.replace('_', ' ').title()
                    score_val = score_data.get('score', 0)
                    max_val = score_data.get('max', 25)
                    pct = score_data.get('percent', 0)
                    f.write(f"| {cat_name} | {score_val:.1f} | {max_val} | {pct:.1f}% |\n")
                f.write("\n")
                
                # Recommendations
                recommendations = dataset_score.get('recommendations', [])
                if recommendations:
                    f.write("#### 💡 Recommendations\n\n")
                    for rec in recommendations:
                        f.write(f"- {rec}\n")
                    f.write("\n")

            # ========== TARGET SUGGESTIONS (NEW!) ==========
            if target_suggestions:
                f.write("## 🎯 Target Variable Suggestions\n\n")
                suggestions = target_suggestions.get('suggestions', [])
                
                if suggestions:
                    top_candidate = suggestions[0]
                    f.write(f"### 🌟 Top Candidate: `{top_candidate['column']}`\n\n")
                    f.write(f"- **Score**: {top_candidate['score']}/100\n")
                    f.write(f"- **Task Type**: {top_candidate['task_type'].replace('_', ' ').title()}\n")
                    f.write(f"- **Unique Values**: {top_candidate['unique_values']}\n")
                    f.write(f"- **Data Type**: {top_candidate['data_type']}\n")
                    f.write("- **Reasons**:\n")
                    for reason in top_candidate['reasons']:
                        f.write(f"  - {reason}\n")
                    f.write("\n")
                    
                    if len(suggestions) > 1:
                        f.write("### Other Candidates\n\n")
                        f.write("| Column | Score | Task Type | Unique Values |\n")
                        f.write("|--------|-------|-----------|---------------|\n")
                        for sug in suggestions[1:]:
                            task_type = sug['task_type'].replace('_', ' ').title()
                            f.write(f"| `{sug['column']}` | {sug['score']} | {task_type} | {sug['unique_values']} |\n")
                        f.write("\n")
                else:
                    f.write("> No clear target variable detected. Manual selection recommended.\n\n")

            # ========== LEAKAGE DETECTION (NEW!) ==========
            if leakage_detection:
                leakage_warnings = leakage_detection.get('leakage_warnings', [])
                
                if leakage_warnings:
                    f.write("## 🚨 Feature Leakage Detection\n\n")
                    f.write(f"**Total Warnings**: {leakage_detection.get('total_warnings', 0)}\n")
                    f.write(f"- 🚨 High Severity: {leakage_detection.get('high_severity', 0)}\n")
                    f.write(f"- ⚠️ Medium Severity: {leakage_detection.get('medium_severity', 0)}\n")
                    f.write(f"- ℹ️ Low Severity: {leakage_detection.get('low_severity', 0)}\n\n")
                    
                    # Group by severity
                    high_sev = [w for w in leakage_warnings if w.get('severity') == 'HIGH']
                    medium_sev = [w for w in leakage_warnings if w.get('severity') == 'MEDIUM']
                    low_sev = [w for w in leakage_warnings if w.get('severity') == 'LOW']
                    
                    if high_sev:
                        f.write("### 🚨 High Severity (Immediate Action Required)\n\n")
                        for warning in high_sev:
                            f.write(f"- **`{warning.get('column', 'Unknown')}`**: {warning.get('description', 'N/A')}\n")
                            if 'correlation' in warning:
                                f.write(f"  - Correlation with target: {warning['correlation']:.4f}\n")
                        f.write("\n")
                    
                    if medium_sev:
                        f.write("### ⚠️ Medium Severity (Review Recommended)\n\n")
                        for warning in medium_sev:
                            f.write(f"- **`{warning.get('column', 'Unknown')}`**: {warning.get('description', 'N/A')}\n")
                        f.write("\n")
                    
                    if low_sev:
                        f.write("### ℹ️ Low Severity (Informational)\n\n")
                        for warning in low_sev[:5]:  # Limit to first 5
                            col_or_cols = warning.get('column') or warning.get('columns', 'Unknown')
                            if isinstance(col_or_cols, list):
                                col_or_cols = ', '.join(f"`{c}`" for c in col_or_cols)
                            else:
                                col_or_cols = f"`{col_or_cols}`"
                            f.write(f"- {col_or_cols}: {warning.get('description', 'N/A')}\n")
                        if len(low_sev) > 5:
                            f.write(f"- ... and {len(low_sev) - 5} more\n")
                        f.write("\n")

            # ========== CORRELATION ANALYSIS (NEW!) ==========
            if correlation_analysis and correlation_analysis.get('high_correlations'):
                f.write("## 🔗 Correlation Analysis\n\n")
                f.write(f"**Numeric columns analyzed**: {correlation_analysis.get('numeric_columns_analyzed', 0)}\n")
                f.write(f"**Correlation threshold**: {correlation_analysis.get('threshold_used', 0.8)}\n")
                f.write(f"**High correlations found**: {correlation_analysis.get('high_correlation_count', 0)}\n\n")
                
                high_corrs = correlation_analysis.get('high_correlations', [])
                
                if high_corrs:
                    f.write("### Top Correlated Feature Pairs\n\n")
                    f.write("| Feature 1 | Feature 2 | Correlation | Type |\n")
                    f.write("|-----------|-----------|-------------|------|\n")
                    for corr in high_corrs[:10]:  # Top 10
                        corr_val = corr.get('correlation', 0)
                        corr_type = corr.get('type', 'unknown')
                        emoji = '📈' if corr_type == 'positive' else '📉'
                        f.write(f"| `{corr['feature_1']}` | `{corr['feature_2']}` | {corr_val:.3f} | {emoji} {corr_type} |\n")
                    f.write("\n")
                
                # Multicollinearity groups
                multi_groups = correlation_analysis.get('multicollinearity_groups', [])
                if multi_groups:
                    f.write("### 🔄 Multicollinearity Groups\n\n")
                    f.write("Groups of highly correlated features (consider removing some):\n\n")
                    for i, group in enumerate(multi_groups[:5], 1):
                        members = ', '.join(f"`{m}`" for m in group['members'])
                        f.write(f"{i}. **Group Size**: {group['size']} features - {members}\n")
                        f.write(f"   - Average correlation: {group['avg_correlation']:.3f}\n")
                        f.write(f"   - Max correlation: {group['max_correlation']:.3f}\n")
                    f.write("\n")

            # ========== OUTLIER SUMMARY ==========
            if outlier_summary.get('total_columns_with_outliers', 0) > 0:
                f.write("## 🔍 Outlier Detection Summary\n\n")
                f.write(f"- **Columns with outliers**: {outlier_summary.get('total_columns_with_outliers', 0)}\n")
                f.write(f"- **Total outliers detected**: {outlier_summary.get('total_outliers_detected', 0)}\n")
                f.write(f"- **Detection methods used**: {', '.join(outlier_summary.get('methods_used', []))}\n\n")

            # ========== WARNINGS ==========
            if warnings:
                f.write("## ⚠️ Data Quality Warnings\n\n")
                for w in warnings:
                    f.write(f"- {self._md_text(w)}\n")
                f.write("\n")

            # ========== TYPE COUNTS ==========
            if type_counts:
                f.write("## 📊 Column Type Distribution\n\n")
                for key in ["numeric", "categorical", "datetime", "boolean", "object"]:
                    count = type_counts.get(key, 0)
                    if count > 0:
                        f.write(f"- **{key.title()}**: {count}\n")
                f.write("\n")

            # ========== DIAGNOSTICS ==========
            if diagnostics:
                # Outlier columns
                outlier_cols = diagnostics.get("outlier_columns", []) or []
                if outlier_cols:
                    f.write("## 🎯 Columns with Detected Outliers\n\n")
                    f.write("| Column | Outlier Count | Outlier % | Methods Detected |\n")
                    f.write("|--------|---------------|-----------|------------------|\n")
                    for item in outlier_cols:
                        col = item.get("column", "?")
                        count = item.get("outlier_count", 0)
                        pct = item.get("outlier_percent", 0.0)
                        methods = ", ".join(item.get("methods_detected", []))
                        f.write(f"| `{col}` | {count} | {pct:.2f}% | {methods} |\n")
                    f.write("\n")
                
                # ID-like columns
                id_like = diagnostics.get("id_like_columns", []) or []
                if id_like:
                    f.write("## 🔑 ID-like Columns (Consider Removing)\n\n")
                    for item in id_like:
                        col = item.get("column", "?")
                        reasons = item.get("reasons", [])
                        ur = item.get("unique_ratio", None)
                        ur_txt = f"{ur:.2f}" if isinstance(ur, (int, float)) and ur is not None else "N/A"
                        f.write(f"- `{col}` (reasons: {', '.join(reasons) if reasons else 'N/A'}, unique_ratio: {ur_txt})\n")
                    f.write("\n")

                # Sparse columns
                sparse_cols = diagnostics.get("sparse_columns", []) or []
                if sparse_cols:
                    f.write("## 🕳️ Sparse Columns (Low Information)\n\n")
                    for item in sparse_cols:
                        col = item.get("column", "?")
                        reasons = item.get("reasons", [])
                        npct = item.get("null_percent", None)
                        f.write(f"- `{col}` (reasons: {', '.join(reasons) if reasons else 'N/A'}, null%: {self._fmt_num(npct)})\n")
                    f.write("\n")

                # Dtype warnings
                dtype_warn = diagnostics.get("dtype_warnings", []) or []
                if dtype_warn:
                    f.write("## ⚙️ Data Type Issues\n\n")
                    for item in dtype_warn:
                        col = item.get("column", "?")
                        issue = item.get("issue", "unknown_issue")
                        f.write(f"- `{col}`: {issue}\n")
                    f.write("\n")

            f.write("---\n\n")

            # ========== COLUMN DETAILS ==========
            f.write("## 📋 Detailed Column Analysis\n\n")
            if not columns:
                f.write("> No column details available.\n")
                return path

            for col in sorted(columns.keys(), key=lambda x: str(x).lower()):
                details = columns[col]
                f.write(f"### {col}\n\n")

                preferred_order = [
                    "dtype", "inferred_dtype", "null_count", "null_percent",
                    "unique_count", "mean", "median", "std", "min", "q1", "q3", "max",
                    "dominant_value_ratio", "zero_ratio", "is_id_like", "is_sparse",
                    "flags", "warnings", "top_values", "outliers",
                ]

                printed_keys = set()
                for k in preferred_order:
                    if k in details:
                        if k == "outliers":
                            self._print_outlier_section_markdown(f, details[k])
                        else:
                            self._print_kv_markdown(f, k, details[k])
                        printed_keys.add(k)

                for k in sorted(details.keys()):
                    if k not in printed_keys:
                        self._print_kv_markdown(f, k, details[k])

                f.write("\n")

        return path

    def _print_outlier_section_markdown(self, f, outlier_data: Dict) -> None:
        """Print comprehensive outlier detection results"""
        if not outlier_data or not isinstance(outlier_data, dict):
            return
        
        f.write("- **Outlier Detection Results**:\n")
        
        for method_name, method_result in outlier_data.items():
            if not isinstance(method_result, dict):
                continue
            
            if 'error' in method_result:
                f.write(f"  - **{method_name}**: Error - {method_result['error']}\n")
                continue
            
            has_outliers = method_result.get('has_outliers', False)
            outlier_count = method_result.get('outlier_count', 0)
            outlier_percent = method_result.get('outlier_percent', 0.0)
            
            if method_name == 'iqr':
                f.write(f"  - **IQR Method**: {outlier_count} outliers ({outlier_percent:.2f}%)\n")
                if has_outliers:
                    f.write(f"    - Bounds: [{method_result.get('lower_bound', 'N/A'):.2f}, {method_result.get('upper_bound', 'N/A'):.2f}]\n")
                    outlier_vals = method_result.get('outlier_values', [])
                    if outlier_vals:
                        vals_str = ", ".join([f"{v:.2f}" if isinstance(v, float) else str(v) for v in outlier_vals[:5]])
                        f.write(f"    - Sample: {vals_str}{'...' if len(outlier_vals) > 5 else ''}\n")
            elif method_name == 'zscore':
                f.write(f"  - **Z-Score Method**: {outlier_count} outliers ({outlier_percent:.2f}%)\n")
            elif method_name == 'modified_zscore':
                f.write(f"  - **Modified Z-Score**: {outlier_count} outliers ({outlier_percent:.2f}%)\n")
            elif method_name == 'consensus':
                f.write(f"  - **Consensus**: {outlier_count} avg outliers ({outlier_percent:.2f}%)\n")

    def write_json(self, summary: Dict[str, Any], filename: str = "csv_profile_report.json") -> str:
        """Export complete summary to JSON"""
        path = os.path.join(self.output_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        return path

    def write_html(self, summary: Dict[str, Any], filename: str = "csv_profile_report.html") -> str:
        """Generate interactive HTML report"""
        path = os.path.join(self.output_dir, filename)
        
        # Extract data
        file_name = summary.get("file", "Unknown file")
        dataset_score = summary.get("dataset_score", {})
        target_suggestions = summary.get("target_suggestions", {})
        leakage_detection = summary.get("leakage_detection", {})
        correlation_analysis = summary.get("correlation_analysis", {})
        
        def esc(x: Any) -> str:
            return (str(x).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

        with open(path, "w", encoding="utf-8") as f:
            f.write("""<!doctype html><html><head><meta charset='utf-8'>
<title>Auto Mini EDA Report</title>
<style>
body{font-family:Segoe UI,Arial,sans-serif;margin:0;padding:20px;background:#f5f5f5}
.container{max-width:1200px;margin:0 auto;background:white;padding:30px;border-radius:8px;box-shadow:0 2px 4px rgba(0,0,0,0.1)}
h1{color:#2c3e50;border-bottom:3px solid #3498db;padding-bottom:10px}
h2{color:#34495e;margin-top:30px;border-left:4px solid #3498db;padding-left:10px}
.score-card{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;padding:20px;border-radius:8px;margin:20px 0}
.score-grade{font-size:48px;font-weight:bold;text-align:center;margin:10px 0}
.metric{display:inline-block;margin:10px 20px;padding:10px;background:rgba(255,255,255,0.1);border-radius:4px}
table{border-collapse:collapse;width:100%;margin:15px 0}
th,td{border:1px solid #ddd;padding:12px;text-align:left}
th{background:#3498db;color:white;font-weight:600}
tr:nth-child(even){background:#f9f9f9}
.warning-high{background:#e74c3c;color:white;padding:10px;border-radius:4px;margin:5px 0}
.warning-medium{background:#f39c12;color:white;padding:10px;border-radius:4px;margin:5px 0}
.badge{display:inline-block;padding:4px 8px;border-radius:4px;font-size:12px;font-weight:bold}
.badge-success{background:#27ae60;color:white}
.badge-warning{background:#f39c12;color:white}
.badge-danger{background:#e74c3c;color:white}
code{background:#ecf0f1;padding:2px 6px;border-radius:3px;font-family:monospace}
</style>
</head><body><div class='container'>""")
            
            f.write(f"<h1>📊 Auto Mini EDA Report</h1>")
            f.write(f"<p><strong>File</strong>: <code>{esc(file_name)}</code></p>")
            
            # Dataset Score Card
            if dataset_score:
                grade = dataset_score.get('grade', 'N/A')
                quality = dataset_score.get('quality', 'Unknown')
                percentage = dataset_score.get('percentage', 0)
                
                f.write(f"<div class='score-card'>")
                f.write(f"<h2 style='color:white;border:none;margin:0'>Dataset Quality Score</h2>")
                f.write(f"<div class='score-grade'>{grade}</div>")
                f.write(f"<p style='text-align:center;font-size:20px'>{quality}</p>")
                f.write(f"<p style='text-align:center'>{percentage:.1f}% Overall Score</p>")
                f.write(f"</div>")
                
                # Recommendations
                recommendations = dataset_score.get('recommendations', [])
                if recommendations:
                    f.write("<h2>💡 Key Recommendations</h2><ul>")
                    for rec in recommendations:
                        f.write(f"<li>{esc(rec)}</li>")
                    f.write("</ul>")
            
            # Target Suggestions
            if target_suggestions and target_suggestions.get('suggestions'):
                top = target_suggestions['suggestions'][0]
                f.write(f"<h2>🎯 Suggested Target Variable</h2>")
                f.write(f"<p><strong>Column</strong>: <code>{esc(top['column'])}</code> ")
                f.write(f"<span class='badge badge-success'>Score: {top['score']}</span></p>")
                f.write(f"<p><strong>Task Type</strong>: {esc(top['task_type'].replace('_', ' ').title())}</p>")
            
            # Leakage Warnings
            if leakage_detection and leakage_detection.get('high_severity', 0) > 0:
                f.write("<h2>🚨 Feature Leakage Warnings</h2>")
                for warning in leakage_detection.get('leakage_warnings', []):
                    if warning.get('severity') == 'HIGH':
                        col = warning.get('column', 'Unknown')
                        desc = warning.get('description', '')
                        f.write(f"<div class='warning-high'><strong>{esc(col)}</strong>: {esc(desc)}</div>")
            
            # Correlation Table
            if correlation_analysis and correlation_analysis.get('high_correlations'):
                f.write("<h2>🔗 High Correlations</h2>")
                f.write("<table><tr><th>Feature 1</th><th>Feature 2</th><th>Correlation</th></tr>")
                for corr in correlation_analysis['high_correlations'][:10]:
                    f.write(f"<tr><td><code>{esc(corr['feature_1'])}</code></td>")
                    f.write(f"<td><code>{esc(corr['feature_2'])}</code></td>")
                    f.write(f"<td>{corr['correlation']:.3f}</td></tr>")
                f.write("</table>")
            
            f.write("</div></body></html>")
        
        return path

    # Helper methods
    def _fmt_bytes(self, n: Any) -> str:
        try:
            n = int(n)
        except Exception:
            return "N/A"
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if n < 1024:
                return f"{n:.0f} {unit}"
            n /= 1024
        return f"{n:.0f} PB"

    def _fmt_num(self, v: Any) -> str:
        if v is None:
            return "None"
        if isinstance(v, float):
            txt = f"{v:.4f}"
            while txt.endswith("0"):
                txt = txt[:-1]
            if txt.endswith("."):
                txt = txt[:-1]
            return txt
        return str(v)

    def _md_text(self, s: Any) -> str:
        return str(s).replace("`", "\\`")

    def _print_kv_markdown(self, f, key: str, value: Any) -> None:
        """Pretty print key-value pair to Markdown"""
        if isinstance(value, dict):
            f.write(f"- **{key}**:\n")
            for kk, vv in value.items():
                out = self._fmt_num(vv) if isinstance(vv, (int, float)) else self._md_text(vv)
                f.write(f"  - `{kk}`: {out}\n")
        elif isinstance(value, (list, tuple)):
            f.write(f"- **{key}**:\n")
            for item in value:
                if isinstance(item, dict):
                    sub = ", ".join(f"{k}={self._fmt_num(v) if isinstance(v, (int, float)) else v}"
                                    for k, v in item.items())
                    f.write(f"  - {self._md_text(sub)}\n")
                else:
                    f.write(f"  - {self._md_text(item)}\n")
        else:
            vv = self._fmt_num(value) if isinstance(value, (int, float)) else self._md_text(value)
            f.write(f"- **{key}**: {vv}\n")