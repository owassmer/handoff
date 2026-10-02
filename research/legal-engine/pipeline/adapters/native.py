"""Mechanical conversion of selected native documents; binary data is never HTML."""
import pathlib
import shutil
import subprocess
import tempfile
from urllib.parse import urlsplit

from . import base


def convert(raw, ref):
    """Return (text, converter) for native documents, None for strict UTF-8 text.

    Legacy XLS requires xlrd in the pipeline Python environment. Word conversion
    uses macOS textutil without launching Word. Missing converters fail explicitly.
    """
    suffix = pathlib.PurePosixPath(urlsplit(ref).path).suffix.lower()
    ole = raw.startswith(bytes.fromhex("d0cf11e0a1b11ae1"))
    archive = raw.startswith(b"PK")
    rtf = raw.lstrip().startswith(b"{\\rtf")
    if suffix == ".xls" and ole:
        try:
            import xlrd
        except ImportError as exc:
            raise base.core.PipelineError("generic: XLS conversion requires xlrd in the pipeline Python environment") from exc
        try:
            workbook = xlrd.open_workbook(file_contents=raw)
            chunks = []
            for sheet in workbook.sheets():
                chunks.append(sheet.name)
                for row in range(sheet.nrows):
                    chunks.append("\t".join(str(cell.value) for cell in sheet.row(row)))
            return "\n".join(chunks), "xlrd (sheet names and stored cell values; no formula recalculation)"
        except Exception as exc:
            raise base.core.PipelineError(f"generic: XLS conversion failed: {exc}") from exc
    if (suffix == ".doc" and ole) or (suffix == ".docx" and archive) or rtf:
        executable = shutil.which("textutil")
        if not executable:
            raise base.core.PipelineError("generic: DOC/DOCX/RTF conversion requires textutil")
        with tempfile.TemporaryDirectory(prefix="legal-native-") as directory:
            source = pathlib.Path(directory) / ("source.rtf" if rtf else "source" + suffix)
            source.write_bytes(raw)
            try:
                result = subprocess.run([executable, "-convert", "txt", "-encoding", "UTF-8", "-stdout", str(source)],
                                        capture_output=True, timeout=60)
            except (OSError, subprocess.TimeoutExpired) as exc:
                raise base.core.PipelineError(f"generic: textutil conversion failed: {exc}") from exc
        if result.returncode or not result.stdout.strip():
            raise base.core.PipelineError("generic: textutil could not extract native document text")
        return result.stdout.decode("utf-8", "strict"), "textutil (plain text conversion)"
    if ole or archive or b"\x00" in raw:
        raise base.core.PipelineError(f"generic: unsupported binary document at {ref}; conversion required")
    if suffix in (".doc", ".docx", ".xls"):
        raise base.core.PipelineError(f"generic: response does not contain the selected native document at {ref}")
    try:
        decoded = raw.decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise base.core.PipelineError(f"generic: non-UTF-8 response at {ref}; explicit encoding or native conversion required") from exc
    if any(ord(c) < 32 and c not in "\n\r\t\f" for c in decoded):
        raise base.core.PipelineError(f"generic: binary control bytes at {ref}; conversion required")
    return None
