import { useAutoDismiss } from "./motion";
import type { Toast, UpdateTab } from "./updates";

export function UpdateToast({
  toast,
  onView,
  onDismiss,
}: {
  toast: Toast | undefined;
  onView(tab: UpdateTab): void;
  onDismiss(): void;
}) {
  const hold = useAutoDismiss(toast, onDismiss);
  return (
    <div className="toast-region" role="status" aria-live="polite">
      {toast && (
        <div className="toast" {...hold}>
          <p>
            {toast.text}
            {toast.more > 0 && (
              <span className="faint">
                {" "}
                · {toast.more} more {toast.more === 1 ? "update" : "updates"}
              </span>
            )}
          </p>
          <button type="button" className="link" onClick={() => onView(toast.tab)}>
            View
          </button>
          <button type="button" className="toast-close" aria-label="Dismiss" onClick={onDismiss}>
            ×
          </button>
        </div>
      )}
    </div>
  );
}
