import { HandoffError, type SourceDocument } from "./contracts";

/** Only passive, recognized originals are embedded; never trust a file extension or render SVG/HTML. */
export async function verifiedOriginal(blob: Blob, document: SourceDocument): Promise<Blob> {
  const bytes = new Uint8Array(await blob.slice(0, 16).arrayBuffer());
  const ascii = new TextDecoder().decode(bytes);
  const starts = (...signature: number[]) => signature.every((byte, i) => bytes[i] === byte);
  const mime = ascii.startsWith("%PDF-")
    ? "application/pdf"
    : starts(137, 80, 78, 71, 13, 10, 26, 10)
      ? "image/png"
      : starts(255, 216, 255)
        ? "image/jpeg"
        : /^GIF8[79]a/.test(ascii)
          ? "image/gif"
          : ascii.startsWith("RIFF") && ascii.slice(8, 12) === "WEBP"
            ? "image/webp"
            : undefined;
  const reported = document.mimeType?.split(";")[0].trim().toLowerCase();
  if (!mime || (reported && reported !== mime && reported !== "application/octet-stream")) {
    throw new HandoffError("document");
  }
  if (document.sha256) {
    const digest = await crypto.subtle.digest("SHA-256", await blob.arrayBuffer());
    const hash = Array.from(new Uint8Array(digest), (b) => b.toString(16).padStart(2, "0")).join(
      "",
    );
    if (hash !== document.sha256) {
      throw new HandoffError("document");
    }
  }
  return new Blob([blob], { type: mime });
}
