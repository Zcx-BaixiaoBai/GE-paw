// Codex-style modal that forces the user to confirm or pick an option before
// the agent can continue. Rendered once at the AppLayout level so it survives
// page navigation. The store handles queuing so multiple requests are answered
// in order.
import { useEffect, useState } from "react";
import { useUserInputStore } from "../stores/userInput";
import { IconClose } from "./Icons";
import { t } from "../lib/i18n";

export function RequestUserInputModal() {
  const current = useUserInputStore((s) => s.current);
  const dismiss = useUserInputStore((s) => s.dismiss);
  const [freeText, setFreeText] = useState("");
  const [pickedId, setPickedId] = useState<string | null>(null);

  useEffect(() => {
    setFreeText("");
    setPickedId(null);
  }, [current?.id]);

  if (!current) return null;

  function submit() {
    const value = pickedId ? { optionId: pickedId, freeText: null } : freeText.trim() ? { optionId: null, freeText: freeText.trim() } : null;
    if (!value) return;
    dismiss(value);
  }

  function onKey(e: React.KeyboardEvent) {
    if (e.key === "Escape") {
      e.preventDefault();
      dismiss({ optionId: null, freeText: null });
    }
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      submit();
    }
  }

  return (
    <div className="modal-backdrop" onKeyDown={onKey} role="dialog" aria-modal>
      <div className="modal-card modal-user-input">
        <div className="modal-head">
          <div className="modal-title">{t("modal.requestUserInput.title")}</div>
          <button className="icon-btn" title={t("modal.requestUserInput.cancel")} onClick={() => dismiss({ optionId: null, freeText: null })}>
            <IconClose size={14} />
          </button>
        </div>
        <div className="modal-body">
          <div className="modal-question">{current.question}</div>
          {current.description && <div className="modal-desc">{current.description}</div>}
          <div className="modal-options">
            {current.options.map((o) => (
              <label key={o.id} className={"modal-option" + (pickedId === o.id ? " picked" : "")}>
                <input
                  type="radio"
                  name={"userinput-" + current.id}
                  checked={pickedId === o.id}
                  onChange={() => setPickedId(o.id)}
                />
                <span className="modal-option-label">{o.label}</span>
                {o.description && <span className="modal-option-desc">{o.description}</span>}
              </label>
            ))}
            {current.allowFreeText && (
              <label className={"modal-option" + (!pickedId ? " picked" : "")}>
                <input
                  type="radio"
                  name={"userinput-" + current.id}
                  checked={!pickedId}
                  onChange={() => setPickedId(null)}
                />
                <span className="modal-option-label">{t("modal.requestUserInput.other")}</span>
                <textarea
                  className="modal-free-text"
                  rows={2}
                  value={freeText}
                  onChange={(e) => setFreeText(e.target.value)}
                  onFocus={() => setPickedId(null)}
                  placeholder={t("modal.requestUserInput.placeholder")}
                />
              </label>
            )}
          </div>
        </div>
        <div className="modal-foot">
          <button onClick={() => dismiss({ optionId: null, freeText: null })}>
            {t("modal.requestUserInput.cancel")}
          </button>
          <button className="primary" onClick={submit} disabled={!pickedId && !freeText.trim()}>
            {t("modal.requestUserInput.submit")}
          </button>
        </div>
      </div>
    </div>
  );
}
