// @vitest-environment jsdom
import { act, cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { DocumentViewer } from "./DocumentViewer";
import { deferred, exampleGateway, exampleWorkspace } from "./examples.test-support";

function setup() {
  const data = exampleWorkspace();
  const summary = {
    ...data.documents[0],
    sourceKind: "Prepared" as const,
    sourceDocumentIds: ["file-a", "file-b"],
    mimeType: null,
  };
  const files = [
    {
      ...data.documents[1],
      id: "file-a",
      title: "Condition correspondence excerpt.pdf",
      kind: "Contextual material",
      sourceKind: "Original" as const,
      text: "Open the attached file.",
    },
    {
      ...data.documents[1],
      id: "file-b",
      title: "Maintenance record.pdf",
      mediaItemRid: "second-file",
      kind: "Contextual material",
      sourceKind: "Original" as const,
      text: "Open the attached file.",
    },
  ];
  const { gateway } = exampleGateway({ ...data, documents: [summary, ...files] });
  const create = vi.fn(() => "blob:supporting-file"),
    release = vi.fn();
  vi.stubGlobal("URL", Object.assign(URL, { createObjectURL: create, revokeObjectURL: release }));
  const close = vi.fn();
  const view = render(
    <DocumentViewer
      document={summary}
      documents={[summary, ...files]}
      gateway={gateway}
      onClose={close}
    />,
  );
  return { summary, files, gateway, create, release, close, ...view };
}
afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
  vi.unstubAllGlobals();
});
const back = (t: ReturnType<typeof setup>) =>
  screen.getByRole("button", { name: `← ${t.summary.title}` });

describe("Supporting files", () => {
  it("shows the record's text with its files, and fetches only the file that is opened", async () => {
    const t = setup();
    expect(screen.getByText(/The kitchen wall needs a small plaster repair/)).toBeTruthy();
    expect(t.gateway.document).not.toHaveBeenCalled();
    fireEvent.click(screen.getByRole("button", { name: t.files[0].title }));
    await screen.findByTitle(t.files[0].title);
    expect(screen.queryByText("Open the attached file.")).toBeNull();
    expect(t.gateway.document).toHaveBeenCalledExactlyOnceWith(t.files[0]);
    expect(screen.getByRole("link", { name: "Download" }).getAttribute("download")).toBe(
      t.files[0].title,
    );
    fireEvent.click(back(t));
    expect(t.release).toHaveBeenCalledWith("blob:supporting-file");
    fireEvent.click(screen.getByRole("button", { name: t.files[1].title }));
    await screen.findByTitle(t.files[1].title);
    expect(t.gateway.document).toHaveBeenLastCalledWith(t.files[1]);
  });
  it("opens a record's only file directly, with its summary one click back", async () => {
    const t = setup();
    cleanup();
    const one = { ...t.summary, sourceDocumentIds: ["file-a"] };
    render(
      <DocumentViewer
        document={one}
        documents={[one, ...t.files]}
        gateway={t.gateway}
        onClose={t.close}
      />,
    );
    await screen.findByTitle(t.files[0].title);
    expect(t.gateway.document).toHaveBeenCalledExactlyOnceWith(t.files[0]);
    fireEvent.click(screen.getByRole("button", { name: `← ${one.title}` }));
    expect(screen.getByText(/The kitchen wall needs a small plaster repair/)).toBeTruthy();
  });
  it("keeps an open file across equivalent refreshed data", async () => {
    const t = setup();
    fireEvent.click(screen.getByRole("button", { name: t.files[0].title }));
    await screen.findByTitle(t.files[0].title);
    t.rerender(
      <DocumentViewer
        document={structuredClone(t.summary)}
        documents={structuredClone([t.summary, ...t.files])}
        gateway={t.gateway}
        onClose={t.close}
      />,
    );
    expect(screen.getByTitle(t.files[0].title)).toBeTruthy();
    expect(t.release).not.toHaveBeenCalled();
    expect(t.gateway.document).toHaveBeenCalledTimes(1);
  });
  it.each(["removed", "version", "reference"])(
    "closes the file when its source is %s",
    async (change) => {
      const t = setup();
      fireEvent.click(screen.getByRole("button", { name: t.files[0].title }));
      await screen.findByTitle(t.files[0].title);
      const docs =
        change === "removed"
          ? [t.summary, t.files[1]]
          : [
              t.summary,
              {
                ...t.files[0],
                ...(change === "version"
                  ? { sourceVersion: "2" }
                  : { mediaItemRid: "changed-file" }),
              },
              t.files[1],
            ];
      t.rerender(
        <DocumentViewer
          document={t.summary}
          documents={docs}
          gateway={t.gateway}
          onClose={t.close}
        />,
      );
      expect(screen.queryByTitle(t.files[0].title)).toBeNull();
      expect(screen.getByRole("alert").textContent).toMatch(/changed or is no longer available/);
      expect(t.release).toHaveBeenCalledWith("blob:supporting-file");
    },
  );
  it("removes the file name and preview when access is withdrawn", async () => {
    const t = setup();
    let invalidate: () => void = () => {};
    t.gateway.onDocumentInvalidated = vi.fn((_doc, callback) => {
      invalidate = callback;
      return () => {};
    });
    fireEvent.click(screen.getByRole("button", { name: t.files[0].title }));
    await screen.findByTitle(t.files[0].title);
    act(() => invalidate());
    expect(screen.queryByTitle(t.files[0].title)).toBeNull();
    expect(screen.queryByRole("heading", { name: t.files[0].title })).toBeNull();
    expect(screen.getByRole("alert").textContent).toContain("no longer available");
    expect(t.release).toHaveBeenCalledWith("blob:supporting-file");
  });
  it("discards a late file after going back", async () => {
    const t = setup(),
      result = deferred<Blob>();
    vi.mocked(t.gateway.document).mockReturnValueOnce(result.promise);
    fireEvent.click(screen.getByRole("button", { name: t.files[0].title }));
    fireEvent.click(back(t));
    await act(async () => result.resolve(new Blob(["%PDF-1.7"], { type: "application/pdf" })));
    expect(t.create).not.toHaveBeenCalled();
    expect(screen.getByRole("button", { name: t.files[1].title })).toBeTruthy();
  });
});
