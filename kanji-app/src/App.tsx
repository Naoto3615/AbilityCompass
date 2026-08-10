import { useState, useEffect, useCallback } from 'react';
import { Header } from './components/Header';
import { KanjiManager } from './components/KanjiManager';
import { PrintSettings as PrintSettingsPanel } from './components/PrintSettings';
import { PrintPreview } from './components/PrintPreview';
import type { KanjiEntry, PrintSettings } from './types';
import { loadKanjiData, saveKanjiData } from './data/kanji2nd';

type Tab = 'settings' | 'preview' | 'manage';

const defaultSettings: PrintSettings = {
  childName: '',
  problemType: 'trace',
  problemCount: 5,
  theme: 'stars',
  showStampRally: true,
  showDifficultyBadge: true,
  selectedKanjiIds: [],
  strokeOrderKanjiIds: [],
  randomize: true,
};

const SETTINGS_KEY = 'kanji-app-settings';

const VALID_PROBLEM_TYPES = new Set<PrintSettings['problemType']>(['trace', 'reading', 'fill']);

function normalizeSettings(
  raw: Partial<PrintSettings> & { showStampArea?: boolean },
): PrintSettings {
  const migrated = { ...raw };
  if (migrated.showStampRally === undefined && migrated.showStampArea !== undefined) {
    migrated.showStampRally = migrated.showStampArea;
  }
  delete migrated.showStampArea;

  return {
    ...defaultSettings,
    ...migrated,
    problemType:
      migrated.problemType && VALID_PROBLEM_TYPES.has(migrated.problemType)
        ? migrated.problemType
        : defaultSettings.problemType,
    selectedKanjiIds: Array.isArray(migrated.selectedKanjiIds) ? migrated.selectedKanjiIds : [],
    strokeOrderKanjiIds: Array.isArray(migrated.strokeOrderKanjiIds)
      ? migrated.strokeOrderKanjiIds
      : [],
  };
}

function loadSettings(): PrintSettings {
  try {
    const s = localStorage.getItem(SETTINGS_KEY);
    if (s) return normalizeSettings(JSON.parse(s));
  } catch { /* ignore */ }
  return defaultSettings;
}

function saveSettings(s: PrintSettings) {
  try { localStorage.setItem(SETTINGS_KEY, JSON.stringify(s)); } catch { /* ignore */ }
}

const tabConfig: { id: Tab; label: string; emoji: string }[] = [
  { id: 'settings', label: 'プリント設定', emoji: '⚙️' },
  { id: 'preview', label: 'プレビュー', emoji: '👀' },
  { id: 'manage', label: '漢字リスト', emoji: '📚' },
];

export default function App() {
  const [kanjiList, setKanjiList] = useState<KanjiEntry[]>(() => loadKanjiData());
  const [settings, setSettings] = useState<PrintSettings>(() => loadSettings());
  const [activeTab, setActiveTab] = useState<Tab>('settings');

  useEffect(() => { saveKanjiData(kanjiList); }, [kanjiList]);
  useEffect(() => { saveSettings(settings); }, [settings]);

  const handlePrint = useCallback(() => {
    setActiveTab('preview');
    setTimeout(() => { window.print(); }, 300);
  }, []);

  const handleUpdateSettings = useCallback((s: PrintSettings) => {
    setSettings(s);
  }, []);

  return (
    <div className="min-h-screen">
      <Header />

      {/* Print-only content (hidden on screen, shown on print) */}
      <div className="hidden print:block">
        <PrintPreview settings={settings} kanjiList={kanjiList} printMode />
      </div>

      {/* Main UI (hidden on print) */}
      <main className="no-print max-w-7xl mx-auto px-4 py-6">
        {/* Tab navigation */}
        <div className="flex gap-2 mb-6 bg-white/70 backdrop-blur-sm rounded-2xl p-2 shadow-md">
          {tabConfig.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex-1 flex items-center justify-center gap-2 py-3 rounded-xl font-bold text-sm transition-all ${
                activeTab === tab.id
                  ? 'bg-gradient-to-r from-pink-400 to-purple-400 text-white shadow-md scale-[1.02]'
                  : 'text-gray-500 hover:bg-pink-50 hover:text-pink-600'
              }`}
            >
              <span>{tab.emoji}</span>
              <span className="hidden sm:inline">{tab.label}</span>
            </button>
          ))}
        </div>

        {/* Content */}
        <div className="animate-fade-in">
          {activeTab === 'settings' && (
            <PrintSettingsPanel
              settings={settings}
              kanjiList={kanjiList}
              onUpdate={handleUpdateSettings}
              onPrint={handlePrint}
            />
          )}
          {activeTab === 'preview' && (
            <div>
              <PrintPreview settings={settings} kanjiList={kanjiList} />
              <div className="mt-4 flex gap-3 justify-center">
                <button
                  onClick={() => setActiveTab('settings')}
                  className="px-6 py-3 rounded-2xl border-2 border-pink-300 text-pink-600 font-bold hover:bg-pink-50 transition-colors"
                >
                  ← もどる
                </button>
                <button
                  onClick={() => window.print()}
                  className="px-8 py-3 rounded-2xl bg-gradient-to-r from-pink-400 to-purple-400 text-white font-black shadow-lg hover:shadow-xl transition-all hover:scale-[1.02]"
                >
                  🖨️ 印刷する！
                </button>
              </div>
            </div>
          )}
          {activeTab === 'manage' && (
            <KanjiManager kanjiList={kanjiList} onUpdate={setKanjiList} />
          )}
        </div>
      </main>

      {/* Bottom wave decoration */}
      <div className="no-print fixed bottom-0 left-0 right-0 pointer-events-none overflow-hidden h-16 opacity-30">
        <svg viewBox="0 0 1440 64" className="w-full" xmlns="http://www.w3.org/2000/svg">
          <path
            d="M0,32 C360,64 720,0 1080,32 C1260,48 1380,40 1440,32 L1440,64 L0,64 Z"
            fill="#f9a8d4"
          />
        </svg>
      </div>
    </div>
  );
}
