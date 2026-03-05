import logging
from pathlib import Path
import sys
import argparse
from typing import Dict, Any

from .profiler import CsvProfiler
from .report_writer import reportWriter


def setup_logging():
    """Configure logging to both console and file"""
    Path("logs").mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    
    file_handler = logging.FileHandler("logs/app.log", encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logging.getLogger().addHandler(file_handler)


def parse_args():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description="🚀 Auto Mini EDA Tool - Comprehensive CSV Profiling & Analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
📊 FEATURES:
  ✓ Outlier Detection (5 methods)
  ✓ Correlation Analysis
  ✓ Feature Leakage Detection
  ✓ Target Variable Suggestion
  ✓ Dataset Quality Scoring
  ✓ Comprehensive Reporting

🎯 EXAMPLES:
  # Full EDA with all features
  python main_auto_eda.py --csv data.csv
  
  # Quick profile without EDA features
  python main_auto_eda.py --csv data.csv --no-outliers --no-correlation --no-leakage
  
  # Focus on specific target column
  python main_auto_eda.py --csv data.csv --target-column price
  
  # Adjust correlation sensitivity
  python main_auto_eda.py --csv data.csv --correlation-threshold 0.9
  
  # Generate all report formats
  python main_auto_eda.py --csv data.csv --all-formats

💡 TIP: Start with defaults, review the dataset score, then adjust based on recommendations!
        """
    )
    
    # Input/Output
    io_group = parser.add_argument_group('📁 Input/Output Options')
    io_group.add_argument("--csv", type=str, required=True, help="Path to CSV file to analyze")
    io_group.add_argument("--output-dir", type=str, default="reports", help="Output directory for reports (default: reports)")
    
    # Basic Profiling
    profile_group = parser.add_argument_group('📊 Basic Profiling Options')
    profile_group.add_argument("--top-n", type=int, default=5, help="Top N values for categorical columns (default: 5)")
    profile_group.add_argument("--coerce-numeric", action="store_true", help="Try converting non-numeric to numeric")
    profile_group.add_argument("--missing-threshold", type=float, default=30.0, help="Missing value warning threshold %% (default: 30)")
    
    # Outlier Detection
    outlier_group = parser.add_argument_group('🔍 Outlier Detection Options')
    outlier_group.add_argument("--no-outliers", action="store_true", help="Disable outlier detection")
    outlier_group.add_argument("--outlier-methods", nargs="+", 
                               choices=['iqr', 'zscore', 'modified_zscore', 'isolation_forest'],
                               help="Outlier detection methods to use")
    outlier_group.add_argument("--iqr-multiplier", type=float, default=1.5, help="IQR multiplier (default: 1.5)")
    outlier_group.add_argument("--zscore-threshold", type=float, default=3.0, help="Z-score threshold (default: 3.0)")
    
    # EDA Features
    eda_group = parser.add_argument_group('🎯 EDA Features (NEW!)')
    eda_group.add_argument("--no-correlation", action="store_true", help="Disable correlation analysis")
    eda_group.add_argument("--correlation-threshold", type=float, default=0.8, 
                          help="Correlation threshold for warnings (default: 0.8)")
    eda_group.add_argument("--no-leakage", action="store_true", help="Disable leakage detection")
    eda_group.add_argument("--no-target-suggestion", action="store_true", help="Disable target variable suggestion")
    eda_group.add_argument("--target-column", type=str, help="Specify target column (for leakage detection)")
    eda_group.add_argument("--no-scoring", action="store_true", help="Disable dataset quality scoring")
    
    # Report Formats
    format_group = parser.add_argument_group('📄 Report Format Options')
    format_group.add_argument("--all-formats", action="store_true", help="Generate Markdown, JSON, and HTML")
    format_group.add_argument("--json-only", action="store_true", help="Generate only JSON report")
    format_group.add_argument("--html-only", action="store_true", help="Generate only HTML report")
    format_group.add_argument("--no-markdown", action="store_true", help="Skip Markdown report")
    
    return parser.parse_args()


def print_summary(summary: Dict[str, Any], args):
    """Print beautiful console summary"""
    print("\n" + "="*70)
    print("🚀 AUTO MINI EDA - ANALYSIS COMPLETE")
    print("="*70)
    
    # Basic info
    print(f"\n📊 Dataset: {summary.get('file', 'Unknown')}")
    print(f"   Rows: {summary.get('total_rows', 0):,}")
    print(f"   Columns: {summary.get('total_columns', 0)}")
    
    # Dataset Score
    if summary.get('dataset_score'):
        score_data = summary['dataset_score']
        grade = score_data.get('grade', '?')
        quality = score_data.get('quality', 'Unknown')
        percentage = score_data.get('percentage', 0)
        
        grade_emoji = {'A': '🌟', 'B': '✅', 'C': '⚠️', 'D': '❌', 'F': '🚨'}.get(grade, '❓')
        
        print(f"\n{grade_emoji} DATASET QUALITY SCORE: {grade} ({quality})")
        print(f"   Overall: {percentage:.1f}%")
        
        scores = score_data.get('scores', {})
        for category, score_info in scores.items():
            cat_name = category.replace('_', ' ').title()
            pct = score_info.get('percent', 0)
            emoji = '✅' if pct >= 80 else ('⚠️' if pct >= 60 else '❌')
            print(f"   {emoji} {cat_name}: {pct:.0f}%")
    
    # Target Suggestions
    if summary.get('target_suggestions') and summary['target_suggestions'].get('top_candidate'):
        top = summary['target_suggestions']['top_candidate']
        print(f"\n🎯 SUGGESTED TARGET: {top['column']}")
        print(f"   Task Type: {top['task_type'].replace('_', ' ').title()}")
        print(f"   Confidence: {top['score']}/100")
    
    # Leakage Detection
    if summary.get('leakage_detection'):
        leak = summary['leakage_detection']
        if leak.get('high_severity', 0) > 0:
            print(f"\n🚨 LEAKAGE ALERT: {leak['high_severity']} high-severity warnings!")
            print("   ⚠️ Review report before modeling!")
        elif leak.get('total_warnings', 0) > 0:
            print(f"\n⚠️ Leakage Warnings: {leak['total_warnings']} (see report for details)")
        else:
            print("\n✅ No leakage detected")
    
    # Correlation
    if summary.get('correlation_analysis'):
        corr = summary['correlation_analysis']
        high_corr = corr.get('high_correlation_count', 0)
        if high_corr > 0:
            print(f"\n🔗 High Correlations: {high_corr} pairs found")
            print(f"   Threshold: {corr.get('threshold_used', 0.8)}")
    
    # Outliers
    if summary.get('outlier_summary'):
        outlier = summary['outlier_summary']
        cols_with_outliers = outlier.get('total_columns_with_outliers', 0)
        total_outliers = outlier.get('total_outliers_detected', 0)
        if cols_with_outliers > 0:
            print(f"\n🔍 Outliers Detected:")
            print(f"   Columns: {cols_with_outliers}")
            print(f"   Total outliers: {total_outliers}")
    
    # Warnings
    warnings = summary.get('warnings', [])
    if warnings:
        print(f"\n⚠️ Data Quality Warnings: {len(warnings)}")
        for i, warning in enumerate(warnings[:3], 1):
            # Truncate long warnings
            short_warn = warning[:60] + "..." if len(warning) > 60 else warning
            print(f"   {i}. {short_warn}")
        if len(warnings) > 3:
            print(f"   ... and {len(warnings) - 3} more (see full report)")
    
    # Recommendations
    if summary.get('dataset_score') and summary['dataset_score'].get('recommendations'):
        recs = summary['dataset_score']['recommendations']
        print(f"\n💡 TOP RECOMMENDATIONS:")
        for i, rec in enumerate(recs[:3], 1):
            print(f"   {i}. {rec}")
    
    print("\n" + "="*70 + "\n")


def main():
    """Main execution"""
    setup_logging()
    args = parse_args()

    # Validate CSV path
    csv_path = Path(args.csv)
    if not csv_path.exists():
        logging.error("CSV file not found: %s", csv_path)
        print(f"❌ Error: CSV file not found: {csv_path}")
        sys.exit(1)

    print("\n🚀 Starting Auto Mini EDA...")
    print(f"📊 Analyzing: {csv_path.name}\n")
    
    # Create profiler and load data
    try:
        profiler = CsvProfiler(str(csv_path))
        profiler.load(low_memory=False)
        logging.info("Successfully loaded CSV with shape: %s", profiler.df.shape)
    except Exception as e:
        logging.exception("Failed to load CSV")
        print(f"❌ Error loading CSV: {e}")
        sys.exit(2)

    # Run comprehensive profiling
    try:
        print("⏳ Running comprehensive analysis...")
        print("   • Basic profiling")
        if not args.no_outliers:
            print("   • Outlier detection")
        if not args.no_correlation:
            print("   • Correlation analysis")
        if not args.no_leakage:
            print("   • Leakage detection")
        if not args.no_target_suggestion:
            print("   • Target suggestion")
        if not args.no_scoring:
            print("   • Dataset scoring")
        
        summary = profiler.profile(
            top_n=args.top_n,
            coerce_numeric=args.coerce_numeric,
            missing_threshold=args.missing_threshold,
            # Outlier detection
            detect_outliers=not args.no_outliers,
            outlier_methods=args.outlier_methods,
            outlier_iqr_multiplier=args.iqr_multiplier,
            outlier_zscore_threshold=args.zscore_threshold,
            # EDA features
            analyze_correlations=not args.no_correlation,
            correlation_threshold=args.correlation_threshold,
            detect_leakage=not args.no_leakage,
            suggest_target=not args.no_target_suggestion,
            target_column=args.target_column,
            score_dataset=not args.no_scoring,
        )
        
        print("✅ Analysis complete!\n")
        
    except Exception as e:
        logging.exception("Profiling failed")
        print(f"❌ Error during profiling: {e}")
        sys.exit(3)

    # Generate reports
    try:
        writer = reportWriter(output_dir=args.output_dir)
        
        # Determine formats
        generate_md = not args.json_only and not args.html_only and not args.no_markdown
        generate_json = args.all_formats or args.json_only
        generate_html = args.all_formats or args.html_only
        
        print("📝 Generating reports...")
        reports_generated = []
        
        if generate_md:
            md_path = writer.write(summary)
            reports_generated.append(("Markdown", md_path))
            logging.info("Markdown report: %s", md_path)
        
        if generate_json:
            json_path = writer.write_json(summary)
            reports_generated.append(("JSON", json_path))
            logging.info("JSON report: %s", json_path)
        
        if generate_html:
            html_path = writer.write_html(summary)
            reports_generated.append(("HTML", html_path))
            logging.info("HTML report: %s", html_path)
        
        # Print summary
        print_summary(summary, args)
        
        # Show generated reports
        print("📄 Reports Generated:")
        for fmt, path in reports_generated:
            print(f"   • {fmt}: {path}")
        
        print("\n✨ Done! Check the reports for detailed insights.\n")
        
    except Exception as e:
        logging.exception("Report generation failed")
        print(f"❌ Error generating reports: {e}")
        sys.exit(4)


if __name__ == "__main__":
    main()