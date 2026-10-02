import unittest
from pipeline.adapters.sharepoint import parse_ref, pdf_payload
from pipeline.core import PipelineError


class SharePointPDFTests(unittest.TestCase):
    def envelope(self, name="legal.pdf", payload=b"%PDF-1.4\nbody", length=None):
        size = len(payload) if length is None else length
        return (b'--BOUNDARY\r\nContent-Disposition: form-data; name="pdf"; filename="' + name.encode()
                + b'"\r\nContent-Type: application/pdf\r\nContent-Length: ' + str(size).encode()
                + b'\r\n\r\n' + payload + b'\r\n--BOUNDARY--\r\n')

    def test_requested_multipart_pdf_only(self):
        self.assertEqual(pdf_payload(self.envelope(), "legal.pdf"), b"%PDF-1.4\nbody")
        for body in [self.envelope(name="other.pdf"), self.envelope(length=999),
                     self.envelope(payload=b"<html>sign in</html>"), b"<html>%PDF-fake</html>"]:
            with self.subTest(body=body), self.assertRaises(PipelineError):
                pdf_payload(body, "legal.pdf")

    def test_reference_preserves_exact_document_path_and_share(self):
        share = "https://edisonintl.sharepoint.com/:f:/t/Public/TM2/id?e=public"
        full = share + "#document=%2Fteams%2FPublic%2Ffolder%20name%2Flegal.pdf"
        self.assertEqual(parse_ref(full), (share, "/teams/Public/folder name/legal.pdf",
                         "https://edisonintl.sharepoint.com/teams/Public/folder%20name/legal.pdf"))
        for bad in [share, share + "#document=https%3A%2F%2Fother.test%2Fx.pdf",
                    share + "#document=%2Fteams%2Fx.pdf&document=%2Fteams%2Fy.pdf"]:
            with self.subTest(ref=bad), self.assertRaises(PipelineError):
                parse_ref(bad)


if __name__ == '__main__':
    unittest.main()
