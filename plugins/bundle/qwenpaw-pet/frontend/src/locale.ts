/** Pet plugin UI locale ?follows gepaw console ``localStorage.language``. */

import { readConsoleLanguage } from "./watchConsoleLanguage";

export type PetLocale = "zh" | "en";

export type MessageKey = keyof typeof messages.en;

const messages = {
  en: {
    routeLabel: "Pet",
    title: "gepaw Pet",
    intro:
      "Installed pets live under your gepaw working directory. Start the desktop bridge, then switch the floating pet without restarting gepaw.",
    startDesktop: "Start desktop pet",
    importPet: "Import pet",
    refresh: "Refresh",
    petsDirectory: "Pets directory:",
    desktopHealth: "Desktop health:",
    desktopUnknown: "unknown (refresh)",
    colPreview: "Preview",
    colName: "Name",
    colFolder: "Folder",
    colManifestId: "pet.json id",
    colAction: "Action",
    switch: "Switch",
    tableEmpty: "No pets found. Run: gepaw-pet install-pet ?,
    desktopAlreadyRunning: "Desktop pet is already running.",
    desktopStartFailed: "Could not start the desktop pet.",
    desktopReady: "Desktop pet is ready.",
    desktopStarting:
      "Desktop may still be starting; check pet-desktop.log if needed.",
    dropFolderOrZip: "Drop a folder or a .zip file.",
    importChooseFirst: "Drop a folder or choose a .zip file first.",
    importSuccess: 'Imported "{name}" ?{path}',
    switchSuccess: 'Switched to "{name}" ({petId})',
    switchFailed: "switch failed",
    modalImportTitle: "Import pet",
    modalImportOk: "Import",
    dropzoneTitle: "Drop a folder or .zip file here",
    dropzoneHint: "or click to choose a .zip",
    importFormatHint:
      "Folder or unzipped archive must contain pet.json and spritesheet.webp (15361872).",
    selectedOne: "Selected: {path}",
    selectedMany: "Selected: {count} files (root: {root})",
    importReplace: "Replace if a pet with the same id already exists",
  },
  zh: {
    routeLabel: "",
    title: "gepaw ",
    intro:
      " gepaw  gepaw ?,
    startDesktop: "",
    importPet: "",
    refresh: "",
    petsDirectory: "?,
    desktopHealth: "",
    desktopUnknown: "?,
    colPreview: "",
    colName: "",
    colFolder: "?,
    colManifestId: "pet.json id",
    colAction: "",
    switch: "",
    tableEmpty: "qwenpaw-pet install-pet ?,
    desktopAlreadyRunning: "?,
    desktopStartFailed: "?,
    desktopReady: "?,
    desktopStarting: "?pet-desktop.log?,
    dropFolderOrZip: "?.zip ?,
    importChooseFirst: " .zip ?,
    importSuccess: "{name} {path}",
    switchSuccess: "{name}{petId}?,
    switchFailed: "",
    modalImportTitle: "",
    modalImportOk: "",
    dropzoneTitle: "?.zip ?,
    dropzoneHint: " .zip ",
    importFormatHint:
      " pet.json ?spritesheet.webp?5361872?,
    selectedOne: "{path}",
    selectedMany: "{count} {root}?,
    importReplace: " id ",
  },
} as const;

/** Map gepaw console language to pet UI locale (non zh/en ?en). */
export function toPetLocale(language: string | null | undefined): PetLocale {
  const base = String(language || "")
    .trim()
    .split("-")[0]
    .toLowerCase();
  if (base === "zh") return "zh";
  return "en";
}

export function resolvePetLocale(language?: string | null): PetLocale {
  return toPetLocale(language ?? readConsoleLanguage());
}

export function t(
  locale: PetLocale,
  key: MessageKey,
  params?: Record<string, string | number>,
): string {
  let text: string = messages[locale][key] ?? messages.en[key];
  if (params) {
    for (const [name, value] of Object.entries(params)) {
      text = text.split(`{${name}}`).join(String(value));
    }
  }
  return text;
}
