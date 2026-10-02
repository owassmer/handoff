"""Add recovered district publication; preserve unresolved resolution questions."""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

def write(path, data):
    backup = path.with_suffix(path.suffix + '.before-notice-recovery')
    if not backup.exists():
        shutil.copy2(path, backup)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')

path = ROOT / 'j1/register_updates.json'
data = json.loads(path.read_text())
item = next(x for x in data['instruments'] if x['id'] == 'CA-HB:SBSD:ASSESSMENT-NOTICES2025-2026')
url = 'https://www.sunnews.org/wp-content/uploads/2024/06/6-13-24-SBS-class.pdf'
unit = {
    'unit': 'FY2024-25-NOTICE',
    'heading': 'Notice of filing report — FY2024–25, dated June11,2024',
    'toc_url': url,
    'source_unit_kind': 'document',
    'section_list': [{'number': 'FY2024-25-NOTICE', 'heading': 'District notice §§1–6', 'ref': url}],
    'reason': 'District-issued publication explicitly connects increased charges to March14,2024 approval after no majority protest; states classifications, owner liability and tax-roll election. It is not the named resolution attachment.',
    'locator': 'PDF page5, lower left two-column notice, publication143444',
    'local_evidence': 'j1/reassessment/scrape-resume/sbsd/2024-06-13-public-notice.pdf',
    'capture_method': 'Downloaded PDF, extracted text and visually reviewed notice.'
}
item['units_in_scope'] = [unit] + [x for x in item['units_in_scope'] if x['unit'] != unit['unit']]
u26 = next(x for x in item['units_in_scope'] if x['unit'] == 'FY2026-27-NOTICE')
u26.update({
    'locator': 'PDF page4, right two-column notice §§1–6, publication163652',
    'capture_method': 'Downloaded PDF, extracted text and visually reviewed notice; supersedes prior indexed-only capture.',
    'local_evidence': 'j1/reassessment/scrape-resume/sbsd/2026-05-28-public-notice.pdf'
})
item['retrieval_note'] = '2024 and2026 actual newspaper PDFs recovered and visually reviewed;2026 is no longer indexed-only. Resolution attachments remain unresolved.'
item['observed_terms']['rate_change'] = '2024 notice states increases of60 trash,100 sewer and150 restaurant cleaning and connects them to March14,2024 approval.2025 and2026 notices state no increase from their preceding year.'
write(path, data)

path = ROOT / 'j1/WORK.json'
data = json.loads(path.read_text())
for task in data['tasks']:
    if task['task'] == 'Establish remaining relevant source facts through online recovery':
        task['status'] = 'in_progress'
        task.pop('blocker', None)
data['latest_online_recovery'] = {
    'evidence': 'j1/reassessment/scrape-resume/',
    'result': 'Added actual2024 district fee notice and recovered full2026 notice. HOME carrier bodies and scanned appendices did not establish incorporated guideline edition. Source-selection gaps remain open; no external contact.'
}
write(path, data)
