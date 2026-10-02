import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from pipeline.adapters import for_url
from pipeline.adapters.laserfiche import Adapter
from pipeline.core import PipelineError

REF = 'https://records.huntingtonbeachca.gov/WebLink/DocView.aspx?id=6780479&repo=COHB&dbid=0'


class LaserficheTests(unittest.TestCase):
    def test_selected_pages_preserve_document_sequence(self):
        calls = []
        def request(url, cookies, payload=None):
            if payload is None:
                return '<html>viewer shell</html>'
            if 'GetBasicDocumentInfo' in url:
                return {'id': 6780479, 'pageCount': 170, 'name': 'Agreement'}
            calls.append(payload['pageNum'])
            return {'text': f"Publisher page {payload['pageNum']}"}
        with tempfile.TemporaryDirectory() as tmp, patch('pipeline.adapters.laserfiche.base.cache_dir', return_value=Path(tmp)), patch.object(Adapter, '_request', side_effect=request):
            result = Adapter().section(REF + '#pages=30-32')
        self.assertEqual(calls, [30, 31, 32])
        self.assertEqual(result['extra']['document_page_count'], 170)
        self.assertEqual(result['text'], 'Publisher page 30\n\f\nPublisher page 31\n\f\nPublisher page 32')

    def test_missing_ocr_does_not_become_partial_or_viewer_text(self):
        def request(url, cookies, payload=None):
            if payload is None:
                return 'Loading official document viewer'
            if 'GetBasicDocumentInfo' in url:
                return {'id': 6780479, 'pageCount': 2}
            return {'text': 'Legal content' if payload['pageNum'] == 1 else ''}
        with tempfile.TemporaryDirectory() as tmp, patch('pipeline.adapters.laserfiche.base.cache_dir', return_value=Path(tmp)), patch.object(Adapter, '_request', side_effect=request):
            with self.assertRaisesRegex(PipelineError, 'page 2 has no OCR'):
                Adapter().section(REF)
            self.assertEqual(list(Path(tmp).iterdir()), [])

    def test_publisher_routes_to_reader(self):
        self.assertIsInstance(for_url(REF), Adapter)
