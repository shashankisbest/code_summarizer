# summarizer/report_generator.py
"""
Generate formatted reports from analysis data
"""
from typing import Dict, Any, List
from typing import Dict, Any, List
import json

class ReportGenerator:
    """
    Formats analysis results into readable reports
    """
    
    def __init__(self):
        self.report_formats = ['text', 'json', 'markdown']
    
    def generate_report(self, ast_analysis: Dict, security_findings: Dict, 
                        ml_summary: str, source_code: str, format_type: str = 'text') -> str:
        """
        Generate report in specified format
        """
        if format_type == 'text':
            return self._generate_text_report(ast_analysis, security_findings, ml_summary)
        elif format_type == 'json':
            return self._generate_json_report(ast_analysis, security_findings, ml_summary)
        elif format_type == 'markdown':
            return self._generate_markdown_report(ast_analysis, security_findings, ml_summary)
        else:
            return self._generate_text_report(ast_analysis, security_findings, ml_summary)
    
    def _generate_text_report(self, ast_data: Dict, security: Dict, summary: str) -> str:
        """Generate plain text report"""
        report = []
        
        # Header
        report.append("=" * 70)
        report.append("🔍 CODE ANALYSIS REPORT")
        report.append("=" * 70)
        report.append("")
        
        # ML Summary
        report.append("📋 SUMMARY")
        report.append("-" * 70)
        report.append(summary)
        report.append("")
        
        # Statistics
        report.append("📊 STATISTICS")
        report.append("-" * 70)
        report.append(f"   - Functions: {len(ast_data.get('functions', []))}")
        report.append(f"   - Classes: {len(ast_data.get('classes', []))}")
        
        imports = ast_data.get('imports', {})
        total_imports = len(imports.get('direct', [])) + len(imports.get('from', []))
        report.append(f"   - Imports: {total_imports}")
        report.append(f"   - Lines of Code: {ast_data.get('line_count', 0)}")
        report.append("")
        
        # Complexity
        report.append("⚙️ COMPLEXITY ANALYSIS")
        report.append("-" * 70)
        complexity = ast_data.get('complexity', {})
        report.append(f"   - Cyclomatic Complexity: {complexity.get('cyclomatic', 0)}")
        report.append(f"   - Cognitive Complexity: {complexity.get('cognitive', 0)}")
        report.append(f"   - Maintainability Index: {complexity.get('maintainability', 0):.1f}")
        report.append(f"   - Level: {complexity.get('level', 'unknown').upper()}")
        report.append("")
        
        # Functions (show up to 10)
        if ast_data.get('functions'):
            report.append("🔧 FUNCTIONS")
            report.append("-" * 70)
            functions = ast_data['functions'][:10]
            for func in functions:
                params = ', '.join(func.get('params', [])[:3])
                if len(func.get('params', [])) > 3:
                    params += ', ...'
                report.append(f"   • {func['name']}({params})")
            
            total_funcs = len(ast_data['functions'])
            if total_funcs > 10:
                report.append(f"   ... and {total_funcs - 10} more functions")
            report.append("")
        
        # Security
        report.append("🔒 SECURITY AUDIT")
        report.append("-" * 70)
        report.append(f"   Security Score: {security.get('security_score', 0)}/100")
        
        if security.get('high_risk'):
            report.append(f"   ⚠️ HIGH RISK: {', '.join(security['high_risk'])}")
        if security.get('medium_risk'):
            # Filter out false positives
            medium_risks = [r for r in security['medium_risk'] if r not in ['open', 'open']]
            if medium_risks:
                report.append(f"   ⚠️ MEDIUM RISK: {', '.join(medium_risks)}")
        
        if security.get('recommendations'):
            report.append("")
            report.append("   💡 Recommendations:")
            for rec in security['recommendations'][:3]:
                report.append(f"      • {rec}")
        
        report.append("")
        report.append("=" * 70)
        
        return '\n'.join(report)
    
    def _generate_json_report(self, ast_data: Dict, security: Dict, summary: str) -> str:
        """Generate JSON report"""
        report = {
            'summary': summary,
            'statistics': {
                'functions': len(ast_data.get('functions', [])),
                'classes': len(ast_data.get('classes', [])),
                'imports': len(ast_data.get('imports', {}).get('direct', [])) + len(ast_data.get('imports', {}).get('from', [])),
                'lines_of_code': ast_data.get('line_count', 0)
            },
            'complexity': ast_data.get('complexity', {}),
            'security': {
                'score': security.get('security_score', 0),
                'high_risk': security.get('high_risk', []),
                'medium_risk': security.get('medium_risk', []),
                'recommendations': security.get('recommendations', [])
            },
            'functions': ast_data.get('functions', [])[:10],
            'classes': ast_data.get('classes', [])[:5]
        }
        
        return json.dumps(report, indent=2)
    
    def _generate_markdown_report(self, ast_data: Dict, security: Dict, summary: str) -> str:
        """Generate Markdown report"""
        report = []
        
        report.append("# 🔍 Code Analysis Report\n")
        
        # Summary
        report.append("## 📋 Summary")
        report.append(f"{summary}\n")
        
        # Statistics
        report.append("## 📊 Statistics")
        report.append("| Metric | Value |")
        report.append("|--------|-------|")
        report.append(f"| Functions | {len(ast_data.get('functions', []))} |")
        report.append(f"| Classes | {len(ast_data.get('classes', []))} |")
        
        imports = ast_data.get('imports', {})
        total_imports = len(imports.get('direct', [])) + len(imports.get('from', []))
        report.append(f"| Imports | {total_imports} |")
        report.append(f"| Lines of Code | {ast_data.get('line_count', 0)} |\n")
        
        # Complexity
        report.append("## ⚙️ Complexity Analysis")
        complexity = ast_data.get('complexity', {})
        report.append(f"- **Cyclomatic Complexity**: {complexity.get('cyclomatic', 0)}")
        report.append(f"- **Cognitive Complexity**: {complexity.get('cognitive', 0)}")
        report.append(f"- **Maintainability Index**: {complexity.get('maintainability', 0):.1f}")
        report.append(f"- **Level**: {complexity.get('level', 'unknown').upper()}\n")
        
        # Security
        report.append("## 🔒 Security Audit")
        report.append(f"**Security Score**: {security.get('security_score', 0)}/100\n")
        
        if security.get('recommendations'):
            report.append("### 💡 Recommendations")
            for rec in security['recommendations']:
                report.append(f"- {rec}")
        
        return '\n'.join(report)